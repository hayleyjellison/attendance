from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()
db = SQLAlchemy()

app = Flask(__name__)

bootstrap.init_app(app)
# db.init_app(app)

# this is a 'view'
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/student')
def student():
    return render_template('student.html')