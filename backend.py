
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from flask import Flask, jsonify, request
from flask_cors import CORS
import cx_Oracle
from datetime import date

app = Flask(__name__)
CORS(app)

host = 'myoracle12c.senecacollege.ca'
port = '1521'
service_name = 'oracle12c'
user = 'dbs501_232v1a05'
password = '25397213'

dsn = cx_Oracle.makedsn(host, port, service_name=service_name)

# Create a function to establish a new connection
def get_connection():
    return cx_Oracle.connect(user=user, password=password, dsn=dsn)

@app.route('/api/getjobs', methods=['GET', 'POST'])
def get_jobs():
    with get_connection() as conn:
        cursor = conn.cursor()
        sql_statement = 'SELECT * FROM HR_jobs'
        cursor.execute(sql_statement)
        results = cursor.fetchall()
        return jsonify(results)

@app.route('/api/getdepartments', methods=['GET', 'POST'])
def get_departments():
    with get_connection() as conn:
        cursor = conn.cursor()
        sql_statement = 'SELECT * FROM HR_departments'
        cursor.execute(sql_statement)
        results = cursor.fetchall()
        return jsonify(results)

@app.route('/api/getmanagers', methods=['GET', 'POST'])
def get_managers():
    with get_connection() as conn:
        cursor = conn.cursor()
        sql_statement = '''SELECT distinct e1.manager_id, e2.first_name , e2.last_name 
                          FROM hr_employees e1
                          JOIN hr_employees e2 ON e1.manager_id = e2.employee_id'''
        cursor.execute(sql_statement)
        results = cursor.fetchall()
        return jsonify(results)

@app.route('/api/getemployees', methods=['GET', 'POST'])
def get_employees():
    with get_connection() as conn:
        cursor = conn.cursor()
        sql_statement = '''SELECT * from HR_employees'''
        cursor.execute(sql_statement)
        results = cursor.fetchall()
        return jsonify(results)



@app.route('/api/addemployee', methods=['POST'])
def create_employee():
    try:
        today_date = date.today()
        
        # Retrieve employee data from the request body
        employee_data = request.json
        print(employee_data)
        print(type(employee_data['hire_date']))
        employee_id = int(employee_data['employee_id'])
        salary= int(employee_data['salary'])
        manager_id = int(employee_data['manager_id'])
        department_id = int(employee_data['department_id'])

         #Execute the stored procedure to create the employee
        with get_connection() as conn:
             cursor = conn.cursor()
             cursor.callproc('SP_NEW_HIRE', [
                 employee_id,
                 employee_data['first_name'],
                 employee_data['last_name'],
                 employee_data['email'],
                 employee_data['phone'],
                 today_date,
                 employee_data['job_id'],
                 salary,
                 manager_id,
                 department_id
             ])
            #  cursor.callproc('SP_NEW_HIRE',[
            #      345,
            #      'Suzie',
            #      'Wang',
            #      'helloworld',
            #      '4565456555',
            #      today_date,
            #      'SA_REP',
            #      23000,
            #      100,
            #      50
            #  ])
             conn.commit()

        return jsonify({'message': 'Employee created successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/updateemployee', methods=['POST'])
def update_employee():
    try:
        employee_data = request.json
        print(employee_data)
       
        employee_id = int(employee_data['employee_id'])
        salary= int(employee_data['salary'])
         #Execute the stored procedure to create the employee
        with get_connection() as conn:
             cursor = conn.cursor()
             cursor.callproc('SP_update_employee', [
                 employee_id,
                 employee_data['email'],
                 employee_data['phone'],
                 salary,
             ])
             conn.commit()

        return jsonify({'message': 'Employee update successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run()
