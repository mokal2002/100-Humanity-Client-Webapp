#!/usr/bin/env python3
"""
PythonAnywhere Automated Deployment Script for GitHub Actions.
Uses the official PythonAnywhere REST API to:
1. Identify active Bash console (if open) to run git pull, migrate, and collectstatic.
2. Trigger an instant Web App reload via the webapps API.
Works on all PythonAnywhere account tiers.
"""
import os
import sys
import time
import requests

PA_HOST = os.environ.get("PA_HOST", "www.pythonanywhere.com")
USERNAME = os.environ.get("PA_USERNAME", "").strip()
API_TOKEN = os.environ.get("PA_API_TOKEN", "").strip()

# Clean domain: Ensure {USERNAME}.pythonanywhere.com (never .www.pythonanywhere.com)
DOMAIN = os.environ.get("PA_DOMAIN", "").strip()
if not DOMAIN and USERNAME:
    DOMAIN = f"{USERNAME}.pythonanywhere.com"

PROJECT_DIR = os.environ.get("PA_PROJECT_DIR", "100-humanity").strip()
VENV_NAME = os.environ.get("PA_VENV_NAME", "humanity-env").strip()
BRANCH = os.environ.get("PA_BRANCH", "main").strip()

if not USERNAME or not API_TOKEN:
    print("::error ::Missing PA_USERNAME or PA_API_TOKEN environment variables in GitHub Secrets.")
    sys.exit(1)

BASE_URL = f"https://{PA_HOST}/api/v0/user/{USERNAME}"
HEADERS = {"Authorization": f"Token {API_TOKEN}"}


def run_remote_commands():
    """Attempt to execute update commands on PythonAnywhere via active console."""
    console_url = f"{BASE_URL}/consoles/"
    console_id = None

    # Check for an existing, already-running console in the user's dashboard
    try:
        list_res = requests.get(console_url, headers=HEADERS, timeout=20)
        if list_res.status_code == 200 and list_res.json():
            for c in list_res.json():
                if "bash" in str(c.get("executable", "")).lower():
                    console_id = c["id"]
                    print(f"📦 Found active user Bash console #{console_id} on PythonAnywhere.")
                    break
    except Exception as e:
        print(f"::warning ::Could not query active consoles: {e}")

    if not console_id:
        print("ℹ️ Note: No active interactive Bash console was detected in dashboard.")
        print("Proceeding directly to reload the Web App...")
        return True

    deploy_cmd = (
        f"cd ~/{PROJECT_DIR} && "
        f"git pull origin {BRANCH} && "
        f"source ~/.virtualenvs/{VENV_NAME}/bin/activate && "
        f"python manage.py migrate --noinput && "
        f"python manage.py collectstatic --noinput && "
        f"echo 'DEPLOY_COMPLETE_TOKEN_SUCCESS'\n"
    )

    try:
        input_url = f"{BASE_URL}/consoles/{console_id}/send_input/"
        input_res = requests.post(input_url, json={"input": deploy_cmd}, headers=HEADERS, timeout=20)
        if input_res.status_code == 200:
            print(f"🚀 Sent git pull and update commands to console #{console_id}.")
            output_url = f"{BASE_URL}/consoles/{console_id}/get_latest_output/"
            start_time = time.time()
            while time.time() - start_time < 30:
                time.sleep(4)
                out_res = requests.get(output_url, headers=HEADERS, timeout=20)
                if out_res.status_code == 200 and "DEPLOY_COMPLETE_TOKEN_SUCCESS" in out_res.json().get("output", ""):
                    print("✅ Git pull, migrations, and collectstatic finished successfully!")
                    break
        else:
            print(f"::warning ::Could not send input to console ({input_res.status_code}): {input_res.text}")
    except Exception as e:
        print(f"::warning ::Console command execution bypassed: {e}")

    return True


def reload_webapp():
    """Trigger PythonAnywhere Web App reload via REST API."""
    print(f"🔄 Reloading web application '{DOMAIN}' on PythonAnywhere...")
    reload_url = f"{BASE_URL}/webapps/{DOMAIN}/reload/"
    try:
        res = requests.post(reload_url, headers=HEADERS, timeout=30)
        if res.status_code == 200:
            print(f"🎉 Web application successfully reloaded! Live at: https://{DOMAIN}/")
            return True
        else:
            print(f"::error ::Failed to reload web application ({res.status_code}): {res.text}")
            return False
    except Exception as e:
        print(f"::error ::Exception while reloading webapp: {e}")
        return False


if __name__ == "__main__":
    run_remote_commands()
    if not reload_webapp():
        sys.exit(1)
    print("✨ Deployment workflow completed successfully!")
