from .app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(16))
    last_name = db.Column(db.String(16))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(64))
    role = db.Column(db.String(16))
    classes_teacher = relationship("TeacherClass")
    classes_student = relationship("StudentClass")
    student_attendance = relationship("StudentAttendance")

class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(16))
    section = db.Column(db.String(4))
    start_time = db.Column(db.Time(timezone=False))
    end_time = db.Column(db.Time(timezone=False))
    class_teach = relationship("TeacherClass")
    class_student = relationship("StudentClass")
    student_attend = relationship("StudentAttendance")

class TeacherClass(db.Model):
    __tablename__ = 'teacherclass'
    teacher_id = db.Column(db.Integer, ForeignKey('user.id'))
    class_id = db.Column(db.Integer, ForeignKey('class.id'))

class StudentClass(db.Model):
    __tablename__ = 'studentclass'
    student_id = db.Column(db.Integer, ForeignKey('user.id'))
    class_id = db.Column(db.Integer, ForeignKey('class.id'))

class StudentAttendance(db.Model):
    __tablename__ = 'studentattendance'
    student_id = db.Column(db.Integer, ForeignKey('user.id'))
    class_id = db.Column(db.Integer, ForeignKey('class.id'))
    date = db.Column(db.Datetime(timezone=False))
    present db.Column(db.Boolean())