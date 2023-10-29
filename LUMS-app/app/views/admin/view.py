import decimal
from app.views.mw import is_employee, is_admin
from flask import Blueprint, flash, json, jsonify, redirect, render_template, request, session, url_for
from .forms import ChangePWDForm, SearchEmployeeForm
from flask_paginate import Pagination, get_page_parameter

import math



admin = Blueprint('admin', __name__)



from .model import initialize as init
from .model import *
import hashlib, os
from app import SALT_BITS, ITERATION, HASH_MODE

import datetime
import numpy as np
from datetime import timedelta, date






def hash_pwd(pwd):
    salt = os.urandom(SALT_BITS)
    ecoded_pwd = pwd.encode()
    digest = hashlib.pbkdf2_hmac(HASH_MODE, ecoded_pwd, salt, ITERATION).hex()
    return digest, salt.hex()




@admin.route('/godmode/initdb')
def initialize():
    print('Start initializing db')
    print('Start creating tables')
    init()
    


@admin.route('/godmode/hsp')
def hash_sample_pwd():
    initialize()
    print('Start hashing password')
    users = get_all_user_id()
    for user in users:
        id = user[0]
        pwd = get_pwd_by_id(id)
        salt = os.urandom(SALT_BITS)
        ecoded_pwd = pwd.encode()
        digest = hashlib.pbkdf2_hmac(HASH_MODE, ecoded_pwd, salt, ITERATION).hex()
        update_pwd_and_salt(digest, salt.hex(), id)
    print('password hashed successfully')
    return "db created with pwd hashed. "



def last_week_of_year(year):
    last_week = date(year, 12, 28)
    return last_week.isocalendar().week


def get_last_friday():
    now = datetime.date.today()
    closest_friday = now + timedelta(days=(4 - now.weekday()))
    return (closest_friday if closest_friday < now
            else closest_friday - timedelta(days=7))


def get_last_pay_date():
    conn = getCursor()
    query = f"SELECT updated_on FROM leave_balance"
    conn.execute(query)
    a_date = conn.fetchone()
    print(query, a_date[0])

    return a_date[0]
    
def get_all_holidays_with_dates(year=None):
    conn = getCursor()
    query = f"SELECT holiday_name, holiday_year, holiday_month, holiday_day FROM holiday"
    if year:
        query += f" WHERE holiday_year={year};"
    conn.execute(query)
    holidays = conn.fetchall()
    holis = []
    

    for holiday in holidays:
        holis.append(datetime.date(holiday[1], holiday[2], holiday[3])) 

    return holis



def init_balance(to_date):
    
    today = datetime.date.today()
    users = get_all_user_id()
    print("last pay:", to_date)


    holis = get_all_holidays_with_dates()
   
    print(holis)

    for user in users:
        
        id = user[0]
        print("id:", id)
        conn = getCursor()
        query = f"SELECT joined_date FROM users AS u LEFT JOIN employee AS e ON u.user_id=e.emp_id WHERE u.user_id={id}"
        conn.execute(query)
        res = conn.fetchone()
        start = res[0]

        
        # all_days = (start + timedelta(x + 1) for x in range((end - start).days))
        # days = sum(1 for day in all_days if day.weekday() < 5)
        
        holiday_pay_rate = 0.08
        hours_per_week = 37.5 * holiday_pay_rate
        hours_per_day = 7.5
        al_quota = 30 * hours_per_day
        al_balance = 0
        
        for year in range(start.year, to_date.year+1):
            weeks = date(year, 12, 28).isocalendar().week
            # weeks = isoweek.Week.last_week_of_year(year).week
            # weeks = 52
            s = start
            e = to_date


            if year != to_date.year:
                
                e = datetime.date(year, 12, 31)

            if year != start.year:
                s = datetime.date(year, 1, 1)
            
            hours_per_week = al_quota / weeks
            
            days = np.busday_count(begindates=s, enddates=e, weekmask=[1,1,1,1,1,0,0])

            al_balance += (days / 5) * hours_per_week
            print("Start", s, "End", e, "Days", days)
            
        # hours_per_year = 30 * 7.5
        
        

        
        sl_balance = 5 * 7.5
        print(al_balance)
        print(al_balance / 7.5)
        print()

        conn = getCursor()
        query = f"SELECT r.start_date, r.end_date FROM leave_request as r WHERE emp_id={id} and leave_code='AL' and used = 1 and r.end_date < '{to_date}'; "
        # print(query)
        conn.execute(query)
        al_requests = conn.fetchall()
        print(al_requests)
        for request in al_requests:
            ignored_days = 0
            start , end = request[0], request[1]+timedelta(days=1)
            for d in holis:
                if start <= d < end:
                    ignored_days += 1
                    print("holiday: {} numbers: {}".format(d, ignored_days))
            # days = end - start
            leave_days = np.busday_count(begindates=start, enddates=end,weekmask=[1,1,1,1,1,0,0]) - ignored_days
            print("request: {} \nstart: {} end: {}, leave_days: {}, ignored_days: {}".format(request, start, end, leave_days, ignored_days))
            al_balance -= leave_days * 7.5
            print((days, leave_days))
        
        year = today.year
        

        conn = getCursor()
        query = f"SELECT r.start_date, r.end_date FROM leave_request as r WHERE emp_id={id} and leave_code='SL' and used = 1 and year(r.end_date)={year} and r.end_date < '{to_date}';"
        conn.execute(query)
        sl_requests = conn.fetchall()
        print(sl_requests)

        for request in sl_requests:
            ignored_days = 0
            start , end = request[0], request[1]+timedelta(days=1)
            for d in holis:
                if d.year==year and start <= d < end:
                    print((d.year, year))
                    ignored_days += 1
            # days = end - start
            if start.year < year:
                start = date(year, 1, 1)
            leave_days = np.busday_count(begindates=start, enddates=end,weekmask=[1,1,1,1,1,0,0]) - ignored_days
            sl_balance -= leave_days * 7.5
            print((days, sl_balance))
 
        
        conn = getCursor()
        query = f"INSERT INTO leave_balance (emp_id, al_balance, sl_balance, updated_on) VALUES ({id},{al_balance},{sl_balance},'{to_date}');"
        
        print("INSERT QUERY=", query)
        conn.execute(query)
        # print("today", today)


        print("final al balance: ", al_balance)
        print("final sl balance: ", sl_balance)
        print()
        
        

    print('In progress...')




def update_balance(to_date):
    
    today = datetime.date.today()
    users = get_all_user_id()
    print("next pay:", to_date)
    current_pay_date = get_last_pay_date().date()
    new_pay_date = to_date

    if current_pay_date > new_pay_date:
        print("Pay date is not valid")
        return "Pay date is not valid"

    holis = get_all_holidays_with_dates(year=new_pay_date.year)
   
    print(holis)

    for user in users:
        
        id = user[0]
        print("id:", id)


        holiday_pay_rate = 0.08
        hours_per_week = 37.5 * holiday_pay_rate
        hours_per_day = 7.5
        al_quota = 30 * hours_per_day

        conn = getCursor()
        query = f"SELECT al_balance, sl_balance FROM leave_balance WHERE emp_id={id} ORDER BY updated_on DESC LIMIT 1;"
        conn.execute(query)
        balances = conn.fetchone()

        al_balance = balances[0]
        sl_balance = balances[1]
        
        for year in range(current_pay_date.year, new_pay_date.year+1):
            # weeks = date(year, 12, 28).isocalendar().week
            # weeks = isoweek.Week.last_week_of_year(year).week
            weeks = 52
            s = current_pay_date
            e = new_pay_date


            if year != new_pay_date.year:
                
                e = datetime.date(year, 12, 31)

            if year != current_pay_date.year:
                s = datetime.date(year, 1, 1)
            
            hours_per_week = al_quota / weeks

            print("Start", s, "End", e)
            
            days = np.busday_count(begindates=s, enddates=e, weekmask=[1,1,1,1,1,0,0])

            al_balance += decimal.Decimal((days / 5) * hours_per_week)
            print("Start", s, "End", e, "Days", days)
            
        # hours_per_year = 30 * 7.5
        if new_pay_date.year != current_pay_date.year:
            sl_balance = decimal.Decimal(5 * 7.5)

        
        

        print(al_balance)
        print(float(al_balance) / 7.5)
        print()

        conn = getCursor()
        query = f"SELECT r.start_date, r.end_date FROM leave_request as r LEFT JOIN leave_decision as d ON r.request_id=d.request_id WHERE emp_id={id} and r.leave_code='AL' and r.used = 1 and d.decision_created_on > '{current_pay_date}'; "
        print(query)
        conn.execute(query)
        al_requests = conn.fetchall()
        print(al_requests)
        for request in al_requests:
            ignored_days = 0
            start , end = request[0], request[1]+timedelta(days=1)
            for d in holis:
                if start <= d < end:
                    ignored_days += 1
                    print("holiday: {} numbers: {}".format(d, ignored_days))
            # days = end - start
            leave_days = np.busday_count(begindates=start, enddates=end,weekmask=[1,1,1,1,1,0,0]) - ignored_days
            print("request: {} \nstart: {} end: {}, leave_days: {}, ignored_days: {}".format(request, start, end, leave_days, ignored_days))
            al_balance -= decimal.Decimal(leave_days * 7.5)
            print((days, leave_days))
        
        year = today.year
        

        conn = getCursor()
        query = f"SELECT r.start_date, r.end_date FROM leave_request as r LEFT JOIN leave_decision as d ON r.request_id=d.request_id WHERE emp_id={id} and r.leave_code='SL' and used = 1 and year(r.end_date)={year} and d.decision_created_on > '{current_pay_date}';"
        print(query)
        conn.execute(query)
        sl_requests = conn.fetchall()
        print(sl_requests)

        for request in sl_requests:
            ignored_days = 0
            start , end = request[0], request[1]+timedelta(days=1)
            for d in holis:
                if d.year==year and start <= d < end:
                    print((d.year, year))
                    ignored_days += 1
            # days = end - start
            if start.year < year:
                start = date(year, 1, 1)
            leave_days = np.busday_count(begindates=start, enddates=end,weekmask=[1,1,1,1,1,0,0]) - ignored_days
            sl_balance -= decimal.Decimal(leave_days * 7.5)
            print((days, sl_balance))
 
        
        conn = getCursor()
        query = f"UPDATE leave_balance SET al_balance = {al_balance}, sl_balance={sl_balance}, updated_on= '{to_date}' WHERE emp_id={id};"
        conn.execute(query)
        # print("today", today)


        print("final al balance: ", al_balance)
        print("final sl balance: ", sl_balance)
        print()
        
        

    print('In progress...')

    return ""




@admin.route('/godmode/gb')
def generate_balances():

    last_pay_date = get_last_friday()

    init_balance(last_pay_date)

    return ":)"

@admin.route('/godmode/go')
def godmode():

    print("Godmode activated!")
    

    hash_sample_pwd()
    
    generate_balances()
    return "Everything set up!"




@admin.route('/settings')
@is_employee
def showsSettings():

    return render_template('settings/settings.html', title='Settings')

    


@admin.route('/changepwd', methods=['GET', 'POST'])
@is_employee
def changePWD():
    
    form = ChangePWDForm()

    print("change password clicked!")

    if form.validate_on_submit():   
        print("form validated!")
        new_pwd, salt = hash_pwd( form.new_password.data )
        print("New PWD= ", new_pwd, "SALT= ", salt)
        update_pwd_and_salt(new_pwd, salt, session['userID'])
        flash('Your password has been changed!', 'success')
        return redirect('/settings')
        pass
    print(form.errors)
    

    return render_template('settings/changePwd.html', title='Cahnge Password', form=form)


@admin.route('/editholiday', methods=['GET', 'POST'])
@is_admin
def editHoliday():
    # all_holidays = get_all_holidays()
    if request.method == 'POST':
        print("editing.....")
        print(request.get_json())
        today = datetime.datetime.now()
        print(request.get_json())
        update_holidays(request.get_json(), session['userID'], today)
        return "update successfully"

    return render_template('settings/editPublicHolidays.html', title='Holidays')

@admin.route('/getholiday', methods=['GET'])
@is_admin
def getHoliday() -> dict:
    print("In get holiday")

    holidays = get_all_holidays()

    print(holidays)


    for h in holidays:
        for key, value in h.items():
            if key == 'edit_date':
                h[key] = value.strftime("%d-%m-%Y %I:%M %p")

    print(holidays)
    
    return holidays


@admin.route('/add_new_holiday', methods=[ 'POST'])
@is_admin
def addNewHoliday():
    
    print(request.get_json())
    req = request.get_json()
    name = req['holiday_name']
    date = req['holiday_date']
    year = date.split('-')[2]
    month = date.split('-')[1]
    day = date.split('-')[0]
    print(year, month, day)
    today = datetime.datetime.now()
    added_by = session['userID']
    add_new_holidays(name, year, month, day, added_by, today)

    return "added successfully"



@admin.route('/getleavetypes/<returned_attr>', methods=['GET'])
@admin.route('/getleavetypes', methods=['GET'])
@is_admin
def getLeaveTypes(returned_attr: str = None):
    print("In get Leave types")

    leave_types = get_all_leave_types()


    # for h in holidays:
    #     for key, value in h.items():
    #         if key == 'edit_date':
    #             h[key] = value.strftime("%d-%m-%Y %I:%M %p")

    # print("Getting json:", request.get_json())
    print("returned attr:", returned_attr)
    if returned_attr is not None:
        response = []
        for lt in leave_types:
            for key, value in (lt.items() ):
                if key == returned_attr:
                    response.append(value)
        response= json.dumps(response)
        return response
                    


    print(leave_types)
    for lt in leave_types:
        for key, value in lt.items():
            if key == 'leave_per_year' and value is None:
                lt[key] = 'N/A'
    
    
    return leave_types

@admin.route('/editlt', methods=['GET', 'POST'])
@is_admin
def editLeaveTypes():


    if request.method == 'POST':
        print("editing.....")
        # print(request.get_json())
        # today = datetime.datetime.now()
        print(request.get_json())
        update_leave_types(request.get_json())
        return "update successfully"



    return render_template('settings/editLeaveTypes.html', title='Leave Types')


@admin.route('/add_new_leave_type', methods=[ 'POST'])
@is_admin
def addLeaveTypes():
    
    add_leave_types(request.get_json())


    return "added successfully"



@admin.route('/updatebl', methods=['GET', 'POST'])
@is_admin
def updateLeaveBalances():

    print("In update leave balances")
    print("request method:", request.method )

    current_pay_date = get_last_pay_date().date()
    today = datetime.datetime.now().date()

    difference = (current_pay_date - today).days+1
    print("difference:", difference)
    




    if request.method == 'POST':
        print("updating.....")
        # print(request.get_json())
        # today = datetime.datetime.now()
        print(request.get_json())

        new_date = datetime.datetime.strptime(request.get_json()['date'], '%d-%m-%Y').date()

        print("new date:", new_date)

        message = update_balance(new_date)
        flash(message, 'success')

        return redirect('/settings')


    return render_template('settings/updateBalances.html', title='Update Balannces', difference=difference)


@admin.route('/updateroles', methods=['GET', 'POST'])
@is_admin
def updateEmployeeRoles():
    admin_id = session['userID']
    form = SearchEmployeeForm()
    
    if request.method == 'POST':
        selected_employees = request.form.getlist('selected_employees[]')
        for employee_id in selected_employees:
            new_role = request.form.get(f'new_role_{employee_id}')
            update_roles_for_employees(employee_id, new_role)
        
        
        return redirect(url_for('admin.updateEmployeeRoles'))
    
    all_employee_roles = get_role_for_all_employees(admin_id)
    
    # Pagination configuration
    page = request.args.get('page', type=int, default=1)
    per_page = 10  # Number of items to display per page
    total = len(all_employee_roles)
    pages = math.ceil(total / per_page)
    
    # Calculate the indices for the current page
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total)
    
    # Get the current page of employee roles
    current_page_roles = all_employee_roles[start_idx:end_idx]
    
    return render_template('settings/updateEmployeeRoles.html',
                       title='Update Roles',
                       allEmployeeRoles=current_page_roles,
                       page=page,
                       per_page=per_page,
                       total=total,
                       pages=pages,
                       start_idx=start_idx + 1,  # add 1 because indexing in Python starts from 0
                       end_idx=end_idx,
                       form=form)

@admin.route('/settings/roles/search', methods=['POST'])
@is_admin
def searchEmployees():
    admin_id = session['userID']
    form = SearchEmployeeForm()

    if form.reset.data:
        return redirect(url_for('admin.updateEmployeeRoles'))

    if form.validate_on_submit():

        print("searching.....")
        search = None if form.search.data == '' else form.search.data
        role = None if form.select_role.data == -1 else form.select_role.data 

        search_results =  search_roles(admin_id, role_id=role, name=search)

         
        # Pagination configuration
        page = request.args.get('page', type=int, default=1)
        per_page = 10  # Number of items to display per page
        total = len(search_results)
        pages = math.ceil(total / per_page)
        
        # Calculate the indices for the current page
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total)
        
        # Get the current page of employee roles
        results = search_results[start_idx:end_idx]


        return render_template('settings/updateEmployeeRoles.html',
                                    title='Update Roles',
                                    allEmployeeRoles=results,
                                    page=page,
                                    per_page=per_page,
                                    total=total,
                                    pages=pages,
                                    start_idx=start_idx + 1,  # add 1 because indexing in Python starts from 0
                                    end_idx=end_idx,
                                    form=form)
    print("form not validated")
    print(form.errors)
    
    return redirect(url_for('admin.updateEmployeeRoles'))
    









