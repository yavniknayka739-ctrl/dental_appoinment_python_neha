---
description: How to push code to GitHub using Git commands
---

# Git Push Workflow

Push local changes to GitHub using standard Git commands in PowerShell.
**ALWAYS use Git CLI commands instead of MCP tools** — it's faster, pushes all files at once, and avoids one-file-at-a-time inefficiency.

---

## Repository Info

- **Repo:** https://github.com/yavniknayka739-ctrl/dental_appoinment_python_neha
- **Branch:** main
- **Local Path:** c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha

---

## Quick Push (Most Common)

// turbo-all
```powershell
cd c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha
git add .
git commit -m "Your commit message here"
git push origin main
```

---

## Before You Push: Pre-Flight Checks

// turbo-all
```powershell
# 1. Check which files have changed
git status

# 2. Check current branch
git branch

# 3. Verify remote URL is correct
git remote -v
```

**Expected remote URL:**
```
origin  https://github.com/yavniknayka739-ctrl/dental_appoinment_python_neha.git (push)
```

> **WARNING:** If remote URL shows a different account or has no token, fix it FIRST (see Troubleshooting section below).

---

## Compare Local vs GitHub (Before or After Push)

// turbo-all
```powershell
# Fetch latest from GitHub without merging
git fetch origin main

# Compare local HEAD with remote — shows file-level diff summary
git diff HEAD origin/main --stat

# If output is EMPTY = local and remote are identical (fully synced)
# If output shows files = those files differ between local and remote
```

**Detailed comparison (line-by-line diff):**
```powershell
git diff HEAD origin/main
```

**Verify both point to same commit:**
```powershell
git log --oneline -3 --all --decorate
```
Look for `(HEAD -> main, origin/main)` on the same commit.

---

## Full Step-by-Step Push

### Step 1: Check Status
// turbo
```powershell
git status
```

### Step 2: Stage Files
// turbo
```powershell
# Add ALL changed files
git add .

# Or add specific files only
git add scripts/main.py scripts/eda_analysis.py notes/project_theory.md
```

### Step 3: Commit
// turbo
```powershell
git commit -m "Describe what changed and why"
```

### Step 4: Push
// turbo
```powershell
git push origin main
```

---

## Troubleshooting

### ERROR: "Permission denied to [wrong_username]"
```
remote: Permission to yavniknayka739-ctrl/dental_appoinment_python_neha.git denied to ankitnayka.
fatal: unable to access '...': The requested URL returned error: 403
```

**Cause:** Git is using cached credentials from a different GitHub account.

**Fix:** Update remote URL with a Personal Access Token:
```powershell
git remote set-url origin https://YOUR_GITHUB_TOKEN@github.com/yavniknayka739-ctrl/dental_appoinment_python_neha.git
```

Then retry:
```powershell
git push origin main
```

**To generate a token:** Go to https://github.com/settings/tokens → Generate new token (classic) → Select **repo** scope → Copy token immediately.

---

### ERROR: "Updates were rejected (fetch first)"
```
! [rejected]  main -> main (fetch first)
error: failed to push some refs
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**Cause:** GitHub has commits that your local repo doesn't have (e.g., files pushed via MCP or GitHub web interface).

**Fix Option A — Pull & Merge (safe, preserves both):**
```powershell
git pull origin main --rebase
# If conflicts appear, resolve them, then:
git add .
git rebase --continue
git push origin main
```

**Fix Option B — Force Push (overwrites remote with local):**
```powershell
git push origin main --force
```

> **CAUTION:** Force push overwrites the remote. Only use when you're SURE your local code is the correct/latest version.

---

### ERROR: Merge Conflicts During Rebase
```
CONFLICT (add/add): Merge conflict in some_file.md
error: could not apply ...
```

**Cause:** Same file was modified both locally and on GitHub differently.

**Fix Option A — Abort rebase and force push:**
```powershell
git rebase --abort
git push origin main --force
```

**Fix Option B — Resolve conflicts manually:**
1. Open conflicted files, look for `<<<<<<<`, `=======`, `>>>>>>>` markers
2. Edit files to keep the correct version
3. Then:
```powershell
git add .
git rebase --continue
git push origin main
```

---

### ERROR: "Everything up-to-date" but Files Missing on GitHub
**Cause:** Files were never committed locally — they exist on disk but Git doesn't know about them.

**Fix:**
```powershell
git add .
git status  # Verify files are staged
git commit -m "Add missing files"
git push origin main
```

---

## Useful Commands Reference

| Command | Purpose |
|---------|---------|
| `git status` | See changed/staged/untracked files |
| `git diff --stat HEAD origin/main` | Compare local vs remote (file summary) |
| `git log --oneline -5` | View recent commits |
| `git remote -v` | Check remote URL |
| `git fetch origin main` | Download remote info without merging |
| `git pull origin main` | Download and merge remote changes |
| `git push origin main` | Upload local commits to GitHub |
| `git push origin main --force` | Overwrite remote with local |
| `git rebase --abort` | Cancel a failed rebase |

---

## Key Lessons (From Real Experience)

1. **Use Git CLI, NOT MCP tools** for pushing code — MCP pushes one file at a time, Git pushes everything in one commit
2. **Always check `git remote -v`** before pushing — wrong cached credentials will cause 403 errors
3. **If you pushed files via MCP earlier**, your local Git won't know about those commits — use `git push --force` to overwrite
4. **Always run `git status` first** to see what's actually staged
5. **After pushing, verify with `git diff HEAD origin/main --stat`** — empty output = fully synced
6. **Write descriptive commit messages** — "Update scripts" is bad, "Remove emojis and add interactive charts" is good
