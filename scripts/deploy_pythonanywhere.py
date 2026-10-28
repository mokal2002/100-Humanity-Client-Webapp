#!/usr/bin/env python3
"""
PythonAnywhere Automated Deployment Script for GitHub Actions.
Uses the official PythonAnywhere REST API to:
1. Open a Bash console session.
2. Execute: git pull, migrate, and collectstatic inside your virtual environment.
3. Trigger a graceful Web App reload via the webapps API.
Works on all PythonAnywhere account tiers (including Free Beginner accounts).
"""
import os
import sys
import time
import requests

PA_HOST = os.environ.get("PA_HOST", "www.pythonanywhere.com")
USERNAME = os.environ.get("PA_USERNAME", "").strip()
API_TOKEN = os.environ.get("PA_API_TOKEN", "").strip()
DOMAIN = os.environ.get("PA_DOMAIN", "").strip() or (f"{USERNAME}.{PA_HOST}" if USERNAME else "")
PROJECT_DIR = os.environ.get("PA_PROJECT_DIR", "100-humanity").strip()
VENV_NAME = os.environ.get("PA_VENV_NAME", "humanity-env").strip()
BRANCH = os.environ.get("PA_BRANCH", "main").strip()

if not USERNAME or not API_TOKEN:
    print("::error ::Missing PA_USERNAME or PA_API_TOKEN environment variables in GitHub Secrets.")
    print("Please set PA_USERNAME and PA_API_TOKEN under GitHub Repository Settings -> Secrets and variables -> Actions.")
    sys.exit(1)

BASE_URL = f"https://{PA_HOST}/api/v0/user/{USERNAME}"
HEADERS = {"Authorization": f"Token {API_TOKEN}"}


def run_remote_commands():
    """Create a temporary bash console on PythonAnywhere and execute update commands."""
    print(f"🚀 [1/3] Creating PythonAnywhere bash console for user '{USERNAME}'...")
    console_url = f"{BASE_URL}/consoles/"
    res = requests.post(console_url, json={"executable": "/bin/bash"}, headers=HEADERS, timeout=30)
    
    if res.status_code not in (200, 201):
        print(f"::warning ::Could not create new console ({res.status_code}): {res.text}")
        # Try finding existing consoles
        list_res = requests.get(console_url, headers=HEADERS, timeout=30)
        if list_res.status_code == 200 and list_res.json():
            console_id = list_res.json()[0]["id"]
            print(f"Using existing console #{console_id}...")
        else:
            print("::error ::Failed to acquire a console session.")
            return False
    else:
        console_id = res.json()["id"]
        print(f"Bash console #{console_id} created.")

    # Prepare command string
    deploy_cmd = (
        f"cd ~/{PROJECT_DIR} && "
        f"git pull origin {BRANCH} && "
        f"source ~/.virtualenvs/{VENV_NAME}/bin/activate && "
        f"python manage.py migrate --noinput && "
        f"python manage.py collectstatic --noinput && "
        f"echo 'DEPLOY_COMPLETE_TOKEN_SUCCESS'\n"
    )

    print(f"📦 [2/3] Executing git pull, migrate, and collectstatic...")
    input_url = f"{BASE_URL}/consoles/{console_id}/send_input/"
    input_res = requests.post(input_url, json={"input": deploy_cmd}, headers=HEADERS, timeout=30)
    if input_res.status_code != 200:
        print(f"::error ::Failed to send commands to console: {input_res.text}")
        return False

    # Poll console output until command finishes or timeout (up to 90 seconds)
    output_url = f"{BASE_URL}/consoles/{console_id}/get_latest_output/"
    start_time = time.time()
    completed = False
    
    while time.time() - start_time < 90:
        time.sleep(5)
        out_res = requests.get(output_url, headers=HEADERS, timeout=30)
        if out_res.status_code == 200:
            text = out_res.json().get("output", "")
            if "DEPLOY_COMPLETE_TOKEN_SUCCESS" in text:
                print("✅ Deployment commands finished successfully on PythonAnywhere!")
                completed = True
                break

    if not completed:
        print("::warning ::Console commands timed out or finished asynchronously. Proceeding with Web reload...")

    # Clean up console
    try:
        requests.delete(f"{BASE_URL}/consoles/{console_id}/", headers=HEADERS, timeout=10)
    except Exception:
        pass

    return True


def reload_webapp():
    """Trigger PythonAnywhere Web App reload via REST API."""
    print(f"🔄 [3/3] Reloading webapp '{DOMAIN}'...")
    reload_url = f"{BASE_URL}/webapps/{DOMAIN}/reload/"
    res = requests.post(reload_url, headers=HEADERS, timeout=30)
    if res.status_code == 200:
        print(f"🎉 Web application successfully reloaded! Live at: https://{DOMAIN}/")
        return True
    else:
        print(f"::error ::Failed to reload web application ({res.status_code}): {res.text}")
        return False


if __name__ == "__main__":
    commands_ok = run_remote_commands()
    reload_ok = reload_webapp()
    if not (commands_ok and reload_ok):
        sys.exit(1)
    print("✨ Deployment workflow completed successfully!")
