import sqlite3
from datetime import datetime
from random import randint

# --------- User creatiom ---------
def insert_user(user_fn, user_ln, user_gender, user_age, user_email):
    sql_conn = sqlite3.connect("healthapp.db")
    sql_cursor = sql_conn.cursor()
    date_now = str(datetime.now())
    # Execute the SQL command to insert the user data
    sql_cursor.execute(
        "INSERT INTO users (first_name, last_name, gender, age, created_at, last_login, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_fn, user_ln, user_gender, user_age, date_now[0:10], date_now[0:10], user_email)
    )
    sql_conn.commit()
    sql_conn.close()

# --------- Database entries for trackables selected ---------
def track_mood(userID):
    conn = None
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()
        date_now = str(datetime.now())[:10]
        cursor.execute(
            "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
            (userID, 2, date_now)
        )
        conn.commit()
    except Exception as e:
        print("Error in track_mood:", e)
    finally:
        if conn:
            conn.close()

def track_anxiety(userID):
    conn = None
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()
        date_now = str(datetime.now())[:10]
        cursor.execute(
            "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
            (userID, 1, date_now)
        )
        conn.commit()
    except Exception as e:
        print("Error in track_anxiety:", e)
    finally:
        if conn:
            conn.close()

def track_sleep(userID):
    conn = None
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()
        date_now = str(datetime.now())[:10]
        # Insert two trackables for sleep
        cursor.execute(
            "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
            (userID, 3, date_now)
        )
        cursor.execute(
            "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
            (userID, 4, date_now)
        )
        conn.commit()
    except Exception as e:
        print("Error in track_sleep:", e)
    finally:
        if conn:
            conn.close()

def track_self_harm(userID):
    conn = None
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()
        date_now = str(datetime.now())[:10]
        cursor.execute(
            "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
            (userID, 5, date_now)
        )
        conn.commit()
    except Exception as e:
        print("Error in track_self_harm:", e)
    finally:
        if conn:
            conn.close()

def track_depression(userID):
    conn = None
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()
        date_now = str(datetime.now())[:10]
        cursor.execute(
            "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
            (userID, 9, date_now)
        )
        conn.commit()
    except Exception as e:
        print("Error in track_depression:", e)
    finally:
        if conn:
            conn.close()

def track_alcohol_abuse(userID):
    conn = None
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()
        date_now = str(datetime.now())[:10]
        cursor.execute(
            "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
            (userID, 6, date_now)
        )
        conn.commit()
    except Exception as e:
        print("Error in track_alcohol_abuse:", e)
    finally:
        if conn:
            conn.close()

def track_drug_abuse(userID):
    conn = None
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()
        date_now = str(datetime.now())[:10]
        cursor.execute(
            "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
            (userID, 7, date_now)
        )
        conn.commit()
    except Exception as e:
        print("Error in track_drug_abuse:", e)
    finally:
        if conn:
            conn.close()

def track_eating_habits(userID):
    conn = None
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()
        date_now = str(datetime.now())[:10]
        cursor.execute(
            "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
            (userID, 8, date_now)
        )
        conn.commit()
    except Exception as e:
        print("Error in track_eating_habits:", e)
    finally:
        if conn:
            conn.close()

# Selects a random message from a text file
def give_message():
    with open("messages.txt", "r") as file:
        message_list = file.readlines()
        for i in range(0, len(message_list)):
            message_list[i] = message_list[i].replace("\n", "")

    return message_list[randint(0, len(message_list) - 1)]

# Gets the user trackables and the values of these trackables
def get_user_trackables(userID):
    conn = None
    user_trackables = []
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()

        cursor.execute("SELECT user_trackablesID, trackableID from user_trackables WHERE userID = ? ORDER BY trackableID ASC", (userID, ))
        user_trackables = cursor.fetchall()

    except Exception as e:
        print("Error in selecting user trackables:", e)

    finally:
        if conn:
            conn.close()
    return user_trackables

def get_values(user_trackableID):
    values = []
    try:
        with sqlite3.connect("healthapp.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT entry_date, value "
                "FROM user_trackables_entries "
                "WHERE user_trackablesID = ? "
                "ORDER BY entry_date ASC",
                (user_trackableID,)
            )
            values = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error for user_trackableID {user_trackableID}: {e}")
    except Exception as e:
        print(f"Unexpected error for user_trackableID {user_trackableID}: {e}")
    return values

# Updates user login date
def update_login(userID):
    conn = sqlite3.connect("healthapp.db")
    cursor = conn.cursor()

    date_now = str(datetime.now())[:10]
    cursor.execute(
        "UPDATE users SET last_login = ? WHERE userID = ?",
        (date_now, userID)
    )

    conn.commit()
    conn.close()

# Simple SQLite command to get user row
def get_user_info(userID):
    try:
        with sqlite3.connect("healthapp.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT first_name, last_name, gender, age, created_at, last_login, email 
                FROM users 
                WHERE userID = ?
            """, (userID,))
            user_info = cursor.fetchone()
            return user_info

    except sqlite3.Error as e:
        print("Error selecting user information:", e)
        return None