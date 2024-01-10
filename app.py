import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_teacher(teacher_id):
    conn = get_db_connection()
    teacher = conn.execute('SELECT * FROM teachers WHERE teacher_id = ?',
                        (teacher_id,)).fetchone()
    conn.close()
    if teacher is None:
        abort(404)
    return teacher


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teachers')
def teachers():
    conn = get_db_connection()
    teachers = conn.execute('SELECT * FROM teachers').fetchall()
    conn.close()
    return render_template('teachers.html', teachers=teachers)


@app.route('/teacher/<int:teacher_id>')
def teacher(teacher_id):
    teacher = get_teacher(teacher_id)
    return render_template('teacher.html', teacher=teacher)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
