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


def get_role_by_id(user_id):
      
      """
      Returns a role id
  
      """
  
      conn = getCursor()
      query = f"""
      SELECT
      role_id
      FROM
      users
      WHERE 
      user_id={user_id};"""
  
      conn.execute(query)
      res = conn.fetchone()
  
      return res[0]

def get_details_by_id(user_id):

    """
    Returns a tuple in the following fomat represents an employee.
    (user_name, role_name, title, first_name, last_name, gender, joined_date)

    """

    conn = getCursor()
    query = f"""
    SELECT
    emp_id, 
    user_name,
    role_name,
    title,
    first_name,
    last_name,
    gender,
    joined_date
    FROM
    users AS u
        LEFT JOIN
    roles AS r ON u.role_id = r.role_id
        LEFT JOIN
    employee AS e ON u.user_id = e.emp_id
    WHERE 
    user_id={user_id};"""

    conn.execute(query)
    res = conn.fetchone()

    return res

def get_position_and_date(user_id):

    """
    Returns a tuple in the following fomat represents an employee.
    (position_title, position_start_date)

    """

    conn = getCursor()
    query = f"""
    SELECT 
    position_title, position_start_date
    FROM
    employee   
    WHERE 
    emp_id={user_id};"""

    conn.execute(query)
    res = conn.fetchone()

    return res
    
def get_dept_name(user_id):

    """
    Returns a tuple in the following fomat represents an employee.
    (dept_code, dept_name)

    """

    conn = getCursor()
    query = f"""
    SELECT 
    e.dept_code, d.dept_name
    FROM
    employee AS e
        INNER JOIN
    department AS d ON e.dept_code = d.dept_code
    WHERE emp_id={user_id};"""

    conn.execute(query)
    res = conn.fetchone()

    return res

def get_report_and_approval_manager(user_id):

    """
    Returns a tuple in the following fomat represents an employee.
    (report_to, approval_manager)

    """

    conn = getCursor()
    query = f"""
    SELECT 
    CONCAT(e2.first_name, ' ', e2.last_name) AS report_to,
    CONCAT(e3.first_name, ' ', e3.last_name) AS approval_manager
    FROM
    employee e1
    INNER JOIN employee e2
    ON e1.report_to = e2.emp_id
    INNER JOIN employee e3
    ON e1.approval_manager = e3.emp_id
    WHERE e1.emp_id={user_id};"""

    conn.execute(query)
    res = conn.fetchone()

    return res

def get_all_employees_by_id(user_id):
    
    conn = getCursor()
    query = f"""
    SELECT emp_id, first_name, last_name, position_title, dept_name, role_name
    FROM employee AS E
    RIGHT JOIN department AS D ON D.dept_code = E.dept_code 
    RIGHT JOIN users AS U ON U.user_id = E.emp_id
    RIGHT JOIN roles AS R ON R.role_id = U.role_id 
    WHERE approval_manager = {user_id}
    ORDER BY last_name;
    """
    conn.execute(query)
    return conn.fetchall()


def get_all_employees_except_id(user_id):
    
    conn = getCursor()
    query = f"""
    SELECT emp_id, first_name, last_name, position_title, dept_name, role_name
    FROM employee AS E
    RIGHT JOIN department AS D ON D.dept_code = E.dept_code 
    RIGHT JOIN users AS U ON U.user_id = E.emp_id
    RIGHT JOIN roles AS R ON R.role_id = U.role_id 
    WHERE emp_id != {user_id}
    ORDER BY last_name;
    """
    conn.execute(query)
    return conn.fetchall()


def get_all_employees_requests(user_id):
    conn = getCursor()

    query = f"""
            SELECT
              R.request_id, R.emp_id, CONCAT(E.first_name, ' ', E.last_name) AS Employee, R.created_on, 
              T.leave_name, S.status_name, CONCAT(A.first_name, ' ', A.last_name) AS Approval_Manager, R.used
            FROM
              leave_request as R
            RIGHT JOIN employee as E
              ON R.emp_id = E.emp_id
            RIGHT JOIN leave_type as T
              ON R.leave_code = T.leave_code
            RIGHT JOIN request_status as S
              ON R.status_id = S.status_id
            RIGHT JOIN employee as A
              ON E.approval_manager = A.emp_id
            WHERE
              R.status_id IN (3,4,5) AND E.approval_manager = {user_id}
            ORDER BY R.created_on DESC;
            """
    
    conn.execute(query)
    all_employees_requests = conn.fetchall()

    return all_employees_requests

def emp_exist(emp_id):
    
    conn = getCursor()
    query = f"SELECT * FROM employee WHERE emp_id={emp_id};"
    conn.execute(query)
    res = conn.fetchone()
    if len(res) > 0:
        return True
    return False

def is_under_manager(emp_id, manager_id):
    
    conn = getCursor()
    query = f"SELECT approval_manager FROM employee WHERE emp_id={emp_id};"
    conn.execute(query)
    res = conn.fetchone()
    if res[0] == manager_id:
        return True
    return False



    

