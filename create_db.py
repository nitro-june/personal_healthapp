import sqlite3

connection = sqlite3.connect('healthapp.db')
con_cursor = connection.cursor()

con_cursor.execute("PRAGMA foreign_keys = ON;")

con_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    age INTEGER,
    created_at TEXT,
    last_login TEXT,
    email TEXT
);
""")

con_cursor.execute("""
CREATE TABLE IF NOT EXISTS trackables (
    trackableID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    min_value REAL,
    max_value REAL
);
""")

con_cursor.execute("""
CREATE TABLE IF NOT EXISTS user_trackables (
    user_trackablesID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER,
    trackableID INTEGER,
    creationDate INTEGER,
    FOREIGN KEY(trackableID) REFERENCES trackables(trackableID),
    FOREIGN KEY(userID) REFERENCES users(userID)
);
""")

con_cursor.execute("""
CREATE TABLE IF NOT EXISTS user_trackables_entries (
    entriesID INTEGER PRIMARY KEY AUTOINCREMENT,
    user_trackablesID INTEGER,
    entry_date TEXT,
    value REAL,
    FOREIGN KEY(user_trackablesID) REFERENCES user_trackables(user_trackablesID)
);
""")

con_cursor.execute("""
CREATE TABLE IF NOT EXISTS bool_user_trackables (
    bool_trackable_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    user_trackablesID INTEGER,
    bool_value INTEGER,
    input_date TEXT,
    FOREIGN KEY(user_trackablesID) REFERENCES user_trackables(user_trackablesID)
);
""")

con_cursor.executemany("""
INSERT INTO trackables (name, description, min_value, max_value)
VALUES (?, ?, ?, ?)
""", [
    ("Anxiety", "Anxiety is persistent worry and tension that disrupts daily life, causing restlessness, fear and unease.", 0.0, 21.0),
    ("Mood", "The overall mood mood of your day in a scale of 0 - 10.", 0.0, 10.0),
    ("Sleep Quality", "The overall sleep quality for a given night.", 0.0, 10.0),
    ("Sleep Length", "The overall sleep quantity for a given night.", 0.0, 10.0),
    ("Self Harm", "Self-harm, or self-injury, is when a person hurts his or her own body on purpose. The injuries may be minor, but sometimes they can be severe.", 0.0, 1.0),
    ("Alcohol Abuse", "Recurrent use of alcohol resulting in a failure to fulfill major role obligations at work, school, or home.", 0.0, 12.0),
    ("Drug Abuse", "Recurrent use of drugs resulting in a failure to fulfill major role obligations at work, school, or home.", 0.0, 1.0),
    ("Eating Habits", "Eating habits are the consistent, often unconscious patterns of how, what, when, and why we eat, influenced by culture, environment, psychology, and lifestyle, forming a crucial part of our daily behavior that impacts overall health by determining our nutrient intake and disease risk.", 0.0, 78.0),
    ("Depression", "Depression is a mental health condition marked by persistent sadness, loss of interest or pleasure, low energy, and difficulty functioning in daily life.", 0.0, 27.0)
])

connection.commit()
connection.close()