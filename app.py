from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import html  # Python's built-in HTML sanitizer

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

# 1. READ Route: Display all vulnerabilities (with Search, Filter, and Metrics)
@app.route('/')
def home():
    search_query = request.args.get('search', '')
    severity_filter = request.args.get('severity', '')

    query = Vulnerability.query

    if search_query:
        query = query.filter(Vulnerability.title.contains(search_query))
    if severity_filter:
        query = query.filter(Vulnerability.severity == severity_filter)

    vulns = query.all()

    # --- CALCULATE METRICS ---
    total_count = Vulnerability.query.count()
    resolved_count = Vulnerability.query.filter_by(status="Resolved").count()
    remediation_rate = int((resolved_count / total_count) * 100) if total_count > 0 else 0
    urgent_count = Vulnerability.query.filter(Vulnerability.severity.in_(['High', 'Critical']), Vulnerability.status != 'Resolved').count()

    return render_template(
        'index.html', 
        vulns=vulns, 
        search_query=search_query, 
        severity_filter=severity_filter,
        total_count=total_count,
        remediation_rate=remediation_rate,
        urgent_count=urgent_count
    )

# 2. CREATE Route: Handle form submission with Input Sanitization (XSS Prevention)
@app.route('/add', methods=['POST'])
def add():
    raw_title = request.form.get('title', '')
    raw_description = request.form.get('description', '')
    severity = request.form.get('severity', 'Medium')

    # Sanitization layer
    clean_title = html.escape(raw_title)
    clean_description = html.escape(raw_description)

    new_vuln = Vulnerability(
        title=clean_title, 
        description=clean_description, 
        severity=severity, 
        status="Open"
    )

    db.session.add(new_vuln)
    db.session.commit()
    return redirect(url_for('home'))

# 3. UPDATE Route: Mark as "In Progress"
@app.route('/start/<int:id>')
def start(id):
    vuln = db.get_or_404(Vulnerability, id)
    vuln.status = "In Progress"
    db.session.commit()
    return redirect(url_for('home'))

# 4. UPDATE Route: Mark as "Resolved"
@app.route('/resolve/<int:id>')
def resolve(id):
    vuln = db.get_or_404(Vulnerability, id)
    vuln.status = "Resolved"
    db.session.commit()
    return redirect(url_for('home'))

# 5. DELETE Route: Remove the record
@app.route('/delete/<int:id>')
def delete(id):
    vuln = db.get_or_404(Vulnerability, id)
    db.session.delete(vuln)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)