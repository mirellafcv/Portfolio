# Importar
import sqlite3
from flask import Flask, render_template, request

DATABASE = 'feedback.db'

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()
    conn.close()


init_db()


# Conteúdo da página
@app.route('/')
def index():
    return render_template('index.html')


# Habilidades Dinâmicas e feedback
@app.route('/', methods=['POST'])
def process_form():
    button_python = request.form.get('button_python')
    feedback_email = request.form.get('email')
    feedback_text = request.form.get('text')

    if feedback_email and feedback_text:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO feedback (email, message) VALUES (?, ?)',
            (feedback_email, feedback_text),
        )
        conn.commit()
        conn.close()

    return render_template(
        'index.html',
        button_python=button_python,
        feedback_email=feedback_email,
        feedback_text=feedback_text,
    )


if __name__ == "__main__":
    app.run(debug=True)
