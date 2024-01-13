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


def get_dance_class(dance_class_id):
    conn = get_db_connection()
    dance_class = conn.execute('SELECT * FROM dance_classes WHERE dance_class_id = ?',
                        (dance_class_id,)).fetchone()
    conn.close()
    if dance_class is None:
        abort(404)
    return dance_class


def get_dance_class_by_name(dance_class_name):
    conn = get_db_connection()
    dance_class = conn.execute('SELECT * FROM dance_classes WHERE dance_class_name = ?',
                        (dance_class_name,)).fetchone()
    conn.close()
    if dance_class is None:
        abort(404)
    return dance_class


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


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


@app.route('/create_teacher', methods=('GET', 'POST'))
def create_teacher():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']

        if not name:
            flash('Name is required!')
        elif not surname:
            flash('Surname is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO teachers (name, surname) VALUES (?, ?)',
                         (name, surname))
            conn.commit()
            conn.close()
            return redirect(url_for('teachers'))

    return render_template('create_teacher.html')


@app.route('/teacher/<int:teacher_id>/edit', methods=('GET', 'POST'))
def edit_teacher(teacher_id):
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

    return render_template('edit_teacher.html', teacher=teacher)


@app.route('/teacher/<int:teacher_id>/delete', methods=('POST',))
def delete_teacher(teacher_id):
    teacher = get_teacher(teacher_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM teachers WHERE teacher_id = ?', (teacher_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(teacher['name']))
    return redirect(url_for('teachers'))


# @app.route('/class/<string:dance_class_name>')
# def dance_class(dance_class_name):
#     dance_class = get_dance_class(dance_class_name)
#     return render_template('class.html', dance_class=dance_class)

@app.route('/class/<string:dance_class_id>')
def dance_class(dance_class_id):
    dance_class = get_dance_class(dance_class_id)
    return render_template('class.html', dance_class=dance_class)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
