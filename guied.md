# 🚀 Step-by-Step PythonAnywhere Deployment Guide — 100% HUMANITY

This guide walks you through the complete deployment workflow for **100% HUMANITY** on [PythonAnywhere](https://www.pythonanywhere.com/).

---

## 📋 Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Project Requirements Overview](#2-project-requirements-overview)
3. [Step 1: Open Bash Console & Clone Repository](#step-1-open-bash-console--clone-repository)
4. [Step 2: Create Virtual Environment & Install Dependencies](#step-2-create-virtual-environment--install-dependencies)
5. [Step 3: Setup Production Environment Variables (.env)](#step-3-setup-production-environment-variables-env)
6. [Step 4: Run Migrations & Seed Initial Content](#step-4-run-migrations--seed-initial-content)
7. [Step 5: Collect Static Files](#step-5-collect-static-files)
8. [Step 6: Configure the PythonAnywhere Web Tab](#step-6-configure-the-pythonanywhere-web-tab)
9. [Step 7: Configure the WSGI File](#step-7-configure-the-wsgi-file)
10. [Step 8: Map Static & Media Files in PythonAnywhere](#step-8-map-static--media-files-in-pythonanywhere)
11. [Step 9: Enable HTTPS & Reload Application](#step-9-enable-https--reload-application)
12. [Step 10: Manage API Keys & Settings via Admin Dashboard](#step-10-manage-api-keys--settings-via-admin-dashboard)
13. [Routine Maintenance & Updating Code](#routine-maintenance--updating-code)
14. [Troubleshooting & FAQs](#troubleshooting--faqs)

---

## 1. Prerequisites
- A [PythonAnywhere Account](https://www.pythonanywhere.com/) (Free "Beginner" tier or custom domain account).
- Your PythonAnywhere username (e.g. `yourusername`).
- Your web app URL will be: `https://yourusername.pythonanywhere.com`.
- Recommended Python version: **Python 3.10** or **Python 3.11**.

---

## 2. Project Requirements Overview

The application uses standard production packages listed in [`requirements.txt`](requirements.txt):

| Package | Purpose in 100% HUMANITY |
| :--- | :--- |
| **Django (>=5.0, <5.2)** | Core monolithic web framework. |
| **Pillow (>=10.4.0)** | Local image validation, resizing, and thumbnail generation. |
| **python-dotenv (>=1.0.1)** | Loads secret keys and database URLs from `.env`. |
| **whitenoise (>=6.7.0)** | High-efficiency static file compression and caching. |
| **dj-database-url (>=2.2.0)** | Enables seamless switching between SQLite and PostgreSQL/MySQL. |
| **psycopg2-binary (>=2.9.9)** | Driver for external PostgreSQL (e.g., Neon or Supabase if used). |
| **requests (>=2.32.0)** | Video and external metadata verification. |
| **cloudinary (>=1.41.0)** | Cloud photo CDN storage (optional; local media is also supported). |
| **gunicorn (>=22.0.0)** | WSGI HTTP server (used on Render/Docker; PythonAnywhere uses native uWSGI). |

---

## Step 1: Open Bash Console & Clone Repository

1. Log in to your **PythonAnywhere Dashboard**.
2. Go to the **Consoles** tab and click on **Bash** under *"Start a new console"*.
3. In the Bash terminal, clone your project repository:
   ```bash
   git clone https://github.com/<your-username>/100-humanity-django-webapp.git 100-humanity
   ```
4. Navigate into the project folder:
   ```bash
   cd ~/100-humanity
   pwd
   ```
   *Expected path: `/home/yourusername/100-humanity`*

---

## Step 2: Create Virtual Environment & Install Dependencies

In the same Bash console:

1. Create a virtual environment with Python 3.10 or 3.11 using `virtualenvwrapper`:
   ```bash
   mkvirtualenv --python=python3.10 humanity-env
   ```
   *(Note: Whenever you open a new console in the future, you can activate this environment by running: `workon humanity-env`)*

2. Upgrade `pip` and `setuptools`:
   ```bash
   pip install --upgrade pip setuptools
   ```

3. Install all project requirements:
   ```bash
   pip install -r requirements.txt
   ```

---

## Step 3: Setup Production Environment Variables (.env)

1. Generate a strong Django `SECRET_KEY`:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   *Copy the output string.*

2. Create your `.env` file in the project root:
   ```bash
   nano .env
   ```

3. Paste the following configuration (replace `yourusername` and `your-generated-secret-key`):
   ```ini
   DEBUG=False
   SECRET_KEY=your-generated-secret-key-here
   ALLOWED_HOSTS=yourusername.pythonanywhere.com,localhost,127.0.0.1
   CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com

   # Database (leave blank to use fast local SQLite out-of-the-box on PythonAnywhere)
   DATABASE_URL=

   # Optional Cloudinary CDN (leave empty to store photos directly on PythonAnywhere)
   CLOUDINARY_CLOUD_NAME=
   CLOUDINARY_API_KEY=
   CLOUDINARY_API_SECRET=
   CLOUDINARY_FOLDER=100_humanity

   # Site Branding
   SITE_NAME=100% HUMANITY
   CONTACT_PERSON=Arvind Betkar
   CONTACT_EMAIL=arvindbet12@gmail.com
   CONTACT_PHONE=8983087210
   YOUTUBE_CHANNEL_NAME=100% HUMANITY
   ```

4. Press `Ctrl + O` then `Enter` to save, and `Ctrl + X` to exit `nano`.

---

## Step 4: Run Migrations & Seed Initial Content

With your virtualenv active (`workon humanity-env`):

1. Apply all database migrations:
   ```bash
   python manage.py migrate
   ```

2. Seed the 15 Dhamma Teacher Principles, site settings, and sample data:
   ```bash
   python manage.py seed_initial_data
   ```

3. Create your administrative superuser account:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to enter your username, email, and password.

---

## Step 5: Collect Static Files

Run `collectstatic` to gather all CSS, JS, SVGs, and brand assets into `staticfiles/`:
```bash
python manage.py collectstatic --noinput
```

---

## Step 6: Configure the PythonAnywhere Web Tab

1. In the PythonAnywhere top navigation bar, click on **Web**.
2. Click **"Add a new web app"**.
3. When prompted:
   - Domain: `yourusername.pythonanywhere.com` (click **Next**).
   - Select web framework: Choose **Manual configuration** *(DO NOT choose Django, as it creates a dummy project)*.
   - Select Python version: Choose **Python 3.10** (matching your virtual environment).
   - Click **Next** to finish setup.

4. On your Web configuration page, configure the paths under **Code**:
   - **Source code**: `/home/yourusername/100-humanity`
   - **Working directory**: `/home/yourusername/100-humanity`
   - **WSGI configuration file**: Click the link `/var/www/yourusername_pythonanywhere_com_wsgi.py` (we will edit this next).

5. Under **Virtualenv**:
   - Enter: `/home/yourusername/.virtualenvs/humanity-env`
   - Click the checkmark to save.

---

## Step 7: Configure the WSGI File

Click the **WSGI configuration file** link (`/var/www/yourusername_pythonanywhere_com_wsgi.py`). Delete all existing code in that file and replace it with:

```python
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 1. Add your project directory to Python's search path
project_home = '/home/yourusername/100-humanity'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 2. Load environment variables from .env file
dotenv_path = Path(project_home) / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# 3. Specify the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# 4. Initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
> ⚠️ **Important**: Replace `yourusername` with your actual PythonAnywhere username!
> Click the **Save** button in the top right corner.

---

## Step 8: Map Static & Media Files in PythonAnywhere

PythonAnywhere's Nginx web server serves static and media files directly for optimal speed.

Return to the **Web** tab and scroll to the **Static files** section. Add two directory mappings:

| URL | Directory Path |
| :--- | :--- |
| `/static/` | `/home/yourusername/100-humanity/staticfiles` |
| `/media/` | `/home/yourusername/100-humanity/media` |

*(Replace `yourusername` with your PythonAnywhere account name).*

---

## Step 9: Enable HTTPS & Reload Application

1. In the **Web** tab, scroll down to **Security** and toggle **Force HTTPS** to **ON**.
2. Scroll back to the top of the **Web** tab and click the large green button:
   ```
   Reload yourusername.pythonanywhere.com
   ```
3. Open your browser and visit:
   - **Public Site**: `https://yourusername.pythonanywhere.com/`
   - **Dhamma Education Curriculum**: `https://yourusername.pythonanywhere.com/dhamma-education/`
   - **Admin Dashboard**: `https://yourusername.pythonanywhere.com/admin/`

---

## Step 10: Manage API Keys & Settings via Admin Dashboard

You do **not** need to SSH into PythonAnywhere or edit server files whenever you want to update configurations:

1. Log into `https://yourusername.pythonanywhere.com/admin/`.
2. Navigate to **Core** &rarr; **Environment & API Settings**:
   - Update **Database URL** (e.g., connect an external PostgreSQL/Neon database).
   - Enter or update **Cloudinary API Key**, **API Secret**, and **Cloud Name**.
   - Update contact details or YouTube channel URLs.
3. Click **Save**. The application uses runtime database-backed overrides with automatic cache synchronization.

---

## Routine Maintenance & Updating Code

Whenever you push new code or commits from your local machine to GitHub:

1. Open your PythonAnywhere **Bash** console:
   ```bash
   cd ~/100-humanity
   workon humanity-env
   git pull origin main
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
2. In the PythonAnywhere **Web** tab, click **Reload**.

---

## Troubleshooting & FAQs

### 1. `DisallowedHost` or `Invalid HTTP_HOST header`
- **Solution**: Open `.env` and verify `ALLOWED_HOSTS` includes `yourusername.pythonanywhere.com`. Then reload the web app.

### 2. `403 Forbidden` / `CSRF verification failed` on form submit
- **Solution**: Open `.env` and check that `CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com` begins with `https://`.

### 3. Styling / CSS appears unstyled
- **Solution**: 
  1. Run `python manage.py collectstatic --noinput`.
  2. Verify in the Web tab that `/static/` points to `/home/yourusername/100-humanity/staticfiles`.

### 4. Viewing Server & Error Logs
- Go to the **Web** tab &rarr; **Log files**:
  - **Error log**: `/var/log/yourusername.pythonanywhere.com.error.log`
  - **Server log**: `/var/log/yourusername.pythonanywhere.com.server.log`
