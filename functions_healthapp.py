import sqlite3
import os
from datetime import datetime
from random import randint

image_paths = ["Images/checkmark.png", "Images/alert_yellow.png", "Images/alert_red.png"]

# Database path (use workspace-relative path)
DB_PATH = os.path.join(os.path.dirname(__file__), "healthapp.db")


def connect_db():
    """Return a sqlite3 connection using the project's DB path."""
    return sqlite3.connect(DB_PATH)


def get_user_trackable_id(userID, trackableID):
    """Return the user_trackablesID for a given user and trackable, or None."""
    try:
        with connect_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT user_trackablesID FROM user_trackables WHERE userID = ? AND trackableID = ?",
                (userID, trackableID),
            )
            row = cur.fetchone()
            return row[0] if row else None
    except sqlite3.Error as e:
        print(f"DB error in get_user_trackable_id: {e}")
        return None


def add_user_entry(user_trackable_id, value, date=None):
    """Insert an entry into user_trackables_entries. Returns True on success."""
    if date is None:
        date = datetime.now().date().isoformat()
    try:
        with connect_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO user_trackables_entries (user_trackablesID, entry_date, value) VALUES (?, ?, ?)",
                (user_trackable_id, date, value),
            )
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"DB error in add_user_entry: {e}")
        return False

# --------- User creatiom ---------
def insert_user(user_fn, user_ln, user_gender, user_age, user_email):
    date_now = str(datetime.now())
    # Execute the SQL command to insert the user data
    try:
        with connect_db() as sql_conn:
            sql_cursor = sql_conn.cursor()
            sql_cursor.execute(
                "INSERT INTO users (first_name, last_name, gender, age, created_at, last_login, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_fn, user_ln, user_gender, user_age, date_now[0:10], date_now[0:10], user_email)
            )
            sql_conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")

# --------- Database entries for trackables selected ---------
def track_mood(userID):
    try:
        date_now = str(datetime.now())[:10]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
                (userID, 2, date_now)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Error in track_mood:", e)

def track_anxiety(userID):
    try:
        date_now = str(datetime.now())[:10]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
                (userID, 1, date_now)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Error in track_anxiety:", e)

def track_sleep(userID):
    try:
        date_now = str(datetime.now())[:10]
        with connect_db() as conn:
            cursor = conn.cursor()
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
    except sqlite3.Error as e:
        print("Error in track_sleep:", e)

def track_self_harm(userID):
    try:
        date_now = str(datetime.now())[:10]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
                (userID, 5, date_now)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Error in track_self_harm:", e)

def track_depression(userID):
    try:
        date_now = str(datetime.now())[:10]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
                (userID, 9, date_now)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Error in track_depression:", e)

def track_alcohol_abuse(userID):
    try:
        date_now = str(datetime.now())[:10]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
                (userID, 6, date_now)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Error in track_alcohol_abuse:", e)

def track_drug_abuse(userID):
    try:
        date_now = str(datetime.now())[:10]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
                (userID, 7, date_now)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Error in track_drug_abuse:", e)

def track_eating_habits(userID):
    try:
        date_now = str(datetime.now())[:10]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_trackables (userID, trackableID, creationDate) VALUES (?, ?, ?)",
                (userID, 8, date_now)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Error in track_eating_habits:", e)

# Selects a random message from a text file
def give_message():
    with open("messages.txt", "r") as file:
        message_list = file.readlines()
        for i in range(0, len(message_list)):
            message_list[i] = message_list[i].replace("\n", "")

    return message_list[randint(0, len(message_list) - 1)]

# Gets the user trackables and the values of these trackables
def get_user_trackables(userID):
    user_trackables = []
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_trackablesID, trackableID from user_trackables WHERE userID = ? ORDER BY trackableID ASC", (userID, ))
            user_trackables = cursor.fetchall()
    except sqlite3.Error as e:
        print("Error in selecting user trackables:", e)
    return user_trackables

# Gets the trackable name from the trackable ID and returns it in a tuple in a list
def get_trackable_name(trackableID):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name from trackables WHERE trackableID = ?", (trackableID, ))
            row = cursor.fetchone()
            return row[0] if row else None
    except sqlite3.Error as e:
        print("Error in selecting trackable name:", e)
        return None

# Get the trackable max y
def get_trackable_maxy(trackableID):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT max_value from trackables WHERE trackableID = ?", (trackableID, ))
            row = cursor.fetchone()
            return row[0] if row else None
    except sqlite3.Error as e:
        print("Error in selecting trackable maxy:", e)
        return None

def get_trackable_tick(trackableID):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tick_count from trackables WHERE trackableID = ?", (trackableID, ))
            row = cursor.fetchone()
            return row[0] if row else None
    except sqlite3.Error as e:
        print("Error in selecting trackable tick:", e)
        return None

def get_values(user_trackableID):
    values = []
    try:
        with connect_db() as conn:
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


def add_bool_user_entry(user_trackable_id, bool_value):
    """Insert a boolean flag for a user_trackables entry."""
    try:
        with connect_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO bool_user_trackables (user_trackablesID, bool_value) VALUES (?, ?)",
                (user_trackable_id, bool_value),
            )
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"DB error in add_bool_user_entry: {e}")
        return False


def get_user_id_by_email(email):
    """Return userID for given email, case-insensitive, or None if not found."""
    try:
        with connect_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT userID FROM users WHERE LOWER(email) = LOWER(?)", (email,))
            row = cur.fetchone()
            return row[0] if row else None
    except sqlite3.Error as e:
        print(f"DB error in get_user_id_by_email: {e}")
        return None

# Updates user login date
def update_login(userID):
    try:
        date_now = str(datetime.now())[:10]
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE userID = ?",
                (date_now, userID)
            )
            conn.commit()
    except sqlite3.Error as e:
        print("Error updating login:", e)

# --------- Functions for changing user data ---------
def update_fname(userID, new_fname):
    try:
        with connect_db() as conn:
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
        with connect_db() as conn:
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
        with connect_db() as conn:
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
        with connect_db() as conn:
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
        with connect_db() as conn:
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
        with connect_db() as conn:
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
        with connect_db() as conn:
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