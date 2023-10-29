
from datetime import datetime
import datetime as dt
import connect
import mysql.connector


# current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

def get_last_pay_date():
    conn = getCursor()
    query = f"SELECT updated_on FROM leave_balance"
    conn.execute(query)
    a_date = conn.fetchone()
    print(query, a_date[0])

    return a_date[0]


def get_available_annual_leave_days(user_id):
    conn = getCursor()

    query = f"""
    SELECT
        al_balance
    FROM
        leave_balance
    WHERE
        emp_id = {user_id};
    """
    
    conn.execute(query)
    al_balance = conn.fetchone()

    if al_balance:


        hours = float(al_balance[0])
        days = hours / 7.5

        return hours, days
    return 0,0


def get_available_sick_leave_days(user_id):
    conn = getCursor()

    query = f"""
    SELECT
        sl_balance
    FROM
        leave_balance
    WHERE
        emp_id = {user_id};
    """
    
    conn.execute(query)

    sl_balance = conn.fetchone()

    if sl_balance:
        sl_balance = sl_balance[0]

        hours = float(sl_balance)
        days = hours / 7.5

        return hours, days
    return 0, 0


def get_my_requests(user_id):
    conn = getCursor()

    query = f"""
            SELECT 
              request_id, R.emp_id, CONCAT (first_name, ' ', last_name) AS employee, R.start_date, R.end_date, R.used, created_on, leave_name, status_name
            FROM 
              leave_request AS R
            RIGHT JOIN 
              leave_type AS T ON T.leave_code = R.leave_code
            RIGHT JOIN 
              request_status AS S ON S.status_id = R.status_id
            RIGHT JOIN
              employee AS E ON E.emp_id = R.emp_id
            WHERE 
              R.emp_id = {user_id}
            ORDER BY
              created_on DESC;
              """
    
    conn.execute(query)
    return conn.fetchall()



def get_all_new_requests(user_id):
    conn = getCursor()

    query = f"""
            SELECT
              R.request_id, R.emp_id, CONCAT(E.first_name, ' ', E.last_name) AS Employee, R.created_on, T.leave_name, R.start_date, R.end_date, S.status_name, CONCAT(A.first_name, ' ', A.last_name) AS Approval_Manager
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
              R.status_id = 2 AND E.approval_manager = {user_id}
            ORDER BY R.created_on DESC;
            """

    conn.execute(query)
    all_new_requests = conn.fetchall()

    return all_new_requests

          

def get_request_by_id(request_id):
    conn = getCursor()

    query = f"""
            SELECT
              R.request_id,
              CONCAT (E1.first_name, ' ', E1.last_name) AS Employee,
              R.created_on,
              T.leave_name,
              R.start_date,
              R.end_date,
              R.note,
              R.used,
              S.status_name,
              CONCAT(E2.first_name, ' ', E2.last_name) AS decision_made_by,
              D.decision_created_on,
              D.comment,
              E1.emp_id
            FROM
              leave_request AS R
            LEFT JOIN 
              leave_type AS T ON R.leave_code = T.leave_code
            LEFT JOIN 
              request_status AS S ON R.status_id = S.status_id
            LEFT JOIN 
              leave_decision AS D ON R.request_id = D.request_id
            LEFT JOIN 
              employee AS E1 ON R.emp_id = E1.emp_id
            LEFT JOIN 
              employee AS E2 ON D.decision_made_by = E2.emp_id
            WHERE
            R.request_id = {request_id};
            """
    
    conn.execute(query)
    get_request_by_id = conn.fetchall()

    return get_request_by_id



def add_decision_to_db(user_id, request_id, current_timestamp, status_id, comment):
    conn = getCursor()

    query = f"""
            INSERT INTO leave_decision (request_id, decision_made_by, decision_created_on, status_id, comment)
            VALUES ({request_id}, {user_id}, '{current_timestamp}', {status_id}, '{comment}');
            """
    
    conn.execute(query)
    conn


def get_audit_history(request_id):
    conn = getCursor()

    query = f"""
            SELECT decision_made_by, decision_created_on, status_id, comment
            FROM leave_decision
            WHERE request_id = {request_id}
            ORDER BY decision_created_on DESC
            """

    conn.execute(query)
    audit_history = conn.fetchall()

    return audit_history



def update_status_in_db(request_id, status_id):
    conn = getCursor()

    query = f"""
            UPDATE leave_request
            SET status_id = {status_id}
            WHERE request_id = {request_id};
            """
    
    conn.execute(query)
    conn



def get_decision_status(request_id, status_id):
    conn = getCursor()

    query = f"""SELECT * FROM leave_request WHERE status_id IN (3, 4, 5);"""
    
    conn.execute(query)
    conn



def delete_requests(request_id):
    conn = getCursor()

    query = f"""
            UPDATE leave_request
            SET status_id = 6
            WHERE (status_id = 1 OR status_id = 2) AND request_id = {request_id};
            """
    
    conn.execute(query)
    conn



def get_leave_balance(emp_id):
        
        conn = getCursor()
        query = f"SELECT al_balance, sl_balance, updated_on FROM leave_balance WHERE emp_id={emp_id} ORDER BY updated_on DESC;"
        conn.execute(query)
        res = conn.fetchone()
        return res


def get_leave_requests(emp_id, leave_type):
    conn = getCursor()
    query = f"""
    SELECT 
    leave_code,
    start_date,
    end_date,
    lr.used,
    status_name,
    lr.request_id
    FROM
        leave_request AS lr
            JOIN
        request_status AS rs ON lr.status_id = rs.status_id
    WHERE
        emp_id = {emp_id} AND leave_code = '{leave_type}';
    """
    conn.execute(query)
    res = conn.fetchall()
    return res

def get_leave_requests_except_status(emp_id, leave_type, status_id=[4,5]):
    conn = getCursor()
    query = f"""
    SELECT 
    leave_code,
    start_date,
    end_date,
    lr.used,
    status_name,
    lr.request_id
    FROM
        leave_request AS lr
            JOIN
        request_status AS rs ON lr.status_id = rs.status_id
    WHERE
        emp_id = {emp_id} AND leave_code = '{leave_type}'
    """
    for i in status_id:
        query += f" AND lr.status_id != {i}"
    query += ";"
    conn.execute(query)
    res = conn.fetchall()
    return res


def add_new_request(user_id, leave_type, start_date, end_date, note, status_id, dt):
    conn = getCursor()

    query = """
    INSERT INTO leave_request (emp_id, leave_code, start_date, end_date, note, status_id, created_on, used)
    VALUES (%s, %s, %s, %s, %s, %s, %s, 0);
    """
    print(query)

    values = (user_id, leave_type, start_date, end_date, note, status_id, dt)
    print(values)

    

    conn.execute(query, values)
    request_id = conn.lastrowid

    return request_id



def get_statuses(isauthorized=False):
    conn = getCursor()

    query = f""" SELECT status_id, status_name FROM request_status WHERE status_id > 2;"""

    if isauthorized:
        query = f""" SELECT status_id, status_name FROM request_status;"""

    conn.execute(query)
    res = conn.fetchall()

    return res


def get_owner_of_request(req_id):
    conn = getCursor()

    query = f""" SELECT emp_id FROM leave_request WHERE request_id = {req_id};"""

    conn.execute(query)
    res = conn.fetchone()

    return res[0] if res else None


def get_approver_of_request(req_id):
    conn = getCursor()

    query = f""" SELECT E.approval_manager FROM leave_request AS L LEFT JOIN 
                    employee AS E ON L.emp_id=E.emp_id WHERE request_id = {req_id};"""

    conn.execute(query)
    print(query)
    res = conn.fetchone()

    return res[0] if res else None


def is_admin(id):
    conn = getCursor()

    query = f"""SELECT role_id FROM users WHERE user_id = {id};"""  
    
    conn.execute(query)
    res = conn.fetchone()
    
    if res and res[0] >= 3:
        return True

    return False


def get_employees_of_manager(manager_id):
    conn = getCursor()

    query = f"""SELECT emp_id FROM employee WHERE approval_manager = {manager_id};"""

    conn.execute(query)
    res = conn.fetchall()

    return [row[0] for row in res] if res else []


def get_a_request(req_id):
    conn = getCursor()

    query = f""" SELECT leave_code, emp_id, start_date, end_date, status_id, used, note, created_on
                    FROM leave_request WHERE request_id = {req_id};"""

    conn.execute(query)
    res = conn.fetchone()

    return res

def get_decisions(req_id):
    conn = getCursor()

    query = f""" SELECT decision_made_by, decision_created_on, status_id, comment FROM leave_decision WHERE request_id = {req_id} ORDER BY decision_created_on DESC;"""

    conn.execute(query)
    res = conn.fetchall()

    return res

def update_request(request_id, leave_type, start_date, end_date, note, status_id=1):
    conn = getCursor()

    query = f""" UPDATE leave_request SET status_id = {status_id}, 
                leave_code='{leave_type}', start_date='{start_date}', end_date='{end_date}', note='{note}' WHERE request_id = {request_id};"""

    conn.execute(query)

    return True

def get_holidays(is_active=True):
    conn = getCursor()
    if is_active:
      query = f"SELECT holiday_name, holiday_year, holiday_month, holiday_day FROM holiday where is_active=1;"
    conn.execute(query)
    holidays = conn.fetchall()
    holis = []

    for holiday in holidays:
        holis.append(dt.date(holiday[1], holiday[2], holiday[3])) 

    return holis

def get_requests_between_dates(emp_id, sdate, edate, type='AL'):
    print('SQL:',sdate, edate)
    conn = getCursor()
    query = f"""SELECT r.start_date, r.end_date, r.status_id FROM leave_request as r WHERE emp_id={emp_id} and leave_code='{type}' and 
                ((r.start_date BETWEEN '{sdate}' AND '{edate}') or (r.end_date BETWEEN '{sdate}' AND '{edate}')) and (r.status_id = 2 or r.status_id = 3);"""
    conn.execute(query)
    print(query)
    al_requests = conn.fetchall()

    return al_requests

def get_requests_made_after_date(emp_id, adate, type='AL'):
    """Return requests that are created after a given date"""
    conn = getCursor()
    query = f"""SELECT r.start_date, r.end_date, r.status_id, r.used FROM leave_request as r WHERE emp_id={emp_id} and 
                r.created_on > '{adate}' and (r.status_id = 2 or r.status_id = 3 or r.status_id = 4) and leave_code = '{type}';"""
    conn.execute(query)
    print(query)
    al_requests = conn.fetchall()

    return al_requests
    

def get_employee_name(emp_id):
    conn = getCursor()
    query = f"SELECT concat(first_name, ' ', last_name) FROM employee WHERE emp_id={emp_id}"
    conn.execute(query)
    emp_name = conn.fetchone()
    return emp_name


def create_notification(user_id, recipient_id, request_id, message, current_timestamp):
    conn = getCursor()
    query = f"""INSERT INTO notifications (sender_id, recipient_id, request_id, message, timestamp) 
                VALUES ({user_id}, {recipient_id}, {request_id}, '{message}', '{current_timestamp}')"""
    
    conn.execute(query)
    return True


def get_notifications_from_db(user_id):
    conn = getCursor()
    query = f"""SELECT notifications.*, employee.first_name, employee.last_name 
                FROM notifications 
                INNER JOIN employee ON notifications.sender_id = employee.emp_id 
                WHERE recipient_id ={user_id} AND read_status = 0 
                ORDER BY timestamp DESC"""
    
    try:
          
      conn.execute(query)
      notifications = conn.fetchall()
    except Exception as e:
        print('!!!!I am trying to get the notifications but something went wrong!!!!')
        print(e)

    
    
    return notifications


def mark_all_notifications_as_read_in_db(user_id):
    conn = getCursor()
    query = f"UPDATE notifications SET read_status = 1 WHERE recipient_id = {user_id} AND read_status = 0"
    conn.execute(query)
    return True


def mark_notification_as_read_in_db(notification_id):
    conn = getCursor()
    query = f"UPDATE notifications SET read_status = 1 WHERE notification_id = {notification_id} AND read_status = 0"
    conn.execute(query)
    return True


def get_last_pay_date():
    conn = getCursor()
    query = "SELECT updated_on FROM leave_balance ORDER BY updated_on DESC LIMIT 1;"
    conn.execute(query)
    result = conn.fetchone()

    if result is not None:
        return result[0]
    else:
        return None



def is_leave_paid(request_id):
    conn = getCursor()
    query = f"SELECT used FROM leave_request WHERE request_id = {request_id}"
    conn.execute(query)
    result = conn.fetchone()
    if result:
        return result[0] == 1
    return False 
