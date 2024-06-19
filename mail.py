import smtplib
import random
import string
import streamlit as st
import sqlite3

# Function to create or connect to the database
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Function to create users table if not exists
def create_table(conn):
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS users
              (username TEXT, password TEXT, email TEXT, verified INTEGER, verification_code TEXT)
              ''')
    conn.commit()

def send_verification_code(email):
    verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_app_password")  # Gunakan kata sandi aplikasi di sini
        message = f"Your verification code is {verification_code}"
        server.sendmail("your_email@gmail.com", email, message)
        server.quit()
        return verification_code
    except smtplib.SMTPAuthenticationError as e:
        st.error(f"Failed to send email: {e}")
        return None

def insert_user(conn, username, password, email, verification_code):
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, email, verified, verification_code) VALUES (?, ?, ?, 0, ?)", 
              (username, password, email, verification_code))
    conn.commit()

def verify_code(conn, email, input_code):
    c = conn.cursor()
    c.execute("SELECT verification_code FROM users WHERE email = ?", (email,))
    record = c.fetchone()
    if record and record[0] == input_code:
        c.execute("UPDATE users SET verified = 1 WHERE email = ?", (email,))
        conn.commit()
        return True
    return False

def main():
    conn = create_connection()  # Connect to the database
    create_table(conn)  # Create users table if not exists

    st.title("Register")  # Set title for the app

    # Registration form
    email = st.text_input("Email", key="register_email")
    username = st.text_input("User name", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

    if st.button("Register", key="register_button"):  # Button to register
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            verification_code = send_verification_code(email)
            if verification_code:
                insert_user(conn, username, password, email, verification_code)
                st.success("Registration successful. Please enter the verification code sent to your email.")
                input_code = st.text_input("Enter verification code", key="verification_code_input")
                if st.button("Verify Code", key="verify_code_button"):
                    if verify_code(conn, email, input_code):
                        st.success("Email verified successfully. You can now login.")
                    else:
                        st.error("Incorrect verification code")
            else:
                st.error("Failed to send verification code. Please check your email credentials.")

    conn.close()  # Close database connection

if __name__ == "__main__":
    main()  # Call the main function
