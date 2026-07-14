from flask import Flask, render_template, request, redirect, url_for  # <-- Added request, redirect, and url_for imports
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the Database helper
db = SQLAlchemy(app)

# Database Table Structure (Vulnerability Model)
class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default="Medium")
    status = db.Column(db.String(20), default="Open")

# Automatically build the database table on startup
with app.app_context():
    db.create_all()

# 1. READ Route: Display all vulnerabilities
@app.route('/')
def home():
    vulns = Vulnerability.query.all()
    return render_template('index.html', vulns=vulns)

# 2. CREATE Route: Handle form submission and save to SQLite
@app.route('/add', methods=['POST'])
def add():
    # Grab data sent from the form inputs
    title = request.form.get('title')
    description = request.form.get('description')
    severity = request.form.get('severity')

    # Construct database object (default status is "Open")
    new_vuln = Vulnerability(
        title=title, 
        description=description, 
        severity=severity, 
        status="Open"
    )

    # Save to SQLite Database
    db.session.add(new_vuln)
    db.session.commit()

    # Redirect user back to the homepage to see their new issue listed
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)