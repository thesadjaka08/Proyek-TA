import streamlit as st
import sqlite3
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib

# Function to create or connect to the database
def create_connection():
    try:
        conn = sqlite3.connect('users.db', check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        st.error(f"Failed to connect to database: {e}")
        return None

conn = create_connection()
c = conn.cursor()

# Function to create users table if not exists
def create_table():
    try:
        c.execute('''
                  CREATE TABLE IF NOT EXISTS users
                  (username TEXT, password TEXT, email TEXT, verified INTEGER)
                  ''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Failed to create table: {e}")

def add_verified_column():
    try:
        c.execute("ALTER TABLE users ADD COLUMN verified INTEGER DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    except sqlite3.Error as e:
        st.error(f"Failed to add verified column: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_verification_code(email):
    verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    st.session_state.verification_code = verification_code
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "jeremiaexcel12@gmail.com"
    smtp_password = "lgyjyhyxfphmgvyh"  # Use your app password here
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        message = MIMEMultipart()
        message['From'] = smtp_user
        message['To'] = email
        message['Subject'] = "Email Verification Code"
        
        body = f"Your verification code is {verification_code}"
        message.attach(MIMEText(body, 'plain'))
        
        server.send_message(message)
        server.quit()
        
        st.success(f"Verification code sent to {email}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Function to insert user data into the database
def insert_user(username, password, email, verified):
    try:
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users (username, password, email, verified) VALUES (?, ?, ?, ?)", 
                  (username, hashed_password, email, verified))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Failed to insert user: {e}")

# Function to authenticate user credentials
def authenticate(username, password):
    try:
        hashed_password = hash_password(password)
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                  (username, hashed_password))
        user = c.fetchone()
        return user
    except sqlite3.Error as e:
        st.error(f"Failed to authenticate user: {e}")
        return None

# Function to check if email already exists
def email_exists(email):
    try:
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        return c.fetchone() is not None
    except sqlite3.Error as e:
        st.error(f"Failed to check email: {e}")
        return False

# Function to update verification status
def update_verification_status(email):
    try:
        c.execute("UPDATE users SET verified = 1 WHERE email = ?", (email,))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Failed to update verification status: {e}")

def main():
    create_table()
    add_verified_column()

    if 'page' not in st.session_state:
        st.title("Login and Registration")
        st.session_state.page = 'login'

    if st.session_state.page == 'login':
        tabs = st.tabs(["Login", "Register"])
        with tabs[0]:
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user = authenticate(username, password)
                if user:
                    email, verified = user[2], user[3]
                    if verified:
                        st.success("Login successful")
                        st.session_state.page = 'homepage'
                        st.experimental_rerun()
                    else:
                        st.error("Please verify your email before logging in.")
                else:
                    st.error("Invalid username or password")

        with tabs[1]:
            st.subheader("Register")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            email = st.text_input("Email")
            if st.button("Register"):
                if email_exists(email):
                    st.error("This email is already registered")
                else:
                    send_verification_code(email)
                    st.session_state.new_username = new_username
                    st.session_state.new_password = new_password
                    st.session_state.email = email

        if "verification_code" in st.session_state:
            input_code = st.text_input("Enter verification code sent to your email")
            if st.button("Verify"):
                if input_code == st.session_state.verification_code:
                    insert_user(st.session_state.new_username, st.session_state.new_password, 
                                st.session_state.email, 1)
                    st.success("Registration successful and email verified. You can now login.")
                    del st.session_state.verification_code
                    del st.session_state.new_username
                    del st.session_state.new_password
                    del st.session_state.email
                else:
                    st.error("Incorrect verification code")

    elif st.session_state.page == 'homepage':
        # Execute the code from homepage.py
        with open("homepage.py") as f:
            code = compile(f.read(), "homepage.py", 'exec')
            exec(code, globals())

if __name__ == "__main__":
    main()
