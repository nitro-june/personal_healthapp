import sqlite3
from datetime import datetime
from random import randint

image_paths = ["Images/checkmark.png", "Images/alert_yellow.png", "Images/alert_red.png"]

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

# Gets the trackable name from the trackable ID and returns it in a tuple in a list
def get_trackable_name(trackableID):
    conn = None
    trackable_name = []
    try:
        conn = sqlite3.connect("healthapp.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name from trackables WHERE trackableID = ?", (trackableID, ))
        trackable_name = cursor.fetchall()

    except Exception as e:
        print("Error in selecting user trackables:", e)

    finally:
        if conn:
            conn.close()
    return trackable_name

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

# --------- Functions for changing user data ---------
def update_fname(userID, new_fname):
    try:
        with sqlite3.connect("healthapp.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET first_name = ? WHERE userID = ?",
                (new_fname, userID)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
        raise

def update_lname(userID, new_lname):
    try:
        with sqlite3.connect("healthapp.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET last_name = ? WHERE userID = ?",
                (new_lname, userID)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
        raise

def update_gender(userID, new_gender):
    try:
        with sqlite3.connect("healthapp.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET gender = ? WHERE userID = ?",
                (new_gender, userID)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
        raise

def update_age(userID, new_age):
    try:
        with sqlite3.connect("healthapp.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET age = ? WHERE userID = ?",
                (new_age, userID)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
        raise

def update_email(userID, new_email):
    try:
        with sqlite3.connect("healthapp.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET email = ? WHERE userID = ?",
                (new_email, userID)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
        raise

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

def delete_user(userID):
    trackables = get_user_trackables(userID)

    try:
        with sqlite3.connect("healthapp.db") as conn:
            cursor = conn.cursor()

            for item in trackables:
                trackable_id = item[0]

                cursor.execute(
                    "DELETE FROM user_trackables_entries WHERE user_trackablesID = ?",
                    (trackable_id,)
                )

                cursor.execute(
                    "DELETE FROM bool_user_trackables WHERE user_trackablesID = ?",
                    (trackable_id,)
                )

            cursor.execute(
                "DELETE FROM user_trackables WHERE userID = ?",
                (userID,)
            )

            cursor.execute(
                "DELETE FROM users WHERE userID = ?",
                (userID,)
            )

    except sqlite3.Error as e:
        print("Database error:", e)
        raise

# Functions to determine what image to show
def select_image_path(values):
    if len(values) > 4:
        median = 0
        for item in values:
            median += item
        median /= len(values)
        if median < 0.33:
            return image_paths[0]
        if median < 0.66:
            return image_paths[1]
        else:
            return image_paths[2]
    else:
        if not values:
            return ""
        elif values[-1] == 0:
            return image_paths[0]
        else:
            return image_paths[2]