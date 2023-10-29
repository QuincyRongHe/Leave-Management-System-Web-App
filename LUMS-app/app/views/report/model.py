import connect
import mysql.connector

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

def get_leave_expetion_data(manager_id):
    dbconn = getCursor()
    query =f"""SELECT e.emp_id, e.first_name, e.last_name, e.position_title, d.dept_name, lb.al_balance FROM employee AS e LEFT JOIN department as d ON e.dept_code=d.dept_code 
                    LEFT JOIN leave_balance as lb ON e.emp_id=lb.emp_id WHERE lb.al_balance >= 225  AND e.approval_manager = {manager_id} ORDER BY lb.al_balance DESC;"""
    
    print(query)
    dbconn.execute(query)
    
    return dbconn.fetchall()


def get_al_liability_data(manager_id):
    dbconn = getCursor()
    query = f"""SELECT e.emp_id, e.first_name, e.last_name, e.position_title, d.dept_name, lb.al_balance FROM employee AS e LEFT JOIN department as d ON e.dept_code=d.dept_code 
                    LEFT JOIN leave_balance as lb ON e.emp_id=lb.emp_id WHERE e.approval_manager = {manager_id} ORDER BY e.first_name ASC, e.last_name ASC;"""
    print(query)
    dbconn.execute(query)
    return dbconn.fetchall()


