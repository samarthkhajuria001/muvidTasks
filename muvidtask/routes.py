from muvidtask import app, Employee
from flask import  jsonify, render_template



# API Endpoints

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/employees', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    result = []
    for employee in employees:
        employee_data = employee.serialize()
        result.append(employee_data)
    return jsonify(result)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    if employee:
        employee_data = employee.serialize()
        return jsonify(employee_data)
    else:
        return jsonify({'message': 'Employee not found'}), 404

@app.route('/employees', methods=['POST'])
def create_employee():
    name = request.form['name']
    department = request.form['department']
    salary = float(request.form['salary'])
    hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d %H:%M:%S')
    employee = Employee(name=name, department=department, salary=salary, hire_date=hire_date)
    db.session.add(employee)
    db.session.commit()
    return jsonify({'id': employee.id})

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)
    if employee:
        employee.name = request.form['name']
        employee.department = request.form['department']
        employee.salary = float(request.form['salary'])
        employee.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d %H:%M:%S')
        db.session.commit()
        return jsonify({'message': 'Employee updated successfully'})
    else:
        return jsonify({'message': 'Employee not found'}), 404

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return f"Employee with ID {id} has been deleted.", 200
    else:
        return f"Employee with ID {id} not found.", 404

@app.route('/departments', methods=['GET'])
def get_departments():
    departments = Employee.query.with_entities(Employee.department).distinct().all()
    department_list = [department[0] for department in departments]
    return jsonify(departments=department_list)

@app.route('/departments/<string:name>', methods=['GET'])
def get_employees_by_department(name):
    employees = Employee.query.filter_by(department=name).all()
    employee_list = []
    if employees:
        for employee in employees:
            employee_list.append({
                'id': employee.id,
                'name': employee.name,
                'department': employee.department,
                'salary': employee.salary,
 'hire_date': employee.hire_date.strftime('%Y-%m-%d %H:%M:%S')
            })
        return jsonify(employees=employee_list)
    else:
        return f"No employees found in department {name}.", 404


@app.route('/average_salary/<string:department>', methods=['GET'])
def get_average_salary(department):
    employees = Employee.query.filter_by(department=department).all()
    if employees:
        total_salary = sum([employee.salary for employee in employees])
        average_salary = total_salary / len(employees)
        return jsonify(department=department, average_salary=average_salary)
    else:
        return f"No employees found in department {department}.", 404

# GET /top_earners
@app.route('/top_earners', methods=['GET'])
def get_top_earners():
    employees = Employee.query.order_by(Employee.salary.desc()).limit(10).all()
    employee_list = []
    if employees:
        for employee in employees:
            employee_list.append({
                'id': employee.id,
                'name': employee.name,
                'department': employee.department,
                'salary': employee.salary,
                'hire_date': employee.hire_date.strftime('%Y-%m-%d %H:%M:%S')
            })
        return jsonify(employees=employee_list)
    else:
        return "No employees found.", 404

# GET /most_recent_hires
@app.route('/most_recent_hires', methods=['GET'])
def get_most_recent_hires():
    employees = Employee.query.order_by(Employee.hire_date.desc()).limit(10).all()
    employee_list = []
    if employees:
        for employee in employees:
            employee_list.append({
                'id': employee.id,
                'name': employee.name,
                'department': employee.department,
                'salary': employee.salary,
                'hire_date': employee.hire_date.strftime('%Y-%m-%d %H:%M:%S')
            })
        return jsonify(employees=employee_list)
    else:
        return "No employees found.", 404