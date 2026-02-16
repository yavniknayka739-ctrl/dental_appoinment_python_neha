---
description: How to interact with GitHub using MCP for this project
---

# GitHub MCP Workflow

This workflow guides AI agents on how to interact with GitHub using the GitHub MCP (Model Context Protocol) server for the dental appointment project.

---

## Project Repository Information

**Owner:** `yavniknayka739-ctrl`  
**Repository:** `dental_appoinment_python_neha`  
**Default Branch:** `main` (or `master` - check first)

---

## Common GitHub Operations

### 1. Getting Repository Information

**Goal:** View files and understand repository structure

**Tool:** `mcp_github_get_file_contents`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `path`: Path to file (e.g., "README.md", "scripts/main.py")
- `branch`: (optional) Specify branch, defaults to main

**Example:**
```
Get README:
  owner: yavniknayka739-ctrl
  repo: dental_appoinment_python_neha
  path: README.md
```

---

### 2. Pushing Single File to GitHub

**Goal:** Update or create a single file on GitHub

**Tool:** `mcp_github_create_or_update_file`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `path`: File path in repo (e.g., "scripts/main.py")
- `content`: Full file content (as string)
- `message`: Commit message (descriptive)
- `branch`: Branch name (usually "main")
- `sha`: (required for updates) Get from viewing file first

**Steps:**
1. If updating existing file, first get current file to obtain SHA
2. Prepare file content
3. Write descriptive commit message
4. Push file with all parameters

**Example - Creating New File:**
```
owner: yavniknayka739-ctrl
repo: dental_appoinment_python_neha
path: notes/new_documentation.md
content: "# New Documentation\n\nContent here..."
message: "Add new documentation file"
branch: main
```

**Example - Updating Existing File:**
```
Step 1: Get current file
  mcp_github_get_file_contents(owner, repo, path: "README.md")
  → Returns: content + sha

Step 2: Update file
  mcp_github_create_or_update_file(
    owner: yavniknayka739-ctrl
    repo: dental_appoinment_python_neha
    path: README.md
    content: "Updated content..."
    message: "Update README with new instructions"
    branch: main
    sha: <sha_from_step_1>
  )
```

---

### 3. Pushing Multiple Files at Once

**Goal:** Push multiple files in a single commit

**Tool:** `mcp_github_push_files`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `branch`: Branch name
- `files`: Array of {path, content} objects
- `message`: Commit message for all files

**Example:**
```
owner: yavniknayka739-ctrl
repo: dental_appoinment_python_neha
branch: main
message: "Update documentation and add new workflow"
files: [
  {
    path: "notes/project_flow.md",
    content: "# Project Flow\n..."
  },
  {
    path: "notes/project_theory.md",
    content: "# Project Theory\n..."
  },
  {
    path: ".agent/workflows/github-workflow.md",
    content: "# GitHub Workflow\n..."
  }
]
```

**When to Use:**
- Pushing multiple related files
- More efficient than individual file pushes
- Creates single commit for all changes

---

### 4. Creating a New Branch

**Goal:** Create a feature branch for development

**Tool:** `mcp_github_create_branch`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `branch`: New branch name (e.g., "feature/interactive-charts")
- `from_branch`: (optional) Source branch, defaults to main

**Example:**
```
owner: yavniknayka739-ctrl
repo: dental_appoinment_python_neha
branch: feature/add-documentation
from_branch: main
```

**Best Practices:**
- Use descriptive branch names
- Prefix with type: `feature/`, `fix/`, `docs/`, `refactor/`
- Keep branch names lowercase with hyphens

---

### 5. Viewing Commit History

**Goal:** See recent commits

**Tool:** `mcp_github_list_commits`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `sha`: (optional) Branch or commit SHA
- `page`: (optional) Page number for pagination
- `perPage`: (optional) Results per page (default 30)

**Example:**
```
owner: yavniknayka739-ctrl
repo: dental_appoinment_python_neha
perPage: 10
```

---

### 6. Creating a Pull Request

**Goal:** Create PR to merge changes

**Tool:** `mcp_github_create_pull_request`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `title`: PR title (descriptive)
- `head`: Source branch (your changes)
- `base`: Target branch (usually "main")
- `body`: (optional) PR description
- `draft`: (optional) true for draft PR

**Example:**
```
owner: yavniknayka739-ctrl
repo: dental_appoinment_python_neha
title: "Add interactive matplotlib charts"
head: feature/interactive-charts
base: main
body: "## Changes\n- Added plt.show(block=False) to all charts\n- Charts now open in non-blocking mode"
```

---

### 7. Listing Pull Requests

**Goal:** View open/closed PRs

**Tool:** `mcp_github_list_pull_requests`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `state`: "open", "closed", or "all"
- `sort`: "created", "updated", "popularity"
- `direction`: "asc" or "desc"

**Example:**
```
owner: yavniknayka739-ctrl
repo: dental_appoinment_python_neha
state: open
```

---

### 8. Merging a Pull Request

**Goal:** Merge approved PR

**Tool:** `mcp_github_merge_pull_request`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `pull_number`: PR number
- `merge_method`: "merge", "squash", or "rebase"
- `commit_title`: (optional) Custom merge commit title
- `commit_message`: (optional) Additional message

**Example:**
```
owner: yavniknayka739-ctrl
repo: dental_appoinment_python_neha
pull_number: 5
merge_method: squash
commit_title: "Add interactive charts feature"
```

---

### 9. Creating an Issue

**Goal:** Report bug or request feature

**Tool:** `mcp_github_create_issue`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `title`: Issue title
- `body`: (optional) Issue description
- `labels`: (optional) Array of label names
- `assignees`: (optional) Array of usernames

**Example:**
```
owner: yavniknayka739-ctrl
repo: dental_appoinment_python_neha
title: "Add data validation for patient age"
body: "## Description\nNeed to validate patient age is within reasonable range\n\n## Acceptance Criteria\n- Age between 1-120\n- Display error for invalid ages"
labels: ["enhancement", "data-validation"]
```

---

### 10. Listing Issues

**Goal:** View project issues

**Tool:** `mcp_github_list_issues`

**Parameters:**
- `owner`: yavniknayka739-ctrl
- `repo`: dental_appoinment_python_neha
- `state`: "open", "closed", or "all"
- `labels`: (optional) Filter by labels
- `sort`: "created", "updated", "comments"

**Example:**
```
owner: yavniknayka739-ctrl
repo: dental_appoinment_python_neha
state: open
sort: updated
```

---

## Common Workflows

### Workflow A: Push Local Documentation to GitHub

**Scenario:** You created new .md files locally and want to push them to GitHub

**Steps:**
1. Identify files to push (e.g., project_flow.md, project_theory.md)
2. Read local file contents
3. Use `mcp_github_push_files` to push all at once
4. Verify files appear on GitHub

**Example:**
```
// turbo
1. Read local files:
   - c:\...\notes\project_flow.md
   - c:\...\notes\project_theory.md

2. Push to GitHub:
   mcp_github_push_files(
     owner: yavniknayka739-ctrl
     repo: dental_appoinment_python_neha
     branch: main
     message: "Add project documentation (flow and theory)"
     files: [
       {path: "notes/project_flow.md", content: <file1_content>},
       {path: "notes/project_theory.md", content: <file2_content>}
     ]
   )
```

---

### Workflow B: Create Feature Branch and Push Changes

**Scenario:** Working on a new feature, want to use proper Git workflow

**Steps:**
1. Create feature branch
2. Push changes to feature branch
3. Create pull request
4. Review and merge

**Example:**
```
1. Create branch:
   mcp_github_create_branch(
     owner: yavniknayka739-ctrl
     repo: dental_appoinment_python_neha
     branch: feature/add-workflows
     from_branch: main
   )

2. Push files to feature branch:
   mcp_github_push_files(
     branch: feature/add-workflows
     message: "Add GitHub workflow documentation"
     files: [...]
   )

3. Create PR:
   mcp_github_create_pull_request(
     title: "Add GitHub workflow documentation"
     head: feature/add-workflows
     base: main
     body: "Adds workflow guide for GitHub MCP operations"
   )

4. Merge PR:
   mcp_github_merge_pull_request(
     pull_number: <pr_number>
     merge_method: squash
   )
```

---

### Workflow C: Update README

**Scenario:** Need to update project README

**Steps:**
1. Get current README to obtain SHA
2. Modify content
3. Push updated README

**Example:**
```
1. Get current README:
   mcp_github_get_file_contents(
     owner: yavniknayka739-ctrl
     repo: dental_appoinment_python_neha
     path: README.md
   )
   → Save the SHA

2. Update README:
   mcp_github_create_or_update_file(
     owner: yavniknayka739-ctrl
     repo: dental_appoinment_python_neha
     path: README.md
     content: <updated_content>
     message: "Update README with new features"
     branch: main
     sha: <sha_from_step_1>
   )
```

---

### Workflow D: Sync Local Changes to GitHub

**Scenario:** Multiple files changed locally, push all to GitHub

**Steps:**
1. Identify all changed files
2. Read their contents
3. Push all files in single commit

**Example:**
```
// turbo
1. Changed files:
   - scripts/main.py
   - scripts/eda_analysis.py
   - scripts/ml_model.py

2. Push all:
   mcp_github_push_files(
     owner: yavniknayka739-ctrl
     repo: dental_appoinment_python_neha
     branch: main
     message: "Add interactive matplotlib windows to all charts"
     files: [
       {path: "scripts/main.py", content: <content1>},
       {path: "scripts/eda_analysis.py", content: <content2>},
       {path: "scripts/ml_model.py", content: <content3>}
     ]
   )
```

---

## Best Practices

### Commit Messages
- Use descriptive, present-tense messages
- Good: "Add interactive chart windows"
- Bad: "changes", "update", "fix"

### Branch Naming
- Use prefixes: `feature/`, `fix/`, `docs/`, `refactor/`
- Use hyphens, not spaces or underscores
- Keep lowercase
- Example: `feature/interactive-charts`

### Pull Requests
- Write clear titles and descriptions
- Reference related issues
- Use draft PRs for work-in-progress
- Request reviews when ready

### File Operations
- Always get SHA before updating existing files
- Use `push_files` for multiple files (more efficient)
- Verify file paths match repository structure

---

## Troubleshooting

### Error: "Not Found"
- **Cause:** Wrong owner, repo, or file path
- **Solution:** Verify repository information and file paths

### Error: "SHA required"
- **Cause:** Trying to update existing file without SHA
- **Solution:** First get file contents to obtain SHA

### Error: "Reference already exists"
- **Cause:** Branch name already exists
- **Solution:** Use different branch name or delete old branch

### Error: "Validation Failed"
- **Cause:** Missing required parameters or invalid values
- **Solution:** Check all required parameters are provided

### No Output After Push
- **Cause:** MCP operations may not show immediate feedback
- **Solution:** Use `mcp_github_get_file_contents` to verify file was pushed

---

## Quick Reference

**View File:**
```
mcp_github_get_file_contents(owner, repo, path)
```

**Create/Update Single File:**
```
mcp_github_create_or_update_file(owner, repo, path, content, message, branch, sha?)
```

**Push Multiple Files:**
```
mcp_github_push_files(owner, repo, branch, files, message)
```

**Create Branch:**
```
mcp_github_create_branch(owner, repo, branch, from_branch?)
```

**Create PR:**
```
mcp_github_create_pull_request(owner, repo, title, head, base, body?)
```

**Create Issue:**
```
mcp_github_create_issue(owner, repo, title, body?, labels?)
```

---

## Repository Constants

For this project, always use:
- **owner:** `yavniknayka739-ctrl`
- **repo:** `dental_appoinment_python_neha`
- **default branch:** `main` (verify first)
