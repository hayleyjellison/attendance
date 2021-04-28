import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import sqlite3 as sql
from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/Attendance.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
User_data = Base.classes.user
Class_data = Base.classes.classes
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "C:\\Users\\hayleyjellison\\Desktop\\Presidio\\attendance-test\\Belly_Button_Biodiversity\\db\\Attendance.sqlite")

def validate(username, password):
    con = sql.connect(db_path)
    completion = False
    pos = ''
    with con:
                cur = con.cursor()
                sel = [
                    User_data.user_id,
                    User_data.first_name,
                    User_data.last_name,
                    User_data.email,
                    User_data.password,
                    User_data.role
                ]
                cur.execute("SELECT * FROM user")
                rows = cur.fetchall()
                results = db.session.query(*sel).filter(User_data.email == username).all()
                for row in results:
                    dbID = row[0]
                    dbUser = row[3]
                    dbPass = row[4]
                    dbRole = row[5]
                    if dbUser==username and dbPass==password and dbRole=="Teacher":
                        completion=True
                        pos="Teacher"
                    elif dbUser==username and dbPass==password and dbRole=="Student":
                        completion=True
                        pos='Student'
    return completion, pos 

def getID(username):
    con = sql.connect(db_path)
    with con:
                cur = con.cursor()
                sel = [
                    User_data.user_id,
                    User_data.first_name,
                    User_data.last_name,
                    User_data.email,
                    User_data.password,
                    User_data.role
                ]
                cur.execute("SELECT * FROM user")
                rows = cur.fetchall()
                results = db.session.query(*sel).filter(User_data.email == username).all()
                for row in results:
                    dbID = row[0]
    return dbID

def getClassName(class_id):
    con = sql.connect(db_path)
    with con:
                cur = con.cursor()
                sel = [
                    Class_data.class_id,
                    Class_data.class_name,
                    Class_data.section,
                    Class_data.start_time,
                    Class_data.end_time
                ]
                cur.execute("SELECT * FROM classes")
                rows = cur.fetchall()
                results = db.session.query(*sel).filter(User_data.email == username).all()
                for row in results:
                    dbClassName = row[1]
    return dbClassName

def get_db_connection():
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    return con

@app.route("/", methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        completion,pos = validate(email, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            if pos == "Teacher":
                return redirect(url_for('teacher',tid=getID(email)))
            elif pos == "Student":
                return redirect(url_for('student',sid=getID(email)))
    return render_template('index.html', error=error)

@app.route('/teacher/<tid>')
def teacher(tid):
    conn = get_db_connection()
    teacherclass = conn.execute(f"SELECT * FROM classes WHERE teacher_id = {tid}").fetchall()
    class_name=conn.execute(f"SELECT * FROM classes WHERE class_id IN (SELECT class_id FROM teacherclass WHERE teacher_id = {tid})").fetchall()
    class_attendance=conn.execute(f"SELECT * FROM studentattendance WHERE class_id IN (SELECT class_id FROM teacherclass WHERE teacher_id = {tid})").fetchall()
    # num_attend =conn.execute(f"SELECT AVG(present) AS AVG FROM studentattendance WHERE class_id IN (SELECT class_id FROM studentclass WHERE student_id = {sid})").fetchall()
    num_attend = []
    for clss in teacherclass:
        temp =conn.execute(f"SELECT AVG(present) AS AVG FROM studentattendance WHERE class_id = {clss['class_id']}").fetchall()
        num_attend.append(temp[0]['AVG']*100)
    conn.close()
    names = []
    for clss in teacherclass:
        temp = {}
        temp['class'] = clss['class_name']
        names.append(temp)
    attendance = []

    print(names, num_attend)
    class_list = {'class_name':names,'attendance':num_attend}
    print(class_list)
    n = len(class_list)
    return render_template('teacher.html', teacherclass=teacherclass,class_attendance=class_attendance,num_attend=num_attend,class_list=class_list,n=n)


@app.route('/student/<sid>')
def student(sid):
    conn = get_db_connection()
    studentclass = conn.execute(f"SELECT class_id FROM studentclass WHERE student_id = {sid}")
    class_name=conn.execute(f"SELECT * FROM classes WHERE class_id IN (SELECT class_id FROM studentclass WHERE student_id = {sid})").fetchall()
    class_attendance=conn.execute(f"SELECT * FROM studentattendance WHERE class_id IN (SELECT class_id FROM studentclass WHERE student_id = {sid})").fetchall()
    # num_attend =conn.execute(f"SELECT AVG(present) AS AVG FROM studentattendance WHERE class_id IN (SELECT class_id FROM studentclass WHERE student_id = {sid})").fetchall()
    num_attend = []
    for clss in class_name:
        temp =conn.execute(f"SELECT AVG(present) AS AVG FROM studentattendance WHERE class_id = {clss['class_id']} AND student_id = {sid}").fetchall()
        num_attend.append(temp[0]['AVG']*100)
    conn.close()
    names = []
    for clss in class_name:
        temp = {}
        temp['class'] = clss['class_name']
        names.append(temp)
    attendance = []
    section = []
    for clss in class_name:
        temp={}
        temp['class_section'] = clss['section']
        section.append(temp)

    print(names, num_attend,section)
    class_list = {'class_name':names,'attendance':num_attend,'class_section':section}
    print(class_list)
    n = len(class_list)
    return render_template('student.html', class_name=class_name,class_attendance=class_attendance,num_attend=num_attend,class_list=class_list,n=n,section=section)


if __name__ == "__main__":
    app.run()
