# StudyMate - Quick Reference Guide
## प्रोजेक्ट की Quick जानकारी

---

## 🎯 प्रोजेक्ट क्या है?
**StudyMate** एक Engineering Notes Management System है जहाँ:
- Students अपने notes देख और download कर सकते हैं
- Faculty members notes upload कर सकते हैं
- Notes year-wise और subject-wise organize होते हैं
- Quantum notes के लिए separate section है

---

## 🛠️ Technology Stack (संक्षेप में)

| Component | Technology |
|-----------|-----------|
| **Backend** | Django 5.0.6 (Python) |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3, Bootstrap 5.3.0 |
| **Icons** | Font Awesome 6.0.0 |
| **Deployment** | Vercel |

---

## 📁 Main Files और उनका काम

### Backend Files
- **`notes/models.py`** - Database tables (Subject, Chapter, Note)
- **`notes/views.py`** - सभी pages का logic (10+ functions)
- **`notes/urls.py`** - URL routing (कौन सा URL किस function को call करे)
- **`notes/admin.py`** - Admin panel configuration
- **`studymate/settings.py`** - Project settings (database, media files, etc.)

### Frontend Files
- **`templates/base.html`** - सभी pages का base template (navbar, footer)
- **`templates/home.html`** - Home page (year cards)
- **`templates/year_view.html`** - Year-wise notes display
- **`templates/quantum.html`** - Quantum notes page
- **`templates/add_note.html`** - Note upload form
- **`static/css/style.css`** - Custom styling

---

## 🗄️ Database Structure (3 Main Tables)

### 1. Subject Table
```
- name (subject का नाम)
- year (1, 2, 3, या 4)
- image (subject की image, optional)
- is_quantum (True/False - quantum है या नहीं)
```

### 2. Chapter Table
```
- name (chapter का नाम)
- subject (किस subject का है - Foreign Key)
- image (chapter की image, optional)
```

### 3. Note Table
```
- title (note का title)
- chapter (किस chapter का है - Foreign Key)
- file (PDF file)
- uploaded_by (किसने upload किया - User Foreign Key)
- upload_date (कब upload हुआ - automatically)
```

**Relationship:**
```
Subject (1) → (Many) Chapter (1) → (Many) Note
```

---

## 🔑 Main Features

### 1. User Authentication
- ✅ Sign Up (registration)
- ✅ Login
- ✅ Logout
- ✅ Session management

### 2. Note Viewing (सभी users)
- ✅ Home page - recent notes
- ✅ Year-wise notes (1st, 2nd, 3rd, 4th Year)
- ✅ Quantum notes section
- ✅ Subject-specific notes
- ✅ Download notes (PDF files)

### 3. Note Management (Staff Only)
- ✅ Upload regular notes
- ✅ Upload quantum notes
- ✅ Delete notes
- ✅ Admin panel access

### 4. File Management
- ✅ Image upload (subject & chapter images)
- ✅ PDF upload (note files)
- ✅ File download
- ✅ File deletion

---

## 👥 User Roles

### Regular User (Student)
**कर सकते हैं:**
- Notes देखना
- Notes download करना
- Account बनाना
- Login/Logout करना

**नहीं कर सकते:**
- Notes upload करना
- Notes delete करना
- Admin panel access

### Staff User (Faculty/Admin)
**कर सकते हैं:**
- सब कुछ जो regular user कर सकता है
- Notes upload करना
- Notes delete करना
- Admin panel access

---

## 🌐 Important URLs

| URL | क्या करता है | Access |
|-----|-------------|--------|
| `/` | Home page | Public |
| `/year/1/` | 1st Year notes | Public |
| `/year/2/` | 2nd Year notes | Public |
| `/year/3/` | 3rd Year notes | Public |
| `/year/4/` | 4th Year notes | Public |
| `/quantum/` | Quantum notes | Public |
| `/login/` | Login page | Public |
| `/signup/` | Registration | Public |
| `/add-note/` | Upload note | Staff only |
| `/add-quantum-note/` | Upload quantum note | Staff only |
| `/delete-note/<id>/` | Delete note | Staff only |
| `/admin/` | Admin panel | Staff only |

---

## 📊 Project Structure (संक्षेप)

```
studymate/
├── manage.py                    # Django management
├── db.sqlite3                   # Database file
├── requirements.txt            # Dependencies
│
├── studymate/                  # Main project
│   ├── settings.py             # Settings
│   └── urls.py                 # Main URLs
│
├── notes/                      # Main app
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── urls.py                 # App URLs
│   └── admin.py                # Admin config
│
├── templates/                   # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── year_view.html
│   └── ...
│
└── media/                       # Uploaded files
    ├── notes/                  # PDF files
    ├── chapter_images/         # Chapter images
    └── subject_images/         # Subject images
```

---

## 🔄 How It Works (कैसे काम करता है)

### Note Upload Process:
1. Staff user "Add Note" button click करता है
2. Form fill करता है (title, year, subject, chapter, file)
3. Form submit होता है
4. System automatically:
   - Subject create करता है (अगर नहीं है)
   - Chapter create करता है (अगर नहीं है)
   - File को `media/notes/` में save करता है
   - Database में record create करता है
5. User को home page पर redirect करता है

### Note Viewing Process:
1. User home page पर जाता है
2. Year card click करता है (जैसे "1st Year")
3. System उस year के सभी subjects fetch करता है
4. हर subject के notes display होते हैं
5. User download button click करके PDF download कर सकता है

---

## 🎨 UI Components

### Home Page Sections:
1. **Hero Section** - Title और tagline
2. **Year Cards** - 5 cards (1st, 2nd, 3rd, 4th Year, Quantum)
3. **Features Section** - 3 features display
4. **Footer** - Links और contact info

### Year View Page:
- **Subject Cards** - हर subject एक card में
- **Notes Grid** - 5 columns में notes display
- **Note Cards** - Image, title, download button

### Navigation Bar:
- Year links (1st, 2nd, 3rd, 4th)
- Quantum link
- Login/Logout/Signup
- Add Note buttons (staff only)

---

## 🔐 Security Features

1. **Authentication**: Login required for certain pages
2. **Authorization**: Staff-only access for upload/delete
3. **CSRF Protection**: All forms में CSRF token
4. **Password Hashing**: Argon2 algorithm
5. **Session Management**: Django sessions

---

## 📝 Key Functions (views.py में)

| Function | क्या करता है |
|----------|-------------|
| `home()` | Home page display करता है |
| `year_notes()` | Year-wise notes show करता है |
| `quantum()` | Quantum notes show करता है |
| `add_note()` | Regular note upload |
| `add_quantum_note()` | Quantum note upload |
| `delete_note()` | Note delete करता है |
| `signup()` | User registration |
| `subject_notes()` | Subject-specific notes |

---

## 🚀 Deployment

- **Platform**: Vercel
- **Config File**: `vercel.json`
- **Runtime**: Python 3.12
- **WSGI**: `studymate/wsgi.py`

---

## 📦 Dependencies (Main)

- Django 5.0.6
- Pillow 10.4.0 (images के लिए)
- WhiteNoise (static files के लिए)
- Bootstrap 5.3.0 (CDN)
- Font Awesome 6.0.0 (CDN)

---

## 💡 Important Points for Report

### 1. Project Type
- Web Application
- Learning Management System (LMS)
- File Management System

### 2. Architecture
- Model-View-Template (MVT) pattern
- Django framework
- SQLite database

### 3. Main Functionality
- CRUD operations (Create, Read, Delete)
- File upload/download
- User authentication
- Role-based access control

### 4. Technologies Used
- Backend: Python, Django
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Database: SQLite
- Deployment: Vercel

### 5. Key Features
- Year-wise organization
- Subject-wise categorization
- Quantum notes section
- Image support
- Responsive design
- Staff-only upload/delete

---

## 📋 Report में Include करने वाले Sections

1. **Introduction**
   - Project overview
   - Objectives
   - Scope

2. **System Analysis**
   - Requirements
   - Use cases
   - User roles

3. **System Design**
   - Architecture
   - Database design
   - UI/UX design

4. **Implementation**
   - Technology stack
   - Features implementation
   - Code structure

5. **Testing**
   - Functionality testing
   - User testing

6. **Deployment**
   - Deployment process
   - Configuration

7. **Conclusion**
   - Summary
   - Future enhancements

---

## 🎓 Project Report के लिए Tips

1. **Screenshots लें:**
   - Home page
   - Year view pages
   - Upload form
   - Admin panel

2. **Diagrams बनाएं:**
   - Database ER diagram
   - System architecture
   - User flow diagram

3. **Code Examples:**
   - Models code
   - Views code
   - URL patterns

4. **Features List:**
   - सभी features को detail में explain करें

5. **Challenges & Solutions:**
   - Development में आई problems
   - उनके solutions

---

**Note**: Complete detailed report `PROJECT_REPORT.md` file में है जिसमें हर point detail में explain किया गया है।


