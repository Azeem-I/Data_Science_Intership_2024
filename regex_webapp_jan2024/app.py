from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    test_string = request.form['test_string']
    regex = request.form['regex']
    matched_strings = re.findall(regex, test_string)
    return render_template('results.html', matched_strings=matched_strings)

@app.route('/validate-email', methods=['POST'])
def validate_email():
    email = request.form['email']
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return render_template('email_valid.html', valid=True)
    else:
        return render_template('email_valid.html', valid=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
