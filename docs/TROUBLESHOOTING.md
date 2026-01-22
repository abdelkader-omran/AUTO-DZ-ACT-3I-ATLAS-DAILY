# Troubleshooting Guide

## Common Issues and Solutions

This guide helps you diagnose and resolve common issues with the AUTO-DZ-ACT-3I-ATLAS-DAILY monitoring system.

## Table of Contents

- [Workflow Issues](#workflow-issues)
- [Data Collection Issues](#data-collection-issues)
- [File and Permission Issues](#file-and-permission-issues)
- [Network and Connectivity Issues](#network-and-connectivity-issues)
- [Data Integrity Issues](#data-integrity-issues)
- [GitHub Actions Issues](#github-actions-issues)
- [Configuration Issues](#configuration-issues)

---

## Workflow Issues

### Workflow doesn't run on schedule

**Symptoms:**
- Workflow scheduled for 03:15 UTC but doesn't execute
- No automatic commits from `trizel-monitor[bot]`

**Possible Causes:**
1. Repository has been inactive for 60+ days
2. GitHub Actions disabled for the repository
3. Workflow file has syntax errors

**Solutions:**

**Check if Actions are enabled:**
1. Go to repository Settings → Actions → General
2. Ensure "Allow all actions and reusable workflows" is selected
3. Check that workflows have write permissions

**Trigger manually to reactivate:**
```bash
# Go to Actions → TRIZEL Monitor → Run workflow
# Leave fields empty and click "Run workflow"
```

**Verify cron syntax:**
```yaml
schedule:
  - cron: "15 3 * * *"  # Must be exactly this format
```

**Check workflow file:**
```bash
# Validate YAML syntax
cat .github/workflows/trizel-monitor.yml
```

### Workflow fails immediately

**Symptoms:**
- Workflow starts but fails within seconds
- Error: "No such file or directory"

**Solutions:**

**Check Python version:**
```yaml
# In .github/workflows/trizel-monitor.yml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.11"  # Must be 3.7+
```

**Verify script exists:**
```bash
ls -la scripts/trizel_monitor.py
```

**Check working directory:**
```bash
# Workflow should run from repository root
pwd  # Should show: /home/runner/work/AUTO-DZ-ACT-3I-ATLAS-DAILY/AUTO-DZ-ACT-3I-ATLAS-DAILY
```

---

## Data Collection Issues

### No data fetched for some sources

**Symptoms:**
- Snapshot shows `"ok": false` for one or more sources
- Error messages in fetch results

**Diagnosis:**

**Check snapshot file:**
```bash
cat data/snapshots/snapshot_2026-01-22.json | python -m json.tool
```

**Look for error messages:**
```json
{
  "source_id": "NASA_JPL_SBDB",
  "ok": false,
  "error": "Connection timeout after 25s"
}
```

**Common Errors and Solutions:**

#### "Connection timeout after 25s"

**Cause:** Remote server slow or unresponsive

**Solution:**
- This is expected occasionally (server maintenance, high load)
- Re-run workflow later or next day
- If persistent, check if source URL changed

#### "HTTP Error 404: Not Found"

**Cause:** URL no longer valid

**Solution:**
1. Verify URL in browser
2. Update `registry/sources.json` with correct URL
3. Re-run with `--overwrite` flag

#### "HTTP Error 403: Forbidden"

**Cause:** Server blocking automated requests

**Solution:**
- Check User-Agent header (already set correctly)
- Source may require authentication (not currently supported)
- Contact source maintainers if persistent

#### "HTTP Error 500: Internal Server Error"

**Cause:** Remote server error

**Solution:**
- Wait and retry later
- If persistent, report to source maintainers

### All sources fail

**Symptoms:**
- Every fetch result shows `"ok": false`
- Network-related errors for all sources

**Diagnosis:**

**Check network connectivity:**
```bash
# Test from GitHub Actions runner
curl -I https://www.google.com
```

**Possible Causes:**
1. GitHub Actions network issue (rare)
2. Firewall blocking outbound HTTPS
3. DNS resolution failure

**Solutions:**
- Re-run workflow (usually temporary)
- Check GitHub Status page
- If persistent, open GitHub Support ticket

### Snapshot files are empty or missing fields

**Symptoms:**
- Snapshot exists but has missing data
- JSON parse errors

**Diagnosis:**

**Validate JSON:**
```bash
python -m json.tool data/snapshots/snapshot_2026-01-22.json
```

**Check file size:**
```bash
ls -lh data/snapshots/snapshot_2026-01-22.json
# Should be at least a few KB
```

**Solution:**
- Delete corrupted file
- Re-run workflow with `--overwrite`

---

## File and Permission Issues

### "Permission denied" errors

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'data/snapshots/snapshot_2026-01-22.json'
```

**Solutions:**

**Check directory permissions:**
```bash
ls -la data/
ls -la data/snapshots/
```

**Fix permissions:**
```bash
chmod -R u+w data/
```

**In GitHub Actions:**
- Usually not a problem (runner has full access)
- Check if workflow permissions set correctly:
```yaml
permissions:
  contents: write  # Required for committing
```

### "No such file or directory" for data directories

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/snapshots/'
```

**Solution:**

**Script should auto-create directories:**
```python
# This is handled by safe_mkdir() in the script
# If failing, check script has write access
```

**Manual creation:**
```bash
mkdir -p data/snapshots data/manifests data/raw data/metadata
```

### Disk space issues

**Symptoms:**
- Workflow fails during file write
- "No space left on device"

**Diagnosis:**

**Check disk usage:**
```bash
du -sh data/
df -h .
```

**Solutions:**
- Archive old raw data files
- Clean up unnecessary files
- For GitHub Actions: rarely an issue (runners have sufficient space)

---

## Network and Connectivity Issues

### Intermittent fetch failures

**Symptoms:**
- Failures occur randomly
- Same source succeeds some days, fails others

**Causes:**
- Network latency
- Server load
- Temporary outages

**Solutions:**
- Normal behavior; don't worry about occasional failures
- Historical data preserved in successful runs
- Can backfill specific dates if needed:
```bash
python scripts/trizel_monitor.py --start 2026-01-22 --end 2026-01-22 --overwrite
```

### Timeout errors (25s timeout)

**Symptoms:**
```
"error": "Connection timeout after 25s"
```

**Diagnosis:**
- 25-second timeout is intentional (prevents hanging)
- Indicates slow server response

**Solutions:**
- Accept occasional timeouts as normal
- If timeout is consistent for a source:
  - Check if URL changed
  - Verify source is still operational
  - Consider increasing timeout in script (not recommended)

---

## Data Integrity Issues

### Checksum mismatches

**Symptoms:**
- Manifest SHA-256 doesn't match snapshot file
- Raw file checksum doesn't match snapshot record

**Diagnosis:**

**Verify snapshot integrity:**
```bash
MANIFEST_SHA=$(cat data/manifests/manifest_2026-01-22.json | jq -r '.snapshot.sha256')
ACTUAL_SHA=$(sha256sum data/snapshots/snapshot_2026-01-22.json | awk '{print $1}')
echo "Manifest: $MANIFEST_SHA"
echo "Actual:   $ACTUAL_SHA"
```

**Causes:**
1. File was modified after creation
2. Corruption during write
3. Git line-ending conversion (shouldn't happen with JSON)

**Solutions:**

**Regenerate the snapshot:**
```bash
python scripts/trizel_monitor.py --start 2026-01-22 --end 2026-01-22 --overwrite
```

**Check Git configuration:**
```bash
git config core.autocrlf
# Should be "false" or "input", not "true"
```

### Missing raw data files

**Symptoms:**
- Snapshot references a `raw_path` but file doesn't exist
- Directory `data/raw/YYYY-MM-DD/SOURCE_ID/` is empty

**Causes:**
1. Fetch failed (check `"ok": false` in snapshot)
2. Files were manually deleted
3. Script error during save

**Solutions:**

**Re-fetch the data:**
```bash
python scripts/trizel_monitor.py --start 2026-01-22 --end 2026-01-22 --overwrite
```

**Check fetch status:**
```bash
cat data/snapshots/snapshot_2026-01-22.json | jq '.fetch_results[] | select(.raw_path != null)'
```

---

## GitHub Actions Issues

### Workflow doesn't commit changes

**Symptoms:**
- Workflow runs successfully
- No new commit appears in repository

**Diagnosis:**

**Check workflow logs:**
- Go to Actions → Select workflow run → View logs
- Look for "Commit generated snapshot" step

**Common Messages:**

#### "Nothing to commit"

**Cause:** No new or changed files

**Solutions:**
- Normal if snapshot already exists and unchanged
- Use `--overwrite` to force regeneration

#### "Permission denied"

**Cause:** Workflow lacks write permissions

**Solution:**
```yaml
# In .github/workflows/trizel-monitor.yml
permissions:
  contents: write  # Ensure this is set
```

### Release creation fails

**Symptoms:**
- Snapshot commits successfully
- No GitHub release created

**Diagnosis:**

**Check release step logs:**
```
Error: Release already exists
```

**Solutions:**

**Normal behavior:**
- Release creation is idempotent
- Existing release is updated with new assets

**If truly failing:**
1. Check `GH_TOKEN` is available:
```yaml
env:
  GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

2. Verify permissions:
```yaml
permissions:
  contents: write  # Required for releases
```

---

## Configuration Issues

### Empty sources registry

**Symptoms:**
```
Error: Registry sources list is empty and --allow-empty-sources not set
```

**Cause:** `registry/sources.json` has empty `sources` array

**Solution:**

**Verify registry:**
```bash
cat registry/sources.json | jq '.sources | length'
# Should be > 0
```

**Fix registry:**
- Restore from Git history if accidentally emptied
- Add at least one valid source

**Emergency workaround (NOT recommended):**
```bash
python scripts/trizel_monitor.py --allow-empty-sources
```

### Invalid JSON in registry

**Symptoms:**
```
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes
```

**Diagnosis:**

**Validate JSON:**
```bash
cat registry/sources.json | python -m json.tool
```

**Solutions:**
- Fix JSON syntax errors (missing commas, quotes, brackets)
- Use a JSON validator or linter
- Restore from Git history if corrupted

### Missing required fields

**Symptoms:**
- Script runs but produces incomplete snapshots
- Missing source information

**Diagnosis:**

**Check registry schema:**
```bash
cat registry/sources.json | jq '.sources[0] | keys'
```

**Required fields:**
- `id`, `name`, `institution`, `authority`, `role`, `official`, `url`

**Solution:**
- Add missing fields to source objects
- See [Data Formats](DATA_FORMATS.md) for complete schema

---

## Debugging Steps

### General debugging workflow

1. **Check the logs**
   ```bash
   # GitHub Actions: View workflow run logs
   # Local: Script outputs to console
   ```

2. **Verify configuration**
   ```bash
   cat registry/sources.json | python -m json.tool
   ```

3. **Test locally**
   ```bash
   python scripts/trizel_monitor.py
   ```

4. **Check recent changes**
   ```bash
   git log --oneline -10
   git diff HEAD~1
   ```

5. **Validate data files**
   ```bash
   # Validate JSON
   python -m json.tool data/snapshots/snapshot_2026-01-22.json

   # Check checksums
   sha256sum data/snapshots/*.json
   ```

### Collecting diagnostic information

When reporting issues, include:

1. **Workflow run URL** (if applicable)
2. **Error messages** (complete stack trace)
3. **Snapshot date** that failed
4. **Registry configuration** (sanitize if needed)
5. **Recent commits** (`git log --oneline -5`)
6. **Environment** (Python version, OS)

### Manual intervention

**Re-run specific date:**
```bash
python scripts/trizel_monitor.py --start 2026-01-22 --end 2026-01-22 --overwrite
```

**Backfill range:**
```bash
python scripts/trizel_monitor.py --start 2026-01-15 --end 2026-01-22
```

**Check single source manually:**
```bash
curl -I https://www.minorplanetcenter.net/
```

---

## Getting Help

### Before asking for help

1. Check this troubleshooting guide
2. Review [User Guide](USER_GUIDE.md)
3. Check [Script Reference](SCRIPT_REFERENCE.md)
4. Search existing GitHub Issues

### How to report issues

1. Go to GitHub Issues
2. Create a new issue
3. Include:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs
   - Environment details

### Emergency contacts

For urgent issues affecting scientific operations:
- Create a high-priority GitHub Issue
- Tag with `urgent` label
- Contact repository maintainers directly

---

## Preventive Measures

### Regular maintenance

**Weekly:**
- Review workflow execution logs
- Check for repeated failures
- Verify disk usage

**Monthly:**
- Review all source URLs
- Test registry configuration
- Validate data integrity (spot checks)

**Quarterly:**
- Archive old raw data (optional)
- Review and update documentation
- Test disaster recovery procedures

### Monitoring

**Key metrics to watch:**
- Success rate of fetches (should be >90%)
- Workflow execution time (should be <5 minutes)
- Data size growth (should be steady)

**Set up alerts:**
- GitHub Actions can notify on workflow failures
- Settings → Notifications → Actions

### Best practices

1. **Don't modify historical data**
   - Use `--overwrite` sparingly
   - Keep original snapshots intact

2. **Test changes locally**
   - Before modifying registry or workflow
   - Use a test date range

3. **Document changes**
   - Commit messages should be clear
   - Update documentation when needed

4. **Back up critical data**
   - Registry configuration
   - Git repository itself
   - Release artifacts (already on GitHub)

---

## Related Documentation

- [User Guide](USER_GUIDE.md) - How to use the system
- [Script Reference](SCRIPT_REFERENCE.md) - Script documentation
- [Data Formats](DATA_FORMATS.md) - Data structure specifications
- [Development Guide](DEVELOPMENT.md) - Contributing and development
