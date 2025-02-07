from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to get data from the database
def query_db(query, args=()):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    conn.close()
    return result

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message", "").lower()

    response = "I don't understand that question."

    # Get employees from a specific department
    if "employees in the" in user_message or "employees working in the" in user_message or "details of employees from the" in user_message:
        parts = user_message.split("the")
        if len(parts) > 1:
            department = parts[1].replace("department", "").strip().capitalize()
            employees = query_db("SELECT Name FROM Employees WHERE Department = ?", (department,))
            response = ", ".join([emp[0] for emp in employees]) if employees else f"No employees found in the {department} department."

    # Get manager of a specific department
    elif "who is the manager of the" in user_message:
        parts = user_message.split("of the")
        if len(parts) > 1:
            department = parts[1].replace("department", "").strip().capitalize()
            manager = query_db("SELECT Manager FROM Departments WHERE Name = ?", (department,))
            response = manager[0][0] if manager else f"No manager found for {department} department."

    # List employees hired after a specific date
    elif "list all employees hired after" in user_message:
        parts = user_message.split("after")
        if len(parts) > 1:
            date = parts[1].strip()
            employees = query_db("SELECT Name FROM Employees WHERE Hire_Date > ?", (date,))
            response = ", ".join([emp[0] for emp in employees]) if employees else "No employees hired after this date."

    # List employees hired before a specific date
    elif "list all employees hired before" in user_message:
        parts = user_message.split("before")
        if len(parts) > 1:
            date = parts[1].strip()
            employees = query_db("SELECT Name FROM Employees WHERE Hire_Date < ?", (date,))
            response = ", ".join([emp[0] for emp in employees]) if employees else "No employees hired before this date."

    # Get total salary expense for a department
    elif "total salary expense for" in user_message:
        parts = user_message.split("total salary expense for")
        if len(parts) > 1:
            department = parts[1].replace("the", "").replace("department", "").strip().capitalize()
            salary = query_db("SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,))
            response = f"Total salary expense for {department} department is ${salary[0][0]:,}" if salary and salary[0][0] else f"No data for {department} department."

    # List all departments and their managers
    elif "list all departments and their managers" in user_message:
        departments = query_db("SELECT Name, Manager FROM Departments")
        if departments:
            response = "\n".join([f"{dept[0]} - {dept[1]}" for dept in departments])
        else:
            response = "No department data available. Please check the database."

    # Get the highest salary in the company
    elif "highest salary" in user_message:
        highest_salary = query_db("SELECT Name, Salary, Department FROM Employees ORDER BY Salary DESC LIMIT 1")
        if highest_salary:
            response = f"The highest salary is ${highest_salary[0][1]:,} ({highest_salary[0][0]} - {highest_salary[0][2]})"
        else:
            response = "No salary data available."

    # Get the average salary of employees
    elif "average salary" in user_message:
        avg_salary = query_db("SELECT AVG(Salary) FROM Employees")
        if avg_salary and avg_salary[0][0] is not None:
            response = f"The average salary is ${avg_salary[0][0]:,.2f}"
        else:
            response = "No salary data available."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
