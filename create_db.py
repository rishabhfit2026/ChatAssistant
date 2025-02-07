import sqlite3

# Connect to SQLite Database (or create it)
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Create Employees Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Department TEXT,
    Salary INTEGER,
    Hire_Date TEXT
)
""")

# Create Departments Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Departments (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Manager TEXT
)
""")

# Insert Sample Data (Only If Table is Empty)
cursor.execute("SELECT COUNT(*) FROM Employees")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO Employees (ID, Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?, ?)", [
        (1, 'Alice', 'Sales', 50000, '2021-01-15'),
        (2, 'Bob', 'Engineering', 70000, '2020-06-10'),
        (3, 'Charlie', 'Marketing', 60000, '2022-03-20')
    ])

cursor.execute("SELECT COUNT(*) FROM Departments")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO Departments (ID, Name, Manager) VALUES (?, ?, ?)", [
        (1, 'Sales', 'Alice'),
        (2, 'Engineering', 'Bob'),
        (3, 'Marketing', 'Charlie')
    ])

# Commit changes and close connection
conn.commit()
conn.close()

print("Database setup complete!")
