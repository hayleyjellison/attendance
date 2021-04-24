CREATE TABLE IF NOT EXISTS user(
    id serial PRIMARY KEY,
    first_name varchar(20) NOT NULL,
    last_name varchar(20) NOT NULL,
    email varchar(50) NOT NULL,
    pwd varchar(20) NOT NULL,
    role varchar(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS class(
    id serial PRIMARY KEY,
    class_name varchar(20) NOT NULL,
    section varchar(5) NOT NULL,
    start_time time without timezone NOT NULL,
    end_time time without timezone NOT NULL
);

CREATE TABLE IF NOT EXISTS teacherclass(
    teacher_id serial FOREIGN KEY,
    class_id serial FOREIGN KEY
);

CREATE TABLE IF NOT EXISTS studentclass(
    student_id serial FOREIGN KEY,
    class_id serial FOREIGN KEY
);

CREATE TABLE IF NOT EXISTS studentattendance(
    student_id serial FOREIGN KEY,
    class_id serial FOREIGN KEY,
    date datetime NOT NULL,
    present boolean
);