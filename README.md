# 🛡️ Easy Tracker - Vulnerability Management Dashboard

Easy Tracker is a lightweight, secure web application designed for Security Operations Centers (SOCs) and IT administrators to report, track, and manage cybersecurity vulnerabilities. 

This project was built from scratch using **Flask**, **Flask-SQLAlchemy (SQLite)**, and **Bootstrap 5**.

## 🚀 Features
- **Full CRUD Operations:** Create, Read, Update (change status to 'In Progress' or 'Resolved'), and Delete vulnerabilities.
- **Search & Filter:** Dynamic search bar and severity-based dropdown filters.
- **Metrics Bar:** Automated calculations for total logged issues, urgent items, and remediation progress rates.
- **Security Hardening:** Server-side input sanitization protecting the application from **Stored Cross-Site Scripting (XSS)**.

---

## 🔒 Cybersecurity Implementation (XSS Defense)
To prevent malicious script injection (Stored XSS), the application utilizes Python's built-in `html` library to sanitize user-provided titles and descriptions before database storage:
```python
clean_title = html.escape(raw_title)
clean_description = html.escape(raw_description)