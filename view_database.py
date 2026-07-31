import sqlite3

connection = sqlite3.connect("kanban.db")

cursor = connection.cursor()

# show tables
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

print("Tables:")
for table in tables:
    print(table[0])


# show tasks
print("\nTasks:")

cursor.execute(
    "SELECT * FROM tasks;"
)

rows = cursor.fetchall()

for row in rows:
    print(row)


connection.close()