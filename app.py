from flask import Flask, render_template  # <-- Added render_template import

app = Flask(__name__)

@app.route('/')
def home():
    # Render and display the templates/index.html file
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)