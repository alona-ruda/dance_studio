import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
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


def get_teacher_detail(teacher_id):
    conn = get_db_connection()
    teacher = conn.execute('''
        SELECT teachers.teacher_id, teachers.name, teachers.surname, 
        GROUP_CONCAT(dance_classes.dance_class_name) as class_names
        FROM teachers 
        LEFT JOIN teacher_classes ON teachers.teacher_id = teacher_classes.teacher_id
        LEFT JOIN dance_classes ON teacher_classes.dance_class_id = dance_classes.dance_class_id
        WHERE teachers.teacher_id = ?
        GROUP BY teachers.teacher_id
    ''', (teacher_id,)).fetchall()
    conn.close()
    if teacher is None:
        abort(404)
    return teacher


def get_dance_class(dance_class_id):
    conn = get_db_connection()
    dance_class = conn.execute('SELECT * FROM dance_classes WHERE dance_class_id = ?',
                               (dance_class_id,)).fetchone()
    conn.close()
    if dance_class is None:
        abort(404)
    return dance_class


def get_dance_classes_for_navbar():
    conn = get_db_connection()
    dance_classes = conn.execute('SELECT * FROM dance_classes').fetchall()
    conn.close()
    return dance_classes


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    dance_classes = get_dance_classes_for_navbar()
    return render_template('index.html', dance_classes=dance_classes)


@app.route('/teachers')
def teachers():
    dance_classes = get_dance_classes_for_navbar()
    conn = get_db_connection()
    teachers = conn.execute('SELECT * FROM teachers').fetchall()
    conn.close()
    return render_template('teachers.html', teachers=teachers, dance_classes=dance_classes)


@app.route('/teacher/<int:teacher_id>')
def teacher(teacher_id):
    dance_classes = get_dance_classes_for_navbar()
    teacher = get_teacher_detail(teacher_id)
    return render_template('teacher.html', teacher=teacher, dance_classes=dance_classes)


@app.route('/create_teacher', methods=('GET', 'POST'))
def create_teacher():
    dance_classes = get_dance_classes_for_navbar()

    conn = get_db_connection()
    dance_classes_form = conn.execute('SELECT dance_class_id, dance_class_name FROM dance_classes').fetchall()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        selected_classes = request.form.getlist('dance_classes_form')

        if not name:
            flash('Name is required!')
        elif not surname:
            flash('Surname is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO teachers (name, surname) VALUES (?, ?)', (name, surname))
            new_teacher_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

            for dance_class_id in selected_classes:
                conn.execute('INSERT INTO teacher_classes (teacher_id, dance_class_id) VALUES (?, ?)',
                             (new_teacher_id, dance_class_id))

            conn.commit()
            conn.close()
            return redirect(url_for('teachers'))
    return render_template('create_teacher.html', dance_classes=dance_classes, dance_classes_form=dance_classes_form)


@app.route('/teacher/<int:teacher_id>/edit', methods=('GET', 'POST'))
def edit_teacher(teacher_id):
    dance_classes = get_dance_classes_for_navbar()
    teacher = get_teacher(teacher_id)
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        if not name:
            flash('Name is required!')
        elif not surname:
            flash('Surname is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE teachers SET name = ?, surname = ?'
                         ' WHERE teacher_id = ?',
                         (name, surname, teacher_id))
            conn.commit()
            conn.close()
            return redirect(url_for('teachers'))
    return render_template('edit_teacher.html', teacher=teacher, dance_classes=dance_classes)


@app.route('/teacher/<int:teacher_id>/delete', methods=('POST',))
def delete_teacher(teacher_id):
    dance_classes = get_dance_classes_for_navbar()
    teacher = get_teacher(teacher_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM teachers WHERE teacher_id = ?', (teacher_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(teacher['name']))
    return redirect(url_for('teachers', dance_classes=dance_classes))


@app.route('/class/<int:dance_class_id>')
def dance_class(dance_class_id):
    dance_classes = get_dance_classes_for_navbar()
    dance_class = get_dance_class(dance_class_id)
    return render_template('class.html', dance_class=dance_class, dance_classes=dance_classes)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
