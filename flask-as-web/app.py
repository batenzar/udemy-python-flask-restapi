from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Getting html file from './templates' folder
    # RULE: The directory must be 'templates'. 
    return render_template('index.html')

app.run(port=5000)
    