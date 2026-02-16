---
description: How to interact with GitHub using MCP for this project
---

# GitHub MCP Workflow

Guide for AI agents on interacting with GitHub for the dental appointment project.

---

## CRITICAL RULE: When to Use MCP vs Git CLI

> **For PUSHING code: ALWAYS use Git CLI commands (see /git-push workflow)**
> MCP tools push files one at a time via API, which is slow and error-prone.
> Git CLI pushes ALL files in a single commit instantly.

> **For READING/QUERYING: Use MCP tools**
> MCP is great for viewing files on GitHub, listing commits, creating issues/PRs, etc.

| Task | Use This |
|------|----------|
| Push code to GitHub | **Git CLI** (`git add . && git commit && git push`) |
| View file on GitHub | MCP: `mcp_github_get_file_contents` |
| List commits | MCP: `mcp_github_list_commits` |
| Create issue | MCP: `mcp_github_create_issue` |
| Create PR | MCP: `mcp_github_create_pull_request` |
| Compare local vs remote | **Git CLI** (`git diff HEAD origin/main --stat`) |

---

## Repository Info

- **Owner:** `yavniknayka739-ctrl`
- **Repo:** `dental_appoinment_python_neha`
- **Branch:** `main`
- **Local Path:** `c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha`

---

## Reading & Querying (Use MCP)

### View File Contents
```
mcp_github_get_file_contents(
  owner: yavniknayka739-ctrl
  repo: dental_appoinment_python_neha
  path: "README.md"
)
```

### List Recent Commits
```
mcp_github_list_commits(
  owner: yavniknayka739-ctrl
  repo: dental_appoinment_python_neha
  perPage: 5
)
```

### View Directory Structure
```
mcp_github_get_file_contents(
  owner: yavniknayka739-ctrl
  repo: dental_appoinment_python_neha
  path: "scripts"
)
```

---

## Creating Issues
```
mcp_github_create_issue(
  owner: yavniknayka739-ctrl
  repo: dental_appoinment_python_neha
  title: "Add data validation for patient age"
  body: "## Description\nValidate patient age is between 1-120\n\n## Acceptance Criteria\n- Reject ages outside range\n- Log warning"
  labels: ["enhancement"]
)
```

---

## Creating Branches
```
mcp_github_create_branch(
  owner: yavniknayka739-ctrl
  repo: dental_appoinment_python_neha
  branch: "feature/add-validation"
  from_branch: "main"
)
```

**Branch naming:** Use prefixes like `feature/`, `fix/`, `docs/`, `refactor/`

---

## Pull Requests

### Create PR
```
mcp_github_create_pull_request(
  owner: yavniknayka739-ctrl
  repo: dental_appoinment_python_neha
  title: "Add interactive matplotlib charts"
  head: "feature/interactive-charts"
  base: "main"
  body: "## Changes\n- Added plt.show(block=False) to all charts"
)
```

### List PRs
```
mcp_github_list_pull_requests(
  owner: yavniknayka739-ctrl
  repo: dental_appoinment_python_neha
  state: "open"
)
```

### Merge PR
```
mcp_github_merge_pull_request(
  owner: yavniknayka739-ctrl
  repo: dental_appoinment_python_neha
  pull_number: 5
  merge_method: "squash"
)
```

---

## Common Workflows

### Workflow A: Push All Local Changes to GitHub
**Use Git CLI, not MCP!** Follow the `/git-push` workflow:
```powershell
cd c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha
git add .
git commit -m "Describe changes here"
git push origin main
```

### Workflow B: Verify Local is Synced with GitHub
```powershell
git fetch origin main
git diff HEAD origin/main --stat
# Empty output = fully synced
```

### Workflow C: Update README on GitHub
Option 1 (Git CLI — recommended):
```powershell
# Edit README.md locally, then:
git add README.md
git commit -m "Update README with current project state"
git push origin main
```

Option 2 (MCP — only if editing directly on GitHub):
```
# Step 1: Get current SHA
mcp_github_get_file_contents(owner, repo, path: "README.md")
# Step 2: Update with SHA
mcp_github_create_or_update_file(
  owner, repo, path: "README.md",
  content: "new content",
  message: "Update README",
  branch: "main",
  sha: <sha_from_step_1>
)
```

> **WARNING:** If you use MCP to push files, those commits won't exist in local Git history. This causes "fetch first" errors on the next `git push`. Fix with `git push --force`.

---

## Troubleshooting

### "Permission denied to [wrong_username]" (403)
**Cause:** Git credentials cached from wrong GitHub account.
**Fix:** Update remote URL with token:
```powershell
git remote set-url origin https://YOUR_TOKEN@github.com/yavniknayka739-ctrl/dental_appoinment_python_neha.git
```

### "Updates were rejected (fetch first)"
**Cause:** GitHub has commits not in local (often from MCP pushes).
**Fix:**
```powershell
git push origin main --force
```

### Merge Conflicts During Pull/Rebase
**Quick fix:** Abort and force push:
```powershell
git rebase --abort
git push origin main --force
```

### MCP Push Only Shows One File on GitHub
**Cause:** MCP `push_files` tool may silently fail on some files.
**Fix:** Use Git CLI instead. It's reliable and pushes everything.

---

## Key Lessons Learned

1. **Git CLI > MCP for pushing** — MCP is slow, unreliable for multi-file pushes
2. **Check `git remote -v` before pushing** — wrong credentials = 403 error
3. **MCP pushes create orphan commits** — local Git won't know about them, causing sync issues
4. **Always verify after push** — run `git diff HEAD origin/main --stat` to confirm sync
5. **Force push when MCP and Git conflict** — `git push --force` resolves diverged histories
6. **Use MCP for reading, Git CLI for writing** — best of both worlds
