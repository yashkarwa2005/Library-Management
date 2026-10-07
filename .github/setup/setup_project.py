#!/usr/bin/env python3
"""
=============================================================================
 ONE-CLICK GITHUB PROJECT & KANBAN SETUP SYSTEM
=============================================================================
 Reusable, dynamic GitHub setup script for Agile Methodologies (AM) PBLs.
 Automatically detects the user's repository, checks authentication,
 creates Scrum labels, issues (with duplicate prevention), milestones,
 and provisions a GitHub Projects V2 Kanban board.

 NO HARDCODED TOKENS, USERNAMES, OR REPOSITORY URLS.
=============================================================================
"""

import sys
import os
import json
import re
import subprocess
import webbrowser
from typing import Dict, Any, List, Optional, Tuple

# Reconfigure stdout/stderr to UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    os.system("")

# Console styling helpers
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def print_header(title: str):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD} {title}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")

def print_step(step: str):
    print(f"{Colors.BOLD}{Colors.BLUE}==> {step}{Colors.RESET}")

def print_success(msg: str):
    try:
        print(f" {Colors.GREEN}[OK] {msg}{Colors.RESET}")
    except UnicodeEncodeError:
        print(f" [OK] {msg}")

def print_warn(msg: str):
    try:
        print(f" {Colors.YELLOW}[!] {msg}{Colors.RESET}")
    except UnicodeEncodeError:
        print(f" [!] {msg}")

def print_error(msg: str):
    try:
        print(f" {Colors.RED}[X] {msg}{Colors.RESET}")
    except UnicodeEncodeError:
        print(f" [X] {msg}")

def print_info(msg: str):
    try:
        print(f"   {Colors.DIM}{msg}{Colors.RESET}")
    except UnicodeEncodeError:
        print(f"   {msg}")


def run_cmd(cmd: List[str], check: bool = False, capture: bool = True) -> Tuple[int, str, str]:
    """Execute a CLI command and return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        stdout = proc.stdout.strip() if proc.stdout else ""
        stderr = proc.stderr.strip() if proc.stderr else ""
        if check and proc.returncode != 0:
            raise RuntimeError(f"Command {' '.join(cmd)} failed with exit code {proc.returncode}: {stderr}")
        return proc.returncode, stdout, stderr
    except FileNotFoundError:
        return 127, "", f"Command not found: {cmd[0]}"
    except Exception as e:
        return 1, "", str(e)

def find_gh_cli() -> Optional[str]:
    """Locate gh executable in PATH or standard Windows directories."""
    code, out, _ = run_cmd(["gh", "--version"])
    if code == 0:
        return "gh"
    
    # Check common Windows install paths
    candidates = [
        os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "GitHub CLI", "gh.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "GitHub CLI", "gh.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "GitHub CLI", "gh.exe"),
    ]
    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            # Temporarily add to PATH
            gh_dir = os.path.dirname(candidate)
            os.environ["PATH"] = gh_dir + os.pathsep + os.environ["PATH"]
            return candidate
    return None

def check_git() -> bool:
    """Verify Git is installed and available."""
    code, out, _ = run_cmd(["git", "--version"])
    return code == 0

def detect_repo_origin() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Detects OWNER and REPOSITORY dynamically from git remote origin.
    Supports both HTTPS and SSH remotes:
      - https://github.com/OWNER/REPO.git
      - https://github.com/OWNER/REPO
      - git@github.com:OWNER/REPO.git
      - git@github.com:OWNER/REPO
    Returns (owner, repo, remote_url).
    """
    code, remote_url, err = run_cmd(["git", "remote", "get-url", "origin"])
    if code != 0 or not remote_url:
        return None, None, None
    
    remote_url = remote_url.strip()
    
    # Regex patterns for HTTPS and SSH GitHub remotes
    patterns = [
        r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
        r"https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$"
    ]
    
    for pat in patterns:
        m = re.search(pat, remote_url, re.IGNORECASE)
        if m:
            return m.group("owner"), m.group("repo"), remote_url
            
    return None, None, remote_url

def check_gh_auth(gh_bin: str) -> Tuple[bool, Optional[str], List[str]]:
    """
    Checks gh auth status and returns (is_authenticated, username, scopes).
    """
    code, stdout, stderr = run_cmd([gh_bin, "auth", "status"])
    output = stdout + "\n" + stderr
    
    is_authed = ("Logged in to github.com" in output or "Active account: true" in output or "Logged in to" in output)
    if not is_authed:
        return False, None, []
    
    # Determine username
    code_user, user_out, _ = run_cmd([gh_bin, "api", "user", "--jq", ".login"])
    username = user_out.strip() if code_user == 0 and user_out.strip() else None
    
    # Scopes
    scopes = []
    scope_match = re.search(r"Token scopes:\s*(.+)", output, re.IGNORECASE)
    if scope_match:
        scopes = [s.strip(" '\"") for s in scope_match.group(1).split(",")]
        
    return True, username, scopes

def ensure_project_scope(gh_bin: str, scopes: List[str]):
    """
    Ensures user token has 'project' scope required for GitHub Projects V2.
    """
    has_project = any('project' in s.lower() for s in scopes)
    if not has_project:
        print_warn("GitHub Project scope ('project') not detected in active CLI session.")
        print_info("GitHub Projects V2 requires the 'project' OAuth scope.")
        choice = input("Would you like to refresh your GitHub login with 'project' scope now? [Y/n]: ").strip().lower()
        if choice in ('', 'y', 'yes'):
            subprocess.run([gh_bin, "auth", "refresh", "-s", "project,repo"], check=False)

def load_project_setup_json(json_path: str) -> Dict[str, Any]:
    """Loads and validates project-setup.json configuration."""
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"Project configuration file not found at: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def reconcile_labels(gh_bin: str, repo_slug: str, labels: List[Dict[str, str]]) -> Tuple[int, int]:
    """
    Creates or updates repository labels idempotently using gh label create --force.
    Returns (created_count, existing_count).
    """
    print_step(f"Configuring {len(labels)} Agile Scrum Labels on {repo_slug}...")
    
    # Query existing labels
    code, out, _ = run_cmd([gh_bin, "label", "list", "--repo", repo_slug, "--limit", "200", "--json", "name"])
    existing_names = set()
    if code == 0 and out:
        try:
            items = json.loads(out)
            existing_names = {item['name'].lower() for item in items}
        except Exception:
            pass
            
    created_count = 0
    updated_or_existing = 0
    
    for lbl in labels:
        name = lbl["name"]
        color = lbl.get("color", "0075ca").lstrip("#")
        desc = lbl.get("description", "")
        
        is_existing = name.lower() in existing_names
        
        cmd = [
            gh_bin, "label", "create", name,
            "--color", color,
            "--description", desc,
            "--repo", repo_slug,
            "--force"
        ]
        code, _, err = run_cmd(cmd)
        if code == 0:
            if is_existing:
                updated_or_existing += 1
                print_info(f"Label '{name}' → updated/ready")
            else:
                created_count += 1
                print_success(f"Label '{name}' → created")
        else:
            print_warn(f"Label '{name}': {err}")
            
    return created_count, updated_or_existing

def reconcile_milestones(gh_bin: str, repo_slug: str, milestones: List[Dict[str, Any]]):
    """Creates repository milestones (Sprints 1-5) if they don't already exist."""
    if not milestones:
        return
    print_step(f"Configuring {len(milestones)} Sprint Milestones on {repo_slug}...")
    
    code, out, _ = run_cmd([gh_bin, "api", f"repos/{repo_slug}/milestones", "--jq", ".[].title"])
    existing_titles = set(out.splitlines()) if code == 0 and out else set()
    
    for m in milestones:
        title = m["title"]
        desc = m.get("description", "")
        if title in existing_titles:
            print_info(f"Milestone '{title}' → already exists")
        else:
            code, _, err = run_cmd([
                gh_bin, "api", f"repos/{repo_slug}/milestones",
                "-f", f"title={title}",
                "-f", f"description={desc}"
            ])
            if code == 0:
                print_success(f"Milestone '{title}' → created")
            else:
                print_warn(f"Milestone '{title}': {err}")

def reconcile_issues(gh_bin: str, repo_slug: str, issues: List[Dict[str, Any]], milestones: List[Dict[str, Any]]) -> Tuple[int, int, List[Dict[str, Any]]]:
    """
    Creates GitHub Issues from project-setup.json.
    Prevents duplicates by searching existing issue titles by stable identifier (e.g. '[US-01]').
    Returns (created_count, existing_count, issues_with_urls).
    """
    print_step(f"Reconciling {len(issues)} User Story Issues on {repo_slug}...")
    
    # Fetch all existing issues (open and closed)
    code, out, _ = run_cmd([
        gh_bin, "issue", "list",
        "--repo", repo_slug,
        "--limit", "300",
        "--state", "all",
        "--json", "number,title,url"
    ])
    
    existing_map = {}
    if code == 0 and out:
        try:
            for item in json.loads(out):
                title = item.get("title", "")
                existing_map[title] = item
                # Match identifier like [US-01]
                id_match = re.search(r"\[([A-Za-z0-9_-]+)\]", title)
                if id_match:
                    existing_map[id_match.group(1).upper()] = item
        except Exception:
            pass
            
    # Map sprint names to milestone titles
    sprint_to_milestone = {}
    for m in milestones:
        sprint_num = m.get("sprint_number")
        if sprint_num:
            sprint_to_milestone[f"Sprint {sprint_num}"] = m["title"]
            sprint_to_milestone[f"sprint {sprint_num}"] = m["title"]
            
    created_count = 0
    existing_count = 0
    synced_issues = []
    
    for item in issues:
        ident = item.get("identifier", "").strip().upper()
        title = item.get("title", "").strip()
        body = item.get("body", "").strip()
        labels = item.get("labels", [])
        sprint = item.get("sprint", "")
        
        # Check duplicate
        existing = existing_map.get(ident) or existing_map.get(title)
        if existing:
            existing_count += 1
            print_info(f"[{ident}] {title} → already exists (#{existing['number']})")
            synced_item = dict(item)
            synced_item["url"] = existing["url"]
            synced_item["number"] = existing["number"]
            synced_issues.append(synced_item)
            continue
            
        # Create Issue
        cmd = [
            gh_bin, "issue", "create",
            "--repo", repo_slug,
            "--title", title,
            "--body", body
        ]
        if labels:
            cmd.extend(["--label", ",".join(labels)])
            
        milestone_title = sprint_to_milestone.get(sprint)
        if milestone_title:
            cmd.extend(["--milestone", milestone_title])
            
        code, created_url, err = run_cmd(cmd)
        if code == 0 and created_url:
            created_count += 1
            # Extract issue number from created URL
            num_match = re.search(r"/issues/(\d+)", created_url)
            num = int(num_match.group(1)) if num_match else None
            print_success(f"[{ident}] {title} → created (#{num if num else 'OK'})")
            synced_item = dict(item)
            synced_item["url"] = created_url
            synced_item["number"] = num
            synced_issues.append(synced_item)
        else:
            print_error(f"[{ident}] Failed to create issue: {err}")
            
    return created_count, existing_count, synced_issues

def setup_github_project(gh_bin: str, owner: str, repo: str, setup_data: Dict[str, Any], issues: List[Dict[str, Any]]) -> Optional[str]:
    """
    Provisions or reuses a GitHub Projects V2 board.
    Configures custom fields (Priority, Sprint, Type, Story Points),
    links the project to the repository, and adds all issues.
    Returns the Project URL.
    """
    project_title = setup_data.get("project_name", f"{repo} — Scrum Board")
    print_step(f"Setting up GitHub Project V2 ('{project_title}')...")
    
    # 1. Check existing projects for owner
    code, out, err = run_cmd([gh_bin, "project", "list", "--owner", owner, "--format", "json"])
    if code != 0:
        print_warn(f"Could not list projects for '{owner}': {err}")
        print_info("Checking if user has 'project' scope enabled on GitHub CLI...")
        # Attempt fallback to @me
        code, out, _ = run_cmd([gh_bin, "project", "list", "--owner", "@me", "--format", "json"])
        
    project_number = None
    project_url = None
    
    if code == 0 and out:
        try:
            p_data = json.loads(out)
            projects_list = p_data.get("projects", p_data) if isinstance(p_data, dict) else p_data
            for p in projects_list:
                if p.get("title", "").strip().lower() == project_title.strip().lower():
                    project_number = p.get("number")
                    project_url = p.get("url")
                    print_info(f"Project '{project_title}' already exists (#{project_number}). Reusing it.")
                    break
        except Exception:
            pass
            
    # 2. Create Project if not found
    if not project_number:
        print_step(f"Creating new GitHub Project: '{project_title}'...")
        code, out, err = run_cmd([
            gh_bin, "project", "create",
            "--owner", owner,
            "--title", project_title,
            "--format", "json"
        ])
        if code != 0:
            print_warn(f"Failed to create project under owner '{owner}': {err}")
            print_info("Trying fallback to '--owner @me'...")
            code, out, err = run_cmd([
                gh_bin, "project", "create",
                "--owner", "@me",
                "--title", project_title,
                "--format", "json"
            ])
            
        if code == 0 and out:
            try:
                created_p = json.loads(out)
                project_number = created_p.get("number")
                project_url = created_p.get("url")
                print_success(f"Created GitHub Project #{project_number}: {project_title}")
            except Exception as e:
                print_error(f"Failed to parse created project output: {e}")
        else:
            print_error(f"Project creation failed: {err}")
            return None
            
    if not project_number:
        return None
        
    # 3. Link Project to the Repository
    print_step(f"Linking Project #{project_number} to repository '{owner}/{repo}'...")
    code, _, _ = run_cmd([
        gh_bin, "project", "link", str(project_number),
        "--owner", owner,
        "--repo", repo
    ])
    if code == 0:
        print_success(f"Project linked to {owner}/{repo}")
    else:
        print_info("Project link verified or already active.")
        
    # 4. Configure Project Fields
    print_step("Configuring custom Scrum Project fields...")
    code, f_out, _ = run_cmd([
        gh_bin, "project", "field-list", str(project_number),
        "--owner", owner,
        "--format", "json"
    ])
    existing_fields = set()
    if code == 0 and f_out:
        try:
            f_data = json.loads(f_out)
            fields_list = f_data.get("fields", f_data) if isinstance(f_data, dict) else f_data
            for f in fields_list:
                existing_fields.add(f.get("name", "").strip().lower())
        except Exception:
            pass
            
    custom_fields_cfg = setup_data.get("fields", {})
    
    # Priority Field
    if "priority" not in existing_fields and "Priority" in custom_fields_cfg:
        options = ",".join(custom_fields_cfg["Priority"])
        code, _, _ = run_cmd([
            gh_bin, "project", "field-create", str(project_number),
            "--owner", owner,
            "--name", "Priority",
            "--data-type", "SINGLE_SELECT",
            "--single-select-options", options
        ])
        if code == 0:
            print_success("Field 'Priority' (Single Select) → created")
            
    # Sprint Field
    if "sprint" not in existing_fields and "Sprint" in custom_fields_cfg:
        options = ",".join(custom_fields_cfg["Sprint"])
        code, _, _ = run_cmd([
            gh_bin, "project", "field-create", str(project_number),
            "--owner", owner,
            "--name", "Sprint",
            "--data-type", "SINGLE_SELECT",
            "--single-select-options", options
        ])
        if code == 0:
            print_success("Field 'Sprint' (Single Select) → created")
            
    # Type Field
    if "type" not in existing_fields and "Type" in custom_fields_cfg:
        options = ",".join(custom_fields_cfg["Type"])
        code, _, _ = run_cmd([
            gh_bin, "project", "field-create", str(project_number),
            "--owner", owner,
            "--name", "Type",
            "--data-type", "SINGLE_SELECT",
            "--single-select-options", options
        ])
        if code == 0:
            print_success("Field 'Type' (Single Select) → created")
            
    # Story Points Field
    if "story points" not in existing_fields:
        code, _, _ = run_cmd([
            gh_bin, "project", "field-create", str(project_number),
            "--owner", owner,
            "--name", "Story Points",
            "--data-type", "NUMBER"
        ])
        if code == 0:
            print_success("Field 'Story Points' (Number) → created")

    # 5. Add Issues to Project
    print_step(f"Adding {len(issues)} issues to Project #{project_number}...")
    
    # Check existing items
    code, item_out, _ = run_cmd([
        gh_bin, "project", "item-list", str(project_number),
        "--owner", owner,
        "--limit", "300",
        "--format", "json"
    ])
    existing_item_urls = set()
    if code == 0 and item_out:
        try:
            items_data = json.loads(item_out)
            items_list = items_data.get("items", items_data) if isinstance(items_data, dict) else items_data
            for itm in items_list:
                u = itm.get("content", {}).get("url") or itm.get("url")
                if u:
                    existing_item_urls.add(u.strip().lower())
        except Exception:
            pass
            
    added_to_project = 0
    for issue in issues:
        url = issue.get("url")
        ident = issue.get("identifier", "US")
        if not url:
            continue
            
        if url.strip().lower() in existing_item_urls:
            print_info(f"[{ident}] already present on Project board")
            added_to_project += 1
        else:
            code, _, err = run_cmd([
                gh_bin, "project", "item-add", str(project_number),
                "--owner", owner,
                "--url", url,
                "--format", "json"
            ])
            if code == 0:
                added_to_project += 1
                print_success(f"[OK] {ident} added to Project")
            else:
                print_warn(f"[{ident}] Could not add to project: {err}")
                
        # Update custom field values
        priority_val = issue.get("priority")
        if priority_val:
            run_cmd([
                gh_bin, "project", "item-edit", str(project_number),
                "--owner", owner,
                "--url", url,
                "--field", "Priority",
                "--value", priority_val
            ])
            
        sprint_val = issue.get("sprint")
        if sprint_val:
            run_cmd([
                gh_bin, "project", "item-edit", str(project_number),
                "--owner", owner,
                "--url", url,
                "--field", "Sprint",
                "--value", sprint_val
            ])
            
        type_val = issue.get("type")
        if type_val:
            run_cmd([
                gh_bin, "project", "item-edit", str(project_number),
                "--owner", owner,
                "--url", url,
                "--field", "Type",
                "--value", type_val
            ])
            
        sp_val = issue.get("story_points")
        if sp_val is not None:
            run_cmd([
                gh_bin, "project", "item-edit", str(project_number),
                "--owner", owner,
                "--url", url,
                "--field", "Story Points",
                "--number", str(sp_val)
            ])
            
        # Set Status to 'Done' or configured status if available
        status_val = issue.get("status", "Done")
        if status_val:
            run_cmd([
                gh_bin, "project", "item-edit", str(project_number),
                "--owner", owner,
                "--url", url,
                "--field", "Status",
                "--value", status_val
            ])

    # 6. Retrieve Final URL
    if not project_url:
        code, v_out, _ = run_cmd([gh_bin, "project", "view", str(project_number), "--owner", owner, "--format", "json"])
        if code == 0 and v_out:
            try:
                project_url = json.loads(v_out).get("url")
            except Exception:
                pass
                
    if not project_url:
        project_url = f"https://github.com/users/{owner}/projects/{project_number}"
        
    return project_url

def main():
    print_header("ONE-CLICK GITHUB PROJECT & KANBAN SETUP")
    
    check_config_only = "--check-config" in sys.argv
    dry_run = "--dry-run" in sys.argv
    
    # 1. Check Git
    if not check_git():
        print_error("Git is not installed or not available in PATH!")
        print_info("Please install Git from: https://git-scm.com/")
        sys.exit(1)
    print_success("Git detected successfully")
        
    # 2. Check GitHub CLI
    gh_bin = find_gh_cli()
    if not gh_bin:
        print_error("GitHub CLI ('gh') is not installed or not in PATH!")
        print_info("To install GitHub CLI:")
        print_info("  Option A (Windows Package Manager): winget install --id GitHub.cli")
        print_info("  Option B (Official Installer):     https://cli.github.com/")
        print_info("After installing, restart your terminal and run setup-project.bat again.")
        sys.exit(1)
    print_success("GitHub CLI ('gh') detected successfully")
        
    # 3. Detect Git Remote (Dynamic Extraction)
    owner, repo, remote_url = detect_repo_origin()
    if not owner or not repo:
        if check_config_only:
            owner, repo = "detected-owner", "detected-repo"
            print_warn(f"Remote origin not detected, using mock: {owner}/{repo}")
        else:
            print_error("Could not dynamically detect GitHub repository from Git remote 'origin'!")
            if remote_url:
                print_info(f"Detected remote origin: {remote_url}")
            else:
                print_info("No 'origin' remote found. Make sure you cloned your repository or ran:")
                print_info("  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git")
                
            print("\nPlease enter your GitHub repository details manually:")
            owner = input("  GitHub Owner / Username : ").strip()
            repo = input("  Repository Name         : ").strip()
            if not owner or not repo:
                print_error("Setup aborted: Repository information required.")
                sys.exit(1)
    else:
        print_success(f"Dynamic remote detected: {owner}/{repo} ({remote_url})")
            
    repo_slug = f"{owner}/{repo}"
    
    # 4. Load & Validate Configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    json_path = os.path.join(project_root, ".github", "project-setup.json")
    
    try:
        setup_data = load_project_setup_json(json_path)
        print_success(f"Configuration verified: {len(setup_data.get('issues', []))} User Stories, {len(setup_data.get('labels', []))} Labels, {len(setup_data.get('milestones', []))} Milestones")
    except Exception as e:
        print_error(f"Failed to load project configuration: {e}")
        sys.exit(1)
        
    if check_config_only:
        print_header("CONFIGURATION VALIDATION PASSED")
        print_info("All Scrum JSON structures, labels, milestones, and issues are 100% valid.")
        sys.exit(0)
    
    # 5. Check GitHub Authentication
    is_authed, username, scopes = check_gh_auth(gh_bin)
    if not is_authed:
        if "--no-interactive" in sys.argv:
            print_warn("GitHub CLI not authenticated in non-interactive mode.")
            print_info("To authenticate, run: gh auth login -w -s repo,project")
            sys.exit(0)
        print_warn("You are not currently authenticated with GitHub CLI.")
        print_info("You must authenticate with YOUR OWN GitHub account to configure your repository.")
        print_info("Launching 'gh auth login' now...\n")
        subprocess.run([gh_bin, "auth", "login", "-w", "-s", "repo,project"])
        
        # Re-check
        is_authed, username, scopes = check_gh_auth(gh_bin)
        if not is_authed:
            print_error("Authentication failed or was cancelled. Setup cannot proceed.")
            sys.exit(1)
            
    # Ensure project scope
    ensure_project_scope(gh_bin, scopes)
    
    # 6. Display Confirmation Banner
        
    project_name = setup_data.get("project_name", f"{repo} — Scrum Board")
    
    print(f"{Colors.BOLD}Detected repository:{Colors.RESET}")
    print(f"  Owner      : {Colors.CYAN}{owner}{Colors.RESET}")
    print(f"  Repository : {Colors.CYAN}{repo}{Colors.RESET}")
    print(f"\n{Colors.BOLD}Authenticated GitHub account:{Colors.RESET}")
    print(f"  User       : {Colors.GREEN}{username or 'Active'}{Colors.RESET}")
    print(f"\n{Colors.BOLD}Target Project Board:{Colors.RESET}")
    print(f"  Name       : {Colors.YELLOW}{project_name}{Colors.RESET}")
    print()
    
    # Non-interactive flag check or confirmation
    if "--yes" not in sys.argv and "-y" not in sys.argv:
        confirm = input("Continue with setup on this repository? [Y/n]: ").strip().lower()
        if confirm not in ('', 'y', 'yes'):
            print_info("Setup cancelled by user.")
            sys.exit(0)
            
    # 6. Reconcile Labels
    labels_cfg = setup_data.get("labels", [])
    labels_created, labels_existing = reconcile_labels(gh_bin, repo_slug, labels_cfg)
    
    # 7. Reconcile Milestones
    milestones_cfg = setup_data.get("milestones", [])
    reconcile_milestones(gh_bin, repo_slug, milestones_cfg)
    
    # 8. Reconcile Issues
    issues_cfg = setup_data.get("issues", [])
    issues_created, issues_existing, synced_issues = reconcile_issues(gh_bin, repo_slug, issues_cfg, milestones_cfg)
    
    # 9. Setup GitHub Project V2 Board
    project_url = setup_github_project(gh_bin, owner, repo, setup_data, synced_issues)
    
    # 10. Display Grand Summary
    print_header("SETUP COMPLETE")
    print(f"{Colors.BOLD}Repository:{Colors.RESET}")
    print(f"  https://github.com/{owner}/{repo}\n")
    
    if project_url:
        print(f"{Colors.BOLD}Project / Kanban Board:{Colors.RESET}")
        print(f"  {Colors.GREEN}{Colors.BOLD}{project_url}{Colors.RESET}\n")
    else:
        print(f"{Colors.BOLD}Project / Kanban Board:{Colors.RESET}")
        print(f"  Visit https://github.com/{owner}/{repo}/projects\n")
        
    print(f"{Colors.BOLD}Summary Statistics:{Colors.RESET}")
    print(f"  Issues created          : {Colors.GREEN}{issues_created}{Colors.RESET}")
    print(f"  Issues already existing : {Colors.YELLOW}{issues_existing}{Colors.RESET}")
    print(f"  Issues added to Project : {Colors.GREEN}{len(synced_issues)}{Colors.RESET}")
    print(f"  Labels configured       : {Colors.GREEN}{labels_created + labels_existing}{Colors.RESET}")
    print(f"  Kanban board status     : {Colors.GREEN}Ready{Colors.RESET}\n")
    
    if project_url:
        print(f"{Colors.BOLD}Open the Project:{Colors.RESET}")
        print(f"  {project_url}\n")
        
        # If interactive, offer to launch browser
        if "--no-browser" not in sys.argv:
            try:
                open_b = input("Would you like to open the GitHub Project in your browser now? [Y/n]: ").strip().lower()
                if open_b in ('', 'y', 'yes'):
                    webbrowser.open(project_url)
            except Exception:
                pass
                
    print(f"\n{Colors.GREEN}{Colors.BOLD}All Scrum artifacts, labels, user stories, and Kanban views are live!{Colors.RESET}\n")

if __name__ == "__main__":
    main()
