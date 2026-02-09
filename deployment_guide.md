---
description: Steps to push to GitHub and host on PythonAnywhere
---

# Deployment Guide

Follow these steps to push your project to GitHub and host it live on PythonAnywhere.

## Phase 1: Push to GitHub

1.  **Create a Repository**:
    *   Go to [GitHub](https://github.com/) and create a new repository (e.g., `courier_tracking`).
    *   Do **not** initialize with README or .gitignore.
2.  **Initialize Git Locally**:
    *   Open your terminal in the project root (`c:\Users\HANSLEM KIMENG\Desktop\WEB\PYTHON\courier_demo\courier_tracking`).
    *   Run:
        ```bash
        git init
        git add .
        git commit -m "Initial commit - Global Express Logistics"
        ```
3.  **Connect to GitHub**:
    *   Copy your repository URL from GitHub.
    *   Run:
        ```bash
        git branch -M main
        git remote add origin https://github.com/YOUR_USERNAME/courier_tracking.git
        git push -u origin main
        ```

---

## Phase 2: Host on PythonAnywhere

1.  **Clone the Code**:
    *   Log in to [PythonAnywhere](https://www.pythonanywhere.com/).
    *   Open a **Bash Console**.
    *   Run:
        ```bash
        git clone https://github.com/YOUR_USERNAME/courier_tracking.git
        cd courier_tracking
        ```
2.  **Set Up Virtual Environment**:
    *   In the same console, run:
        ```bash
        mkvirtualenv --python=/usr/bin/python3.10 .venv
        pip install -r requirements.txt
        ```
3.  **Configure Web Tab**:
    *   Go to the **Web** tab on PythonAnywhere.
    *   Click **Add a new web app**.
    *   Choose **Manual Configuration** -> **Python 3.10**.
    *   **Source Code**: `/home/hanzfx/courier_tracking`
    *   **Virtualenv**: `/home/hanzfx/.virtualenvs/.venv`
4.  **Edit WSGI File**:
    *   In the Web tab, click the link to your **WSGI configuration file**.
    *   Replace everything inside with:
        ```python
        import os
        import sys

        path = '/home/hanzfx/courier_tracking'
        if path not in sys.path:
            sys.path.append(path)

        os.environ['DJANGO_SETTINGS_MODULE'] = 'courier_tracking.settings'

        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        ```
5.  **Static Files**:
    *   Go to the **Web** tab -> **Static files** section.
    *   Add two entries:
        *   URL: `/static/` | Path: `/home/hanzfx/courier_tracking/static/`
        *   URL: `/media/` | Path: `/home/hanzfx/courier_tracking/media/`
6.  **Database & Admin**:
    *   In the Bash console, run:
        ```bash
        python manage.py migrate
        python manage.py createsuperuser
        ```
7.  **Reload**:
    *   Go back to the **Web** tab and click **Reload hanzfx.pythonanywhere.com**.

> [!IMPORTANT]
> Ensure `ALLOWED_HOSTS` in `settings.py` is set to `['hanzfx.pythonanywhere.com']` before pushing to GitHub.
