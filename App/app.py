from flask import Flask 
app = Flask(__name__)

@app.route('/')
def login():
    return "Hello!"

@app.route('/teacher')
def teacher():
    return "Hello Teacher!"

@app.route('/student')
def student():
    return "Hello Student!"