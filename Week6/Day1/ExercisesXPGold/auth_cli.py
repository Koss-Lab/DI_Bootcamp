# auth_cli.py

import psycopg2
import bcrypt

DB_NAME = "postgres"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )

def signup(username, password):
    conn = get_connection()
    cur = conn.cursor()

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, hashed.decode('utf-8')))
        conn.commit()
        print("Signup successful ✅")
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

def login(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        print("You are now logged in ✅")
        return True
    else:
        print("Invalid credentials ❌")
        return False


# CLI loop
logged_in = None

while True:
    action = input("Type 'login', 'signup' or 'exit': ").lower()

    if action == "exit":
        print("Bye 👋")
        break

    elif action == "signup":
        username = input("Choose username: ")
        password = input("Choose password: ")
        signup(username, password)

    elif action == "login":
        username = input("Username: ")
        password = input("Password: ")
        if login(username, password):
            logged_in = username
