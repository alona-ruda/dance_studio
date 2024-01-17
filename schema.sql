DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS dance_classes;
DROP TABLE IF EXISTS teacher_classes;

CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL
);


CREATE TABLE dance_classes (
    dance_class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dance_class_name VARCHAR(50) NOT NULL,
    dance_class_about TEXT
);

CREATE TABLE teacher_classes (
    teacher_id INTEGER,
    dance_class_id INTEGER,
    PRIMARY KEY (teacher_id, dance_class_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (dance_class_id) REFERENCES dance_classes(dance_class_id)
);
