import sqlite3

def clear_users_table():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("DELETE FROM users")
        conn.commit()
        print("All rows deleted successfully.")
    except sqlite3.Error as e:
        print(f"Failed to clear users table: {e}")
    finally:
        if conn:
            conn.close()

clear_users_table()
