import sqlite3

# Connect to your existing chatbot database
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Insert Departments Data
departments_data = [
    (1, 'Sales', 'Alice'),
    (2, 'Engineering', 'Bob'),
    (3, 'Marketing', 'Charlie')
]

cursor.executemany("INSERT OR IGNORE INTO Departments (ID, Name, Manager) VALUES (?, ?, ?)", departments_data)

# Insert Employees Data
employees_data = [
    (1, 'Alice', 'Sales', 50000, '2021-01-15'),
    (2, 'Bob', 'Engineering', 70000, '2020-06-10'),
    (3, 'Charlie', 'Marketing', 60000, '2022-03-20'),
    (4, 'David', 'Sales', 55000, '2023-07-15'),
    (5, 'Emma', 'Engineering', 80000, '2022-11-20'),
    (6, 'Michael', 'Marketing', 62000, '2023-05-25'),
    (7, 'Sophia', 'Sales', 51000, '2021-09-05'),
    (8, 'Liam', 'Engineering', 75000, '2019-12-30'),
    (9, 'Olivia', 'Marketing', 58000, '2020-08-19')
]

cursor.executemany("INSERT OR IGNORE INTO Employees (ID, Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?, ?)", employees_data)

# Commit and close the database connection
conn.commit()
conn.close()

print("✅ Data inserted successfully! Now test your chatbot.")
