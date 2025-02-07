from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to get data from the database safely
def query_db(query, args=()):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        cursor.execute(query, args)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        print("Database error:", e)
        return []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message", "").lower()

    response = "I don't understand that question."

    if "employees in the" in user_message and "department" in user_message:
        department = user_message.split("in the")[1].split("department")[0].strip().capitalize()
        employees = query_db("SELECT Name FROM Employees WHERE Department = ?", (department,))
        response = ", ".join([emp[0] for emp in employees]) if employees else f"No employees found in the {department} department."

    elif "who is the manager of the" in user_message:
        department = user_message.split("of the")[1].split("department")[0].strip().capitalize()
        manager = query_db("SELECT Manager FROM Departments WHERE Name = ?", (department,))
        response = manager[0][0] if manager else f"No manager found for {department} department."

    elif "list all employees hired after" in user_message:
        date = user_message.split("after")[1].strip()
        employees = query_db("SELECT Name FROM Employees WHERE Hire_Date > ?", (date,))
        response = ", ".join([emp[0] for emp in employees]) if employees else "No employees hired after this date."

    elif "total salary expense for the" in user_message:
        department = user_message.split("for the")[1].split("department")[0].strip().capitalize()
        salary = query_db("SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,))
        response = f"Total salary expense for {department} department is ${salary[0][0]:,}" if salary and salary[0][0] else f"No data for {department} department."

    return jsonify({"response": response})

if __name__ == "__main__":
    # ✅ Corrected for Streamlit Cloud Deployment
    app.run(host="0.0.0.0", port=8080)
