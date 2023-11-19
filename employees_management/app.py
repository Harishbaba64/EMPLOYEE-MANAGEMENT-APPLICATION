from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = os.path.join("data", "employees.json")

def read_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return []

def write_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/show_employees')
def show_employees():
    employees = read_data()
    return render_template('show_employees.html', employees=employees)

@app.route('/filter_employees', methods=['GET', 'POST'])
def filter_employees():
    if request.method == 'POST':
        criteria = request.form.get('criteria')
        value = request.form.get('value')
        employees = read_data()
        filtered_employees = [employee for employee in employees if str(employee.get(criteria, '')) == value]
        return render_template('show_employees.html', employees=filtered_employees)

    return render_template('filter_employees.html')

@app.route('/search_employee', methods=['GET', 'POST'])
def search_employee():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        employees = read_data()
        filtered_employees = [employee for employee in employees if search_query.lower() in employee.get('full_name', '').lower()]
        return render_template('show_employees.html', employees=filtered_employees)

    return render_template('search_employee.html')

@app.route('/update_employee/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    employees = read_data()
    employee = next((employee for employee in employees if employee["id"] == id), None)

    if request.method == 'POST':
        updated_data = {
            "full_name": request.form.get("full_name"),
            "age": int(request.form.get("age")),
            "date_of_birth": request.form.get("date_of_birth"),
            "salary": int(request.form.get("salary")),
            "department": request.form.get("department")
        }

        employee.update(updated_data)
        write_data(employees)
        return redirect(url_for('show_employees'))

    return render_template('update_employee.html', employee=employee)

@app.route('/delete_employee/<int:id>')
def delete_employee(id):
    employees = read_data()
    employees = [employee for employee in employees if employee["id"] != id]
    write_data(employees)
    return redirect(url_for('show_employees'))

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee_page():
    if request.method == 'POST':
        employees = read_data()

        new_employee = {
            "id": len(employees) + 1,  
            "full_name": request.form.get("full_name"),
            "age": int(request.form.get("age")),
            "date_of_birth": request.form.get("date_of_birth"),
            "salary": int(request.form.get("salary")),
            "department": request.form.get("department")
        }

        employees.append(new_employee)
        write_data(employees)
        return redirect(url_for('show_employees'))

    return render_template('add_employee.html')

if __name__ == '__main__':
    app.run(debug=True)
