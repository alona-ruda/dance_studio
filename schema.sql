
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS days;
DROP TABLE IF EXISTS teacher_days;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS teacher_classes;

CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL
);

CREATE TABLE days (
    day_id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_name VARCHAR(15) NOT NULL
);

CREATE TABLE teacher_days (
    teacher_id INTEGER,
    day_id INTEGER,
    PRIMARY KEY (teacher_id, day_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (day_id) REFERENCES days(day_id)
);

CREATE TABLE classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name VARCHAR(50) NOT NULL
);

CREATE TABLE teacher_classes (
    teacher_id INTEGER,
    class_id INTEGER,
    PRIMARY KEY (teacher_id, class_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);
