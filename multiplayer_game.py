import socket
import threading
import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                      id INTEGER PRIMARY KEY,
                      question TEXT,
                      option1 TEXT,
                      option2 TEXT,
                      option3 TEXT,
                      option4 TEXT,
                      answer TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                      username TEXT PRIMARY KEY,
                      score INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      username TEXT PRIMARY KEY,
                      password_hash TEXT)''')
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    username = None
    authenticated = False
    while True:
        data = conn.recv(1024).decode('utf-8')
        if data:
            command, *args = data.split('|')
            if command == 'REGISTER':
                username, password = args
                register_user(conn, username, password)
            elif command == 'LOGIN':
                username, password = args
                authenticated = login_user(conn, username, password)
            elif command == 'ADD' and authenticated:
                add_question(conn, *args)
            elif command == 'ANSWER' and authenticated:
                show_question_and_answer(conn, *args)
            elif command == 'LEADERBOARD' and authenticated:
                show_leaderboard(conn)
            elif command == 'DISCONNECT':
                break
            else:
                conn.send("Please login first.".encode('utf-8'))
    conn.close()
def register_user(conn, username, password):
    conn_db = sqlite3.connect('quiz.db')
    cursor = conn_db.cursor()
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        conn.send("Username already taken.".encode('utf-8'))
    else:
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn_db.commit()
        conn.send("Registration successful.".encode('utf-8'))
    conn_db.close()
def login_user(conn, username, password):
    conn_db = sqlite3.connect('quiz.db')
    cursor = conn_db.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    record = cursor.fetchone()
    if record and record[0] == hash_password(password):
        conn.send("Login successful.".encode('utf-8'))
        return True
    else:
        conn.send("Invalid username or password.".encode('utf-8'))
        return False
    conn_db.close()

def add_question(conn, question, opt1, opt2, opt3, opt4, answer):
    conn_db = sqlite3.connect('quiz.db')
    cursor = conn_db.cursor()
    cursor.execute('INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?)',
                   (question, opt1, opt2, opt3, opt4, answer))
    conn_db.commit()
    conn.send('Question added successfully.'.encode('utf-8'))
    conn_db.close()

def show_question_and_answer(conn, qid, user_answer=None):
    conn_db = sqlite3.connect('quiz.db')
    cursor = conn_db.cursor()
    cursor.execute('SELECT question, option1, option2, option3, option4, answer FROM questions WHERE id = ?', (qid,))
    question = cursor.fetchone()
    if question:
        qtext, opt1, opt2, opt3, opt4, correct_answer = question
        if user_answer:
            if user_answer.strip().lower() == correct_answer.strip().lower():
                cursor.execute('INSERT OR IGNORE INTO leaderboard (username) VALUES (?)', (username,))
                cursor.execute('UPDATE leaderboard SET score = score + 1 WHERE username = ?', (username,))
                conn.send("Correct!".encode('utf-8'))
            else:
                conn.send("Incorrect.".encode('utf-8'))
        else:
            response = f"Q: {qtext}\n1: {opt1}\n2: {opt2}\n3: {opt3}\n4: {opt4}"
            conn.send(response.encode('utf-8'))
    else:
        conn.send('Question not found.'.encode('utf-8'))
    conn_db.commit()
    conn_db.close()


def show_leaderboard(conn):
    conn_db = sqlite3.connect('quiz.db')
    cursor = conn_db.cursor()
    cursor.execute('SELECT username, score FROM leaderboard ORDER BY score DESC')
    leaderboard = cursor.fetchall()
    response = '\n'.join([f"{username}: {score}" for username, score in leaderboard])
    conn.send(response.encode('utf-8'))
    conn_db.close()


def start_server():
    init_db()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  
    server.listen()
    print("[SERVER STARTED] Waiting for connections...")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

start_server()