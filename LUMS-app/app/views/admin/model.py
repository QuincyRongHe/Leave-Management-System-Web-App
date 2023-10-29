import connect
import mysql.connector
import hashlib, os
from pathlib import Path


def getCursor(isDict=False):
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor(dictionary=isDict)
    return dbconn


def initialize():
    conn = getCursor()
    host = connect.dbhost

    print("host: ", host)
    
    
    if host == "localhost":
        path = Path(__file__).parent.parent.parent.parent.parent / "./Database/leave_system.sql"
    else:
        path = Path(__file__).parent.parent.parent.parent.parent / "./Database/leave_system_pa.sql"
    print("Finished path: ", path)
    # print(path)

    print("Running SQL file.....")
    with path.open(mode='r') as sql_file:
        results = conn.execute(sql_file.read(), multi=True)
        print(results)
        
        if host == "localhost":
            for res in results:
                print("Running query: ", res)  # Will print out a short representation of the query
                print(f"Affected {res.rowcount} rows" )
    print('tables created successfully')

def get_all_user_id():
    conn = getCursor()
    query = "SELECT user_id FROM users"
    conn.execute(query)
    res = conn.fetchall()
    # print(res)
    return res

def get_pwd_by_id(user_id):
    conn = getCursor()
    query = f"SELECT pwd FROM users WHERE user_id = {user_id}"
    # print(query)
    conn.execute(query)
    res = conn.fetchone()[0]
    # print(res)
    return res

def update_pwd_and_salt(new_pwd, new_salt, user_id):
    conn = getCursor()
    query = f"UPDATE users SET pwd='{new_pwd}', salt='{new_salt}' WHERE user_id = {user_id}"
    conn.execute(query)

def get_all_holidays():
    conn = getCursor(isDict=True)
    query = "SELECT holiday_id, holiday_name, holiday_year, holiday_month, holiday_day, concat(e.first_name,' ', e.last_name) AS edit_by, edit_date, is_active FROM holiday AS h Left JOIN employee AS e ON h.edit_by=e.emp_id"
    conn.execute(query)
    res = conn.fetchall()
    # print(res)
    return res

def update_holidays(data, updated_by, updated_time):
    conn = getCursor()

    query = "UPDATE holiday SET"

    for col in ['holiday_name', 'holiday_year', 'holiday_month', 'holiday_day', 'edit_by', 'edit_date', 'is_active']:
        if col in data.keys():
            data[col] = 1 if data[col] else 0
            query += f" {col} = '{data[col]}',"
    query += f" edit_by = {updated_by}, edit_date = '{updated_time}'"
    query += f" WHERE holiday_id = {data['id']};"
    

    print("to update:", query)
    conn.execute(query)
    return "Update successful!"



def add_new_holidays(name, year, month, day, updated_by, updated_time):
    conn = getCursor()

    query = f"""INSERT INTO holiday (holiday_name, holiday_year, holiday_month, holiday_day, edit_by, edit_date, is_active) VALUES ('{name}', {year}, {month}, {day}, {updated_by}, '{updated_time}', 1);"""

    print("inserted a new row:", query)
    conn.execute(query)
    return "Added successful!"

def get_all_leave_types():
    conn = getCursor(isDict=True)
    query = "SELECT leave_code, leave_name, leave_per_year, is_active FROM leave_type"
    conn.execute(query)
    res = conn.fetchall()
    print(res)
    return res


def update_leave_types(data):
    conn = getCursor()

    query = "UPDATE leave_type SET"

    for col in ['leave_name', 'is_active']:
        if col in data.keys():
            data[col] = 1 if data[col] else 0
            query += f" {col} = '{data[col]}',"
    query = query[:-1]
    query += f" WHERE leave_code = '{data['id']}';"
    

    print("to update:", query)
    conn.execute(query)
    return "Update successful!"

    
def add_leave_types(data):
    conn = getCursor()

    query = f"""INSERT INTO leave_type (leave_code, leave_name, is_active) VALUES 
             ('{data['leave_code']}', '{data['leave_name']}', 1);"""

    
    print(data)
    #query = query[:-1]
    #query += f" WHERE leave_code = '{data['id']}';"
    

    conn.execute(query)
    return "Update successful!"


def get_role_for_all_employees(admin_id):
    conn = getCursor()
    
    query = f"""SELECT e.emp_id, e.first_name, e.last_name, r.role_name
                FROM employee e
                LEFT JOIN users u ON e.emp_id = u.user_id
                LEFT JOIN roles r ON u.role_id = r.role_id
                WHERE e.emp_id <> {admin_id}
                ORDER BY r.role_name;"""
    
    conn.execute(query)
    all_employee_roles = conn.fetchall()

    return all_employee_roles

def search_roles(admin_id, role_id=None, name=None):
    conn = getCursor()

    
    
    query = f"""SELECT e.emp_id, e.first_name, e.last_name, r.role_name
                FROM employee e
                LEFT JOIN users u ON e.emp_id = u.user_id
                LEFT JOIN roles r ON u.role_id = r.role_id
                WHERE e.emp_id <> {admin_id}
            """
    
    if role_id:
        query += f" AND r.role_id = {role_id}"
    if name:
        query += f" AND CONCAT(e.first_name, ' ', e.last_name) LIKE '%{name}%'"
    
    query += " ORDER BY r.role_name;"
    
    conn.execute(query)
    result = conn.fetchall()

    return result

def update_roles_for_employees(employee_id, new_role):
    cursor = getCursor()

    # Get the role ID based on the role name
    query = "SELECT role_id FROM roles WHERE role_name = %s;"
    cursor.execute(query, (new_role,))
    role_id = cursor.fetchone()[0]

    # Update the role for the employee
    query = "UPDATE users SET role_id = %s WHERE user_id = %s;"
    cursor.execute(query, (role_id, employee_id))
    connection.commit()

    cursor.close()





