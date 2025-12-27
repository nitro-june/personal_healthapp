import sqlite3

sql_conn = sqlite3.connect("healthapp.db")
sql_cursor = sql_conn.cursor()

sql_cursor.execute("SELECT entry_date, value FROM user_trackables_entries WHERE user_trackablesID = 2 ORDER BY entry_date ASC")
results = sql_cursor.fetchall()

sql_conn.commit()
sql_conn.close()

dates_mood =[]
values_mood = []

for item in results:
    dates_mood += [item[0]]
    values_mood += [item[1]]

print(dates_mood)
print(values_mood)
