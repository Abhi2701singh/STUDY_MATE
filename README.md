# 📚 StudyMate - Engineering Notes & Quantum Series Platform

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-success?style=for-the-badge&logo=vercel)](https://studymate-tawny.vercel.app)
[![Django](https://img.shields.io/badge/Django-5.0.6-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> A modern, elegant, and community-driven engineering notes management platform. Built to simplify university exam prep with organized lecture notes, unit-wise questions, and previous year Quantum series question banks.

🌐 **Live 24/7 Production URL**: [https://studymate-tawny.vercel.app](https://studymate-tawny.vercel.app)

---

## 🌟 Key Features

### 🎨 Modern & Responsive UI/UX
- **Glassmorphic Navigation**: Sleek translucent navbar with active page indicators, profile status pill, and responsive mobile drawer.
- **Hero Section & Live Statistics**: Dynamic counters for total uploaded notes, subjects, academic years, and quantum series.
- **Vibrant Year Cards**: Custom 3D hover effects with distinct gradient branding for **1st, 2nd, 3rd, 4th Year** and **Quantum Series**.
- **Real-Time Client Search**: Instant search filtering on notes pages without reloading.

### ⚡ Streamlined Admin & Note Upload Workflow
- **Interactive Upload Interface (`/add-note/`)**:
  - **Smart Subject Selector**: Pick from existing subjects via dropdown or create a new subject in 1 click.
  - **Dynamic Cascading Chapters**: Automatically fetches unit chapters for the selected subject via API (`/api/chapters/<subject_id>/`).
  - **Modern Drag & Drop Dropzone**: Drag and drop PDF, DOCX, PPTX, or ZIP files with live file size and name badges.
  - **Quantum Series Toggle**: Dedicated switcher to upload university Quantum materials effortlessly.
- **Enhanced Django Admin Console (`/admin/`)**:
  - **Inline Management**: Add and preview chapters directly inside subjects, and notes directly inside chapters.
  - **Auto-Assigned Uploader**: Automatically defaults `uploaded_by` to the logged-in administrator.
  - **Rich Badges & Actions**: Year-coded pill badges, direct file download links, and deep search filters.

---

## 🛠️ Tech Stack

- **Backend Framework**: [Django 5.0.6](https://djangoproject.com) (Python 3.12)
- **Frontend**: HTML5, Modern CSS3 with Custom Design System, Bootstrap 5.3, FontAwesome 6, Google Fonts (*Plus Jakarta Sans*)
- **Database**: SQLite3 (Local & Serverless Compatible) / PostgreSQL Ready
- **Static Files Serving**: [WhiteNoise](http://whitenoise.evans.io/)
- **WSGI Production Server**: Gunicorn
- **Deployment**: [Vercel](https://vercel.com) & [Render](https://render.com) (Configurations included)

---

## 📂 Project Structure

```text
STUDY_MATE/
├── build.sh                  # Production build script
├── Procfile                  # Gunicorn web process definition
├── render.yaml               # 1-Click Render blueprint configuration
├── vercel.json               # Vercel serverless deployment config
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
├── db.sqlite3                # SQLite database
│
├── studymate/                # Core Django project configuration
│   ├── settings.py           # Application settings & WhiteNoise config
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI application entrypoint
│   └── asgi.py               # ASGI application entrypoint
│
├── notes/                    # Notes application module
│   ├── admin.py              # Customized admin site & inlines
│   ├── models.py             # Subject, Chapter, and Note models
│   ├── urls.py               # Notes & API routes
│   └── views.py              # Views, search logic & API handlers
│
├── static/                   # Static assets
│   ├── css/
│   │   ├── style.css         # Modern design system & custom styles
│   │   └── custom_admin.css  # Sleek Django admin portal styling
│   └── js/
│       └── main.js           # Client-side dynamic filters & dropzone logic
│
└── templates/                # Responsive HTML templates
    ├── base.html             # Base layout with navbar & footer
    ├── home.html             # Landing page with search & year cards
    ├── add_note.html         # Intuitive multi-mode note upload form
    ├── year_view.html        # Academic year-wise notes browser
    ├── quantum.html          # Quantum series questions bank
    ├── subject_notes.html    # Specific subject notes view
    ├── login.html            # User & admin sign in
    ├── signup.html           # User registration
    └── admin/
        └── base_site.html    # Branded custom admin header & shortcuts
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/Abhi2701singh/STUDY_MATE.git
cd STUDY_MATE
```

### 2. Create and activate a Virtual Environment
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Web App**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## ☁️ Deployment

This project comes pre-configured for both **Vercel** and **Render**:

### Vercel Deployment (Live 24/7)
Deploy in one command with the Vercel CLI:
```bash
npx vercel --prod
```

### Render Deployment
1. Connect your repository to [Render Dashboard](https://dashboard.render.com).
2. Render automatically recognizes `render.yaml` and `build.sh` for 1-click hosting with automated SSL and zero config!

---

## 👨‍💻 Author & Contributions

Developed by **Abhinav Singh**
- GitHub: [@Abhi2701singh](https://github.com/Abhi2701singh)
- Email: [studymate.support@gmail.com](mailto:studymate.support@gmail.com)

Feel free to fork this project, submit pull requests, or open an issue for improvements!
