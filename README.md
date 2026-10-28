# 100% HUMANITY — Official Educational Website (Django Monolithic Web App)

A complete, responsive, zero-budget Python/Django monolithic web application built for **100% HUMANITY**, an educational initiative focused on Gautama Buddha's teachings, Buddha Dhamma, human equality, compassion, mindfulness meditation, scientific thinking, and social awareness.

---

## 1. Website Identity & Verified Details

- **Website Name:** 100% HUMANITY
- **Coordinator / Contact Person:** Arvind Betkar
- **Email:** `arvindbet12@gmail.com`
- **Phone:** `8983087210`
- **YouTube Channel Name:** 100% HUMANITY *(Channel URL is editable anytime in Django Admin → Site Settings)*
- **Budget Requirement:** Strictly ₹0 (100% Free Open-Source Stack & Free-Tier Hosting)

---

## 2. Architecture & Project Structure

```text
100-humanity/
├── manage.py
├── requirements.txt
├── runtime.txt
├── build.sh
├── Procfile
├── render.yaml
├── vercel.json
├── pythonanywhere_wsgi.py
├── .env.example
├── .gitignore
├── README.md
├── config/
│   ├── __init__.py
│   ├── settings.py          # Local SQLite + Prod PostgreSQL, Cloudinary, Security, i18n
│   ├── urls.py              # Named routes, Sitemap, robots.txt, healthz, Admin
│   ├── sitemaps.py          # SEO XML Sitemaps
│   ├── wsgi.py              # Gunicorn / PythonAnywhere / Vercel WSGI entry point
│   └── asgi.py
├── apps/
│   ├── core/                # SiteSettings singleton, Home, About Us, seed_initial_data
│   ├── education/           # 15 Principles for Developing Good Dhamma Teachers
│   ├── events/              # Events & EventImage management, upcoming/past filtering
│   ├── gallery/             # GalleryAlbum, GalleryImage, Cloudinary SDK service, bulk upload
│   ├── videos/              # VideoCategory, Video, server-side YouTube ID validator
│   ├── articles/            # ArticleCategory, Article, safe rendering, search & tags
│   └── contact/             # ContactSubmission (New / In Progress / Resolved), honeypot spam guard
├── templates/
│   ├── base.html
│   ├── 404.html
│   ├── 500.html
│   ├── components/          # navbar.html, footer.html, pagination.html, messages.html
│   ├── core/                # home.html, about.html
│   ├── education/           # principle_list.html
│   ├── events/              # event_list.html, event_detail.html
│   ├── gallery/             # album_list.html, album_detail.html, bulk_upload.html
│   ├── videos/              # video_list.html, video_detail.html
│   ├── articles/            # article_list.html, article_detail.html
│   └── contact/             # contact.html
├── static/
│   ├── css/style.css        # Warm ivory, muted saffron & gold, WCAG accessible typography
│   ├── js/main.js           # Mobile nav, gallery lightbox (prev/next/keyboard), upload preview
│   └── images/dhamma-wheel.svg
└── locale/                  # English (en), Marathi (mr), Hindi (hi) i18n catalogs
```

---

## 3. Local Setup on Windows (Step-by-Step)

### Step 1: Install Python & Git
1. Download and install **Python 3.11 or 3.12** from [python.org](https://www.python.org/downloads/windows/).
   - **Important:** Check the box **"Add python.exe to PATH"** during installation.
2. Open **Command Prompt (`cmd`)** or **PowerShell** and navigate to the project folder:
   ```powershell
   cd path\to\100-humanity
   ```

### Step 2: Create and Activate a Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables (`.env`)
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Open `.env` in Notepad or VS Code:
- Keep `DEBUG=True` for local development on your computer.
- Leave `DATABASE_URL=` blank locally so Django automatically uses `db.sqlite3`.
- Generate a strong `SECRET_KEY` by running:
  ```powershell
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  Paste that output into `SECRET_KEY=` in `.env`.

### Step 5: Run Database Migrations & Seed the 15 Dhamma Principles
```powershell
python manage.py migrate
python manage.py seed_initial_data
```

### Step 6: Create Your Administrator (Superuser) Account
```powershell
python manage.py createsuperuser
```
- Enter a username (e.g., `arvind`), email (`arvindbet12@gmail.com`), and a strong password (at least 10 characters, mixing letters, numbers, and symbols).

### Step 7: Start the Development Server
```powershell
python manage.py runserver
```
- **Public Website:** Open `http://127.0.0.1:8000/`
- **Admin Dashboard:** Open `http://127.0.0.1:8000/admin/`

---

## 4. Running Automated Checks & Tests

Run the following verification commands from your activated virtual environment:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py check --deploy
```

---

## 5. Free Cloudinary Setup (Image Uploads & Storage)

1. Sign up for a free account at [https://cloudinary.com/users/register_free](https://cloudinary.com/users/register_free) (No credit card required; includes **25 free monthly credits** = up to 25 GB storage or bandwidth or 25,000 transformations).
2. Open your **Cloudinary Programmable Media Dashboard** and copy your:
   - **Cloud Name**
   - **API Key**
   - **API Secret**
3. Paste them into your `.env` file (locally) or your hosting provider's Environment Variables panel:
   ```ini
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   CLOUDINARY_FOLDER=100_humanity
   ```
4. **How it works:**
   - All uploads happen server-side via the official `cloudinary` Python SDK (`apps/gallery/services.py`).
   - API secrets are never exposed to browser JavaScript.
   - Only `JPG`, `JPEG`, `PNG`, and `WEBP` images up to `5 MB` are accepted and verified with Pillow.
   - Replacing or deleting an image in Django Admin or the Gallery automatically deletes the old asset from Cloudinary using its stored `public_id`.
   - **Free Alternative if Cloudinary is unavailable:** Every image model (`GalleryImage`, `Event`, `Article`) also allows pasting a direct HTTPS image URL (for example, from an open-source GitHub repository release asset or Wikimedia Commons) without requiring Cloudinary credentials.

---

## 6. Free Hosting & Database Comparison (Verified 2026 Official Limits)

| Hosting Option | Free Tier Limits | Database Persistence | Cloudinary Outbound API | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **Option A: Render Free Web Service + Neon Free PostgreSQL** *(Recommended)* | Render Free: 750 hrs/month, free `.onrender.com` HTTPS subdomain, sleeps after 15 mins idle. Neon Free: 1 GB persistent PostgreSQL storage, 100 CU-hours/month, no credit card, never expires. | **100% Persistent** via Neon PostgreSQL (`DATABASE_URL`). | **Unrestricted** outbound HTTPS access to `api.cloudinary.com`. | **Best Overall** for full features (Admin + Bulk Cloudinary Uploads + Persistent DB). |
| **Option B: Vercel Hobby + Neon Free PostgreSQL** | Vercel Hobby: 100 GB bandwidth, 1M function invocations/month, non-commercial use, free `.vercel.app` HTTPS domain. | **100% Persistent** via Neon PostgreSQL (`DATABASE_URL`). | **Unrestricted** outbound HTTPS access to `api.cloudinary.com`. | **Great Fast Alternative** (4.5 MB serverless request body cap means upload 1–2 photos at a time). |
| **Option C: PythonAnywhere Free Plan** | 1 web app at `username.pythonanywhere.com`, 512 MiB persistent disk, 100 CPU-seconds/day, must click "Extend" once a month. | **Persistent SQLite** on the 512 MiB disk. | **Restricted Outbound Proxy:** Free accounts can only connect to allowlisted domains; `api.cloudinary.com` is often blocked by the free proxy. | Good for zero-external-DB hosting, but direct server-side Cloudinary uploads may require pasting image URLs instead. |

### Step-by-Step Deployment (Recommended: Render + Neon + Cloudinary)

1. **Push Code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: 100% HUMANITY Django web application"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/100-humanity.git
   git push -u origin main
   ```
2. **Create Free Neon PostgreSQL Database:**
   - Sign up at [https://neon.com](https://neon.com) (Free plan, no credit card).
   - Create a project named `100-humanity` and copy the **Connection String** (`postgresql://...`).
3. **Deploy on Render:**
   - Sign up at [https://render.com](https://render.com) using your GitHub account.
   - Click **New + → Web Service** and select your `100-humanity` repository.
   - Set **Build Command:** `./build.sh`
   - Set **Start Command:** `gunicorn config.wsgi:application`
   - Choose the **Free** instance type.
   - Under **Environment Variables**, add:
     - `DEBUG` = `False`
     - `SECRET_KEY` = *(your 50-character random secret key)*
     - `ALLOWED_HOSTS` = `.onrender.com,localhost,127.0.0.1`
     - `DATABASE_URL` = *(your Neon PostgreSQL connection string)*
     - `CLOUDINARY_CLOUD_NAME` = *(your Cloudinary cloud name)*
     - `CLOUDINARY_API_KEY` = *(your Cloudinary API key)*
     - `CLOUDINARY_API_SECRET` = *(your Cloudinary API secret)*
   - Click **Deploy Web Service**. Render will automatically install packages, collect static files with WhiteNoise, run migrations, and seed the 15 Dhamma principles!

---

## 7. Non-Technical Administrator Guide (Managing Your Website)

Log in at `https://your-site-url/admin/` with your administrator username and password.

1. **Updating Contact Details & YouTube Channel Link:**
   - Click **Site Settings & Page Content** → **100% HUMANITY — Global Configuration**.
   - Update phone numbers, email, homepage text, or paste your official **YouTube Channel URL**, then click **Save**.
2. **Editing or Reordering the 15 Dhamma Principles:**
   - Click **Dhamma Education Principles**.
   - You can change the **Display Order**, toggle **Feature on Homepage**, or click any principle to edit its explanation and learning resources.
3. **Adding an Event:**
   - Click **Events → Add Event**.
   - Enter the Title, Start/End Date, Time, Venue, and Description.
   - Upload a Cover Photograph (and optional additional photographs at the bottom).
   - Set **Publication Status** to **Published** and click **Save**.
4. **Uploading Multiple Gallery Photographs at Once:**
   - Create an album first under **Gallery Albums → Add Gallery Album**.
   - Visit `/gallery/upload/` on the website while logged in as an administrator (or click **+ Upload Multiple Photos** on the Photo Gallery page).
   - Choose the album, select multiple photos from your computer or phone, review the instant image previews, and click **Upload Photographs to Cloudinary**.
5. **Adding a YouTube Video:**
   - Click **YouTube Videos → Add YouTube Video**.
   - Enter the Title, Description, and paste any standard YouTube link (`https://www.youtube.com/watch?v=...`, `https://youtu.be/...`, or `https://www.youtube.com/shorts/...`).
   - Django automatically validates the URL, extracts the 11-character Video ID, and creates a privacy-enhanced responsive video player.
6. **Publishing an Educational Article:**
   - Click **Educational Articles → Add Educational Article**.
   - Enter the Title, Summary, Full Content (plain text paragraphs—safe from HTML injection), Category, and Tags.
   - Change **Publication Status** from `Draft` to `Published` and click **Save**.
7. **Managing Contact Form Submissions:**
   - Click **Contact Submissions**.
   - View messages submitted by visitors and update their **Workflow Status** (`New`, `In Progress`, or `Resolved`) and private **Internal Admin Notes**.

---

## 8. Backup, Recovery & Portability

Because you own 100% of the source code and standard Django ORM models:
- **Exporting All Database Content:** Run `python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > backup.json`
- **Restoring to Any New Host:** Run `python manage.py migrate && python manage.py loaddata backup.json`
