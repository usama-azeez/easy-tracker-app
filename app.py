from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # <-- Added SQLAlchemy import

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

@app.route('/')
def home():
    # Query all vulnerabilities from our database (currently empty)
    vulns = Vulnerability.query.all()
    # Pass the vulnerabilities list into the HTML template
    return render_template('index.html', vulns=vulns)

if __name__ == '__main__':
    app.run(debug=True, port=5001)