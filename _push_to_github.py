"""
Helper script to push project files to GitHub using the GitHub API.
This is a one-time use script that can be deleted after pushing.
"""
import os
import sys
import json
import base64
import urllib.request
import urllib.error

# Configuration
OWNER = "yavniknayka739-ctrl"
REPO = "dental_appoinment_python_neha"
BRANCH = "main"

# Files to push (relative paths)
FILES_TO_PUSH = [
    "scripts/data_cleaning.py",
    "scripts/eda_analysis.py",
    "scripts/ml_model.py",
    "scripts/main.py",
    "data/dental_appointments_raw.csv",
    "data/dental_appointments_cleaned.csv",
    "notes/how_to_run.md",
    "notes/ssot.yaml",
    "notes/generate_data.py",
]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_token():
    """Try to find the GitHub token from environment or git config."""
    # Try environment variable
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    
    # Try gh CLI
    try:
        import subprocess
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    
    return None

def push_file(token, filepath, message):
    """Push a single file to GitHub."""
    full_path = os.path.join(PROJECT_ROOT, filepath.replace("/", os.sep))
    
    if not os.path.exists(full_path):
        print(f"  SKIP: {filepath} (file not found)")
        return False
    
    # Read file content
    with open(full_path, "rb") as f:
        content = f.read()
    
    # Base64 encode
    encoded = base64.b64encode(content).decode("utf-8")
    
    # GitHub API request
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{filepath}"
    
    data = json.dumps({
        "message": message,
        "content": encoded,
        "branch": BRANCH,
    }).encode("utf-8")
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "dental-project-pusher",
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
    
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode("utf-8"))
        sha = result.get("content", {}).get("sha", "unknown")
        print(f"  OK: {filepath} (sha: {sha[:8]})")
        return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"  FAIL: {filepath} - {e.code}: {error_body[:200]}")
        return False

def main():
    token = get_token()
    if not token:
        print("ERROR: No GitHub token found!")
        print("Set GITHUB_TOKEN environment variable or install gh CLI")
        sys.exit(1)
    
    print(f"Pushing files to {OWNER}/{REPO} (branch: {BRANCH})")
    print(f"Token found: {token[:8]}...")
    print()
    
    success = 0
    fail = 0
    
    for filepath in FILES_TO_PUSH:
        basename = os.path.basename(filepath)
        message = f"Add {basename}"
        
        if push_file(token, filepath, message):
            success += 1
        else:
            fail += 1
    
    print(f"\nDone! {success} succeeded, {fail} failed")

if __name__ == "__main__":
    main()
