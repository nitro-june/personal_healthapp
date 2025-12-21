import sqlite3
from datetime import datetime
from random import randint

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

def update_last_login(user_email):
    sql_conn =  sqlite3.connect("healthapp.db")
    sql_cursor = sql_conn.cursor()
    date_now = str(datetime.now())
    sql_cursor.execute(
        "UPDATE users SET last_login = (?) WHERE email = (?)",
        (date_now[0:10], user_email)
    )
    sql_conn.commit()
    sql_conn.close()

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

def give_message():
    with open("messages.txt", "r") as file:
        message_list = file.readlines()
        for i in range(0, len(message_list)):
            message_list[i] = message_list[i].replace("\n", "")

    return message_list[randint(0, len(message_list) - 1)]

