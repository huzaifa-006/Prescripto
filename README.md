# Prescripto - Digital Prescription Management System

A Django web application for doctors to generate digital prescription slips.

**Live URL:** https://huzaifa05.pythonanywhere.com

---

## Features

- ✅ Patient management with unique IDs (PT-XXXXX)
- ✅ Medicine database (52+ medicines pre-loaded)
- ✅ Lab tests database (33+ tests pre-loaded)
- ✅ Prescription creation with dosage timing (Morning/Afternoon/Evening/Night)
- ✅ Print-friendly prescription slips
- ✅ Duplicate patient detection for returning patients
- ✅ Search patients by name, ID, or phone number

---

## How to Run Locally

```bash
# 1. Navigate to project folder
cd /Users/huzaifa/Downloads/Huzaifa/My\ Projects/Prescripto

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run the server
python manage.py runserver

# 4. Open in browser
# http://127.0.0.1:8000
```

---

## How to Update the Live Website

### Step 1: Make Your Changes
Edit files on your computer as needed.

### Step 2: Push to GitHub
```bash
cd /Users/huzaifa/Downloads/Huzaifa/My\ Projects/Prescripto
git add .
git commit -m "Describe your changes here"
git push
```

### Step 3: Update PythonAnywhere
1. Log in to https://www.pythonanywhere.com
2. Go to **Consoles** → Open **Bash**
3. Run:
```bash
cd ~/Prescripto
git pull
python manage.py collectstatic --noinput
```
4. Go to **Web** tab → Click **Reload** (green button)

---

## Important: Keep Website Active

PythonAnywhere free tier requires you to log in **once a month** and click the "Run until 1 month from today" button on the Web tab. They'll email you a week before as a reminder.

---

## Project Structure

```
Prescripto/
├── clinic/                 # Main app
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── forms.py           # Form definitions
│   ├── urls.py            # URL routing
│   └── management/        # Custom commands (seed_data)
├── templates/clinic/       # HTML templates
├── static/                # CSS and JavaScript
├── prescripto/            # Django project settings
└── requirements.txt       # Python dependencies
```

---

## Credentials

- **GitHub:** https://github.com/huzaifa-006/Prescripto
- **PythonAnywhere:** https://huzaifa05.pythonanywhere.com

---

## Built With

- Django 4.2
- Python 3.10
- SQLite Database
- WhiteNoise (static files)

---

## Created

February 2, 2026
