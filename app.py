from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT)')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect('tasks.db') as conn:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_name = request.form['task']
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('INSERT INTO tasks (name) VALUES (?)', (task_name,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
