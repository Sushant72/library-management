# Library Management Web Application

A Django-based web application that helps librarians manage books, members, and book borrowing/return transactions. This app also supports importing books from the [Frappe Library API](https://frappe.io/api/method/frappe-library).

---

## Features

* Add, view, and search books
* Add and manage members
* Issue books to members
* Return books and update stock
* Block members with ₹500+ debt
* Import books using an external API
* Admin panel with full control

---

## Tech Stack

* **Backend:** Django (Python)
* **Frontend:** Django Templates + Bootstrap 5
* **Database:** SQLite (default)
* **API:** Frappe Library API

---

## Project Structure

```
library-management/
├── env/                        # Virtual environment
├── library_project/           # Django settings and URLs
├── library/                   # Main app (models, views, templates)
│   ├── static/library/        # CSS styling
│   └── templates/library/     # HTML templates
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django CLI entry
```


## Admin Panel
    Access: http://127.0.0.1:8000/admin/

    Manage books, members, and transactions with a GUI



