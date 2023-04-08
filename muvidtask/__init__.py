from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)
fake = Faker()
    


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, department, salary, hire_date):
        self.name = name
        self.department = department
        self.salary = salary
        self.hire_date = hire_date

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'salary': self.salary,
            'hire_date': self.hire_date.strftime('%Y-%m-%d %H:%M:%S')
        }




# Generate fake employee data
def generate_fake_data():
    for _ in range(1000):
        name = fake.name()
        department = fake.job()
        salary = fake.random_digit()
        hire_date = fake.date_between(start_date='-2y', end_date='today')
        employee = Employee(name=name, department=department, salary=salary, hire_date=hire_date)
        db.session.add(employee)
    db.session.commit()

with app.app_context():
    db.metadata.clear()
    db.create_all()
    generate_fake_data()

from muvidtask import routes