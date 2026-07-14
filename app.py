from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import html

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


# 1. READ Route: Display all vulnerabilities (with Search & Filter)
@app.route('/')
def home():
    # Grab optional filters from the URL query parameters
    search_query = request.args.get('search', '')
    severity_filter = request.args.get('severity', '')

    # Begin database query
    query = Vulnerability.query

    # If the user typed a search term, filter titles containing that term
    if search_query:
        query = query.filter(Vulnerability.title.contains(search_query))
    
    # If the user selected a specific severity, filter by that severity
    if severity_filter:
        query = query.filter(Vulnerability.severity == severity_filter)

    # Execute the final query
    vulns = query.all()

    # Render template and pass back search terms to keep them in the inputs
    return render_template('index.html', vulns=vulns, search_query=search_query, severity_filter=severity_filter)

# 2. CREATE Route: Handle form submission and save to SQLite
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    severity = request.form.get('severity')

    new_vuln = Vulnerability(
        title=title, 
        description=description, 
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