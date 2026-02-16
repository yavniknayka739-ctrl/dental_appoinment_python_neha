---
description: How to push code to GitHub using Git commands
---

# Git Push Workflow

Simple workflow to push local changes to GitHub repository using standard Git commands.

---

## Prerequisites

- Git installed on your system
- GitHub repository already initialized
- Remote origin configured

---

## Quick Push (Most Common)

```powershell
# Navigate to project directory
cd c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha

# Add all changes
git add .

# Commit with message
git commit -m "Your commit message here"

# Push to GitHub
git push origin main
```

---

## Step-by-Step Commands

### 1. Check Status
```powershell
// turbo
git status
```
Shows which files have been modified, added, or deleted.

### 2. Add Files
```powershell
// turbo
# Add all files
git add .

# Or add specific files
git add notes/project_flow.md
git add notes/project_theory.md
git add .agent/workflows/github-workflow.md
```

### 3. Commit Changes
```powershell
// turbo
git commit -m "Add project documentation and workflows"
```

### 4. Push to GitHub
```powershell
// turbo
git push origin main
```

---

## Common Scenarios

### Scenario A: Push All New Documentation
```powershell
// turbo-all
cd c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha
git add notes/*.md
git add .agent/workflows/*.md
git commit -m "Add comprehensive project documentation"
git push origin main
```

### Scenario B: Push Code Changes
```powershell
// turbo-all
cd c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha
git add scripts/*.py
git commit -m "Update scripts with interactive chart windows"
git push origin main
```

### Scenario C: Push Everything
```powershell
// turbo-all
cd c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha
git add .
git commit -m "Update project with latest changes"
git push origin main
```

---

## Useful Git Commands

### View Commit History
```powershell
// turbo
git log --oneline -10
```

### View Differences
```powershell
// turbo
git diff
```

### Undo Last Commit (Keep Changes)
```powershell
git reset --soft HEAD~1
```

### Pull Latest Changes
```powershell
// turbo
git pull origin main
```

### Check Remote URL
```powershell
// turbo
git remote -v
```

---

## Troubleshooting

### Error: "fatal: not a git repository"
**Solution:** Initialize Git first
```powershell
git init
git remote add origin https://github.com/yavniknayka739-ctrl/dental_appoinment_python_neha.git
```

### Error: "Updates were rejected"
**Solution:** Pull first, then push
```powershell
git pull origin main --rebase
git push origin main
```

### Error: "Authentication failed"
**Solution:** Use GitHub Personal Access Token or SSH key

---

## Best Practices

1. **Always check status first:** `git status`
2. **Write descriptive commit messages:** Be specific about what changed
3. **Commit related changes together:** Don't mix unrelated changes
4. **Pull before push:** Avoid merge conflicts
5. **Use .gitignore:** Exclude unnecessary files (venv, __pycache__, etc.)

---

## Project-Specific Info

**Repository:** https://github.com/yavniknayka739-ctrl/dental_appoinment_python_neha
**Default Branch:** main
**Project Path:** c:\Users\yavni\OneDrive\Desktop\python\projects\dental_appoinment_python_neha
