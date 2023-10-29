
import json 
from flask import jsonify
from flask import Blueprint, request as flask_request, session, render_template, redirect, flash, url_for, abort
from app.views.mw import is_employee, is_manager, is_admin
from .model import *
from .forms import LeaveRequestForm, LeaveRequestEditForm

import datetime as dt
import numpy as np
from datetime import timedelta, datetime
from decimal import Decimal

from flask_paginate import Pagination, get_page_parameter
import math

from flask_wtf.csrf import CSRFProtect

import pytz

request = Blueprint('request', __name__)
csrf = CSRFProtect()

current_timestamp = dt.datetime.now(pytz.timezone('pacific/Auckland')).strftime('%Y-%m-%d %H:%M:%S')


def calcLeave_by_two_dates(start, end):

    holidays = get_holidays(is_active=True)
    start_date = start
    end_date = end
    days = (end_date - start_date).days+1
    print(start_date, end_date, days)
    leave_days = np.busday_count(begindates=start_date, enddates=end_date,weekmask=[1,1,1,1,1,0,0])+1


    weekend_count = days - leave_days
    ignored_days = 0
 
    for d in holidays:
        if start_date <= d and d <= end_date:
            ignored_days += 1
            print(ignored_days, d, start_date, end_date)
    # days = end - start
    leave_days = leave_days - ignored_days
    return int(leave_days), int(weekend_count), int(ignored_days)


def has_overlapped_requests( start , end):

    requests = get_leave_requests(session['userID'], 'AL')
    for request in requests:
        if request[1] <= start <= request[2] or request[1] <= end <= request[2]:
            return True


###....... dashboard info ........###


@request.route('/dashboard')
@is_employee
def dashboard():
    id = session['userID']

    sick_leave_hours, sick_leave_days = get_available_sick_leave_days(id)
    annual_leave_hours, annual_leave_days = get_available_annual_leave_days(id)
    my_leave_requests = get_my_requests(id)
    last_pay_date = get_last_pay_date()
    weekday = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday',6:'Sunday'}


    return render_template("dashboard/mydashboard.html", title='My Dashboard',
                           sickLeaveHours=sick_leave_hours,
                           sickLeaveDays=sick_leave_days,
                           annualLeaveHours=annual_leave_hours,
                           annualLeaveDays=annual_leave_days,
                           myLeaveRequests=my_leave_requests, 
                           last_pay_date = last_pay_date,
                           weekday=weekday[last_pay_date.weekday()]
                           )



###....... leave requests history and details ........###

@request.route('/leaverequests', methods=['GET'])
@request.route('/leaverequests/_/_/<int:status>', methods=['GET'])
@request.route('/leaverequests/<int:emp_id>', methods=['GET'])
@request.route('/leaverequests/<int:emp_id>/<int:request_id>', methods=['GET'])
@is_employee
def viewMyRequests(emp_id=None, request_id=None, status=None):
    
    name = ""
    id = session['userID']

    # Case when specific employee's requests are being accessed
    if emp_id is not None:
        if id != emp_id:
            if is_admin(id):
                id = emp_id  # if the user is admin, they can view any employee's requests
                name = get_employee_name(id)[0]
            else:
                managed_employees = get_employees_of_manager(id)
                if emp_id not in managed_employees:
                    return render_template('error_pages/401.html')
                else:
                    id = emp_id  # if the user is a manager, they can view their managed employees' requests
                    name = get_employee_name(id)[0]
                    

    # Case when specific leave request is being accessed
    if request_id is not None:
        request_owner = get_owner_of_request(request_id)
        approver = get_approver_of_request(request_id)
        
        if id != request_owner and id != approver and not is_admin(id):
            return render_template('error_pages/401.html')

    if request_id is not None:
        leave_request_details = get_request_by_id(request_id)

        start = leave_request_details[0][4]
        end = leave_request_details[0][5]

        leave, _, _ = calcLeave_by_two_dates(start, end)

         # Fetch the audit history for the request
        audit_history = get_audit_history(request_id)
        
        return render_template("request/requestDetails.html",
                               leaveRequestDetails=leave_request_details,
                               emp_id=id,
                               leave=leave,
                               show_approval_options=id in [request_owner, approver],
                               name=name,
                               audit_history=audit_history)

    my_leave_requests = get_my_requests(id)

     # Fetch the audit history for each leave request
    for request in my_leave_requests:
        request_id = request[0]
        request_audit_history = get_audit_history(request_id)
        
        # Add the audit history to the request tuple
        request += (request_audit_history,)


    # Pagination configuration
    page = flask_request.args.get('page', type=int, default=1)
    per_page = 10  # Number of items to display per page
    total_requests = len(my_leave_requests)
    pages = math.ceil(total_requests / per_page)

    # Calculate the indices for the current page
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_requests)

    # Get the current page of leave requests
    current_page_requests = my_leave_requests[start_idx:end_idx]

    pagination = Pagination(page=page, per_page=per_page, total=total_requests, css_framework='bootstrap4')

    return render_template("request/request.html",
                           myLeaveRequests=current_page_requests,
                           emp_id=id,
                           status=status,
                           pagination=pagination,
                           start_idx=start_idx + 1,
                           end_idx=end_idx,
                           page=page,
                           pages=pages,
                           total_requests=total_requests,
                           name=name)



###....... new requests and details ........###



@request.route('/newrequests', methods=['GET', 'POST'])
@request.route('/newrequests/<int:request_id>', methods=['GET', 'POST'])
@is_manager
def approveLeaves(request_id=None):

    """
    Shows new submitted request which needs action
    """

    logged_in_user = session.get('userID')
    if request_id is not None:
        approver = get_approver_of_request(request_id)
        print(f"Approver for request {request_id}: {approver}")  # Debug print

        if approver != logged_in_user:
            return render_template('error_pages/401.html')

        # Fetch the current status of the request
        req = get_a_request(request_id)
        req_status = req[4]

        if req_status == 6:
            return render_template('error_pages/requestError.html')

        request_info = get_request_by_id(request_id)

        start = request_info[0][4]
        end = request_info[0][5]

        leave, _, _ = calcLeave_by_two_dates(start, end)

        return render_template("request/requestDetails.html",
                               leaveRequestDetails=request_info,
                               current_endpoint='approveLeaves',
                               emp_id=logged_in_user,
                               leave=leave)
    else:
        all_new_requests = get_all_new_requests(logged_in_user)

        return render_template("request/newRequests.html", title='New Requests',
                               allNewRequests=all_new_requests)



###....... decision making of leave requests ........###


@request.route('/leave_decision/<int:request_id>', methods=['POST'])
@is_manager
def leave_decision(request_id):
    decision = flask_request.form['decision']
    comment = flask_request.form['comment']
    user_id = session['userID']

    # Fetch the current status of the request
    req = get_a_request(request_id)
    req_status = req[4]

    if req_status == 6:
        return render_template('error_pages/requestError.html')

    if decision == 'Approve':
        status_id = 3  
    elif decision == 'Reject':
        status_id = 4  
    elif decision == 'Delete':
        status_id = 5
    else:
        status_id = 2

    update_status_in_db(request_id, status_id)
    add_decision_to_db(user_id, request_id, current_timestamp, status_id, comment)

    if status_id in [3, 4, 5]:
        user_name = get_employee_name(user_id)[0]
        message = f"""New response received from {user_name}"""
        recipient_id = get_owner_of_request(request_id)
        create_notification(user_id, recipient_id, request_id, message, current_timestamp)


    return redirect(url_for('request.approveLeaves'))



###....... leave applications, modifications and deletions ........###


# @request.route('/checkapply', methods=['POST'])
# def check_apply():
#     form = LeaveRequestForm()

#     print(form.validate_on_submit())

#     return json.dumps( {'data':form.validate_on_submit()})

@request.route('/apply', methods=['GET'])
@request.route('/apply', methods=['POST'])
@request.route('/apply/<int:check>', methods=['POST'])
@is_employee
def apply(check=0):
    form = LeaveRequestForm()

    print("Checking....", form.validate_on_submit(), check)

    # if check == 1:
    #     return json.dumps({'data': form.validate_on_submit()})

    print(form.start_date.data, form.end_date.data, form.leave_type.data, form.reason.data, form.submit.data)
    print(form.errors)
    sdate = dt.date.today() +timedelta(days=30)
    edate = dt.date.today() +timedelta(weeks=52)


    if form.validate_on_submit():
        print('validated')
        

        start_date = form.start_date.data
        end_date = form.end_date.data
        leave_type = form.leave_type.data
        reason = form.reason.data
        status_id = 1 if form.save.data else 2
        # if check == 1:
        #     form.start_date.data = start_date
        #     form.end_date.data = end_date
        #     form.leave_type.data = leave_type  
        #     return json.dumps({'data': True})
        
        # current_time = dt.datetime.now(pytz.timezone('pacific/Auckland'))
        request_id = add_new_request(session['userID'], leave_type, start_date, end_date, reason, status_id, current_timestamp)
        print(status_id, start_date, end_date, leave_type, reason)

        
        # insert_leave_request(session['userID'], start_date, end_date, leave_type, reason)

        if status_id == 2:
                emp_id = session['userID']
                user_name = get_employee_name(emp_id)[0]

                message = f"""New request received from {user_name}"""
                recipient_id = get_approver_of_request(request_id) 
                create_notification(emp_id, recipient_id, request_id, message, current_timestamp) 
                return redirect('/leaverequests/_/_/1')

        return redirect('/leaverequests/_/_/2')
    
    if flask_request.method == 'GET':
        print('get')
        form.errors.clear()
    if form.errors:
        print('errors')
        print(form.errors)
    # if check == 1:
    #         return json.dumps({'data': False})
    
    return render_template("request/application.html", title='Apply for Leave', form=form, sdate=sdate, edate=edate)



@request.route('/modify/<int:req_id>', methods=['GET', 'POST'])
@is_employee
def modify(req_id):
    is_owner = True if session['userID'] == get_owner_of_request(req_id) else False
    is_manager = False
    if not is_owner:
        is_manager = True if session['userID'] == get_approver_of_request(req_id) else False

        if not is_manager:
            flash("You are not authorized to modify this request.", "error")
            return redirect('/leaverequests')
    
    print('first gate passed')
    req = get_a_request(req_id)
    req_status = int(req[4])
        
    print('second gate passed')
    req_sender, req_start_date, req_end_date = req[1], req[2], req[3]
    req_leave_type, req_used, req_reason = req[0], req[5], req[6]
    print('third gate passed')
    decisions = get_decisions(req_id)
    print(decisions)
    req_comment = ""
    if decisions:
        req_comment = decisions[0][3]
    
    _form = LeaveRequestEditForm(isManager=is_manager)
    print('Form created')
    _form.request_id.data = req_id
    
    if flask_request.method == 'GET':
        print('Method = "GET"')
        _form.leave_type.data = req_leave_type
        _form.start_date.data = req_start_date
        _form.end_date.data = req_end_date
        _form.reason.data = req_reason

    if is_manager:
        print('This is a manager')
        _form.comment.data = req_comment

    if _form.validate_on_submit():
        print("Validated....")
        leave_type = _form.leave_type.data
        start_date = _form.start_date.data
        end_date = _form.end_date.data
        reason = _form.reason.data
        
        if _form.save.data or _form.submit.data:  # Allow both save and submit actions
            print('Clicked SAVE or SUBMIT')
            req_status = 2 if _form.submit.data else 1  # 2 for submitted, 1 for saved
            
            if is_manager and _form.submit.data:
                print('Manager submitted a decision')
                
            if req_status == 2:
                # Notification for manager's decision
                emp_id = session['userID']
                user_name = get_employee_name(emp_id)[0]
                message = f"New request received from {user_name}"
                recipient_id = get_approver_of_request(req_id)
                create_notification(emp_id, recipient_id, req_id, message, current_timestamp)
            
            update_request(req_id, leave_type, start_date, end_date, reason, status_id=req_status)
            
            if is_manager:
                flash("Update successful", "success")  # Flash the success message
                return redirect(f'/newrequests/{req_id}')  # Redirect to /newrequests/<int:request_id>
            else:
                return redirect('/leaverequests')

    return render_template("request/application.html", title='Modify Leave Request', form=_form, isManager=is_manager, req_id=req_id, status_id=req_status)



@request.route('/delete/<int:request_id>', methods=['POST'])
@is_employee
def delete(request_id):

    #delete request by employee from unactioned request, set it as cancelled.

    delete_requests(request_id)

    return redirect(url_for('request.viewMyRequests'))



###....... leave balance ........###


@csrf.exempt
@request.route('/projectleaves', methods=['POST'])
@request.route('/projectleaves/<int:emp_id>', methods=['POST'])
@is_employee
def calcProjectedLeaves(emp_id=None):
    """calc projected leaves"""

    req_data = flask_request.get_json()
    asked_date = req_data['todate'] 

    
    
    emp_id = req_data['emp_id']

    # print(close_of_last_pay)
    balances = get_leave_balance(emp_id)

    close_of_last_pay = balances[2]
    final_balance = balances[0]
    
    start_date = close_of_last_pay.date()
    
    
    date_format = "%d/%m/%Y"
    end_date = datetime.strptime(asked_date, date_format).date()
    print("11111111111111111111",end_date)
    # days = abs((end_date - start_date).days)

    # get all the requests overlapping the period
    
    requests = get_requests_between_dates(emp_id, start_date, end_date, 'AL')

    past_requests = get_requests_made_after_date(emp_id, start_date, 'AL')

    print("Request: ",requests)

    # get all holidays 
    
    holidays = get_holidays(is_active=True)


    holiday_pay_rate = 0.08
    hours_per_week = 37.5 * holiday_pay_rate
    hours_per_day = 7.5
    al_quota = 30 * hours_per_day
    accrual_balance = 0
    
    for year in range(start_date.year, end_date.year+1):
        # weeks = date(year, 12, 28).isocalendar().week
        # weeks = isoweek.Week.last_week_of_year(year).week
        weeks = 52
        s = start_date
        e = end_date


        if year != end_date.year:
            
            e = dt.date(year, 12, 31)

        if year != start_date.year:
            s = dt.date(year, 1, 1)
        
        hours_per_week = al_quota / weeks
        
        days = np.busday_count(begindates=s, enddates=e, weekmask=[1,1,1,1,1,0,0])

        accrual_balance += (days / 5) * hours_per_week
        print("Start", s, "End", e, "Days", days)

    leave_days=0
    approved_not_paid= 0
    applied_not_approved = 0

    for request in requests:
        ignored_days = 0
        start , end = request[0], request[1]
        status = request[2]

        print(request)
        
        if start < start_date:
            start = start_date
        if end > end_date:
            end = end_date
        for d in holidays:
            if start <= d and d <= end:
                ignored_days += 1
                print(ignored_days, d, start, end)
        # days = end - start
        leave_days = np.busday_count(begindates=start, enddates=end,weekmask=[1,1,1,1,1,0,0]) - ignored_days +1
        if status == 3:
            approved_not_paid += leave_days*7.5
        elif status == 2:
            applied_not_approved += leave_days*7.5
        # if leave_days>0:
        #     accrual_balance -= leave_days * 7.5
        print((days, leave_days))

    for request in past_requests:
        ignored_days = 0
        start , end = request[0], request[1]
        status = request[2]
        is_used = request[3]

        print(request)
        
        # if start < start_date:
        #     start = start_date
        # if end > end_date:
        #     end = end_date
        for d in holidays:
            if start <= d and d <= end:
                ignored_days += 1
                print(ignored_days, d, start, end)
        # days = end - start
        leave_days = np.busday_count(begindates=start, enddates=end,weekmask=[1,1,1,1,1,0,0]) - ignored_days+1
        if status == 3 and not is_used:
            approved_not_paid += leave_days*7.5
        elif status == 2:
            applied_not_approved += leave_days*7.5
        # if leave_days>0:
        #     accrual_balance -= leave_days * 7.5
        print((days, leave_days))

    # is_positive = 1
    # if al_balance < 0:
    #     is_positive = 0
    #     al_balance = abs(al_balance)

    print(final_balance, approved_not_paid, applied_not_approved, accrual_balance)


    final_balance = float(final_balance) - float(approved_not_paid) - float(applied_not_approved) + float(accrual_balance)
    final_days = round((final_balance)/ 7.5, 2)
    final_balance = round(final_balance, 2)
    accrual_balance = float(round(accrual_balance,2 ))
    approved_not_paid = float(round(approved_not_paid, 2))
    applied_not_approved = float(round(applied_not_approved, 2))   

    
    


    resp = [str(close_of_last_pay.date()), accrual_balance, round(accrual_balance/7.5, 2), approved_not_paid, round(approved_not_paid/7.5, 2), 
            applied_not_approved, round(applied_not_approved/7.5, 2), final_balance, final_days]
    
    print(resp)
    return json.dumps({'success':True, 'data':resp}), 200, {'ContentType':'application/json'} 



@request.route('/leavebalance', methods=['GET'])
@request.route('/leavebalance/<int:emp_id>', methods=['GET'])
@is_employee
def myLeaveBalance(emp_id=None):
    """
    Shows the leave balance of the chosen user
    """

    # endopoint = flask_request.referrer
    # print("EP:::", endopoint)
    name = ""
    id = session['userID']
    if emp_id:
        id = emp_id
        if get_approver_of_request(id) != session['userID'] and not session['role'] != 3:
            return abort(401)
        name = get_employee_name(id)[0]

    

        

    

    leave_balance = get_leave_balance(id)

    al_balance = round(leave_balance[0], 2)    
    sl_balance = round(leave_balance[1], 2)
    close_of_last_pay = leave_balance[2]

    print(al_balance, sl_balance, close_of_last_pay)
    al_requests = get_leave_requests(id, 'AL')
    sl_requests = get_leave_requests(id, 'SL')
    al_leave_approved_not_paid = 0
    al_leave_applied_not_approved = 0

    sl_leave_approved_not_paid = 0
    sl_leave_applied_not_approved = 0
    
    for request in al_requests:
        if request[4] == 'Approved' and not request[3]:
            al_leave_approved_not_paid += np.busday_count(request[1], request[2]+timedelta(days=1))*7.5
        elif request[4] == 'Submitted':
            al_leave_applied_not_approved += np.busday_count(request[1], request[2]+timedelta(days=1))*7.5

    al = ('Annual Leave', al_balance, al_leave_approved_not_paid, round(al_leave_approved_not_paid/7.5, 2), al_leave_applied_not_approved, round(al_leave_applied_not_approved/7.5, 2))


    print('SL', sl_requests, 'AL', al_requests)
    for request in sl_requests:
        if request[4] == 'Approved' and not request[3]:
            sl_leave_approved_not_paid += np.busday_count(request[1], request[2]+timedelta(days=1))*7.5
        elif request[4] == 'Submitted':
            sl_leave_applied_not_approved += np.busday_count(request[1], request[2]+timedelta(days=1))*7.5


    sl = ('Sick Leave', sl_balance, sl_leave_approved_not_paid, round(sl_leave_approved_not_paid/7.5, 2), sl_leave_applied_not_approved, round(sl_leave_applied_not_approved/7.5, 2))

    balances = [al, sl]
    print(balances)
    
    
    return render_template("request/leaveBalance.html", title='My Leave Balance', balances=balances, close_of_last_pay=close_of_last_pay, emp_id=id, name=name)






@request.route('/caleave', methods=['POST'])
@is_employee
def calcLeave():

    req = flask_request.get_json()
    print(req)
    start = datetime.strptime(req['start'], '%Y-%m-%d').date()
    end = datetime.strptime(req['end'], '%Y-%m-%d').date()

    leave_days, weekend_count, ignored_days = calcLeave_by_two_dates(start, end)

    
    resp = {}
    resp['leave_days'] = leave_days
    resp['ignored_days'] = ignored_days
    resp['weekend_count'] = weekend_count
    print(resp)
    
    return json.dumps({'success':True, 'data':resp}), 200, {'ContentType':'application/json'} 
    


###.......notifications........###



@request.route('/api/notifications', methods=['GET'])
@is_employee
def get_notifications():
    notifications = []
    recipient_id = session['userID']
    try:

        notifications = get_notifications_from_db(recipient_id)
    except Exception as e:
        print(e)


    return jsonify(notifications)


@request.route('/api/mark_all_notifications_read', methods=['PUT'])
@is_employee
def mark_all_notifications_read():
    user_id = session['userID']
    
    mark_all_notifications_as_read_in_db(user_id)
    return jsonify({'success': True})


@request.route('/api/mark_notification_read/<int:notification_id>', methods=['PUT'])
@is_employee
def mark_notification_read(notification_id):
    mark_notification_as_read_in_db(notification_id)
    return jsonify({'success': True})



@request.route('/check_holiday')
@is_employee
def getallHoliday():


    holidays = get_holidays(is_active=True)

    ans = {}

    i = 0
    print("Holidays:::", holidays)

    for holiday in holidays:

        ans[i] = f"{holiday.strftime('%d/%m/%Y')}"
        i += 1




    print("Holidays:::", ans)

    
    
    return json.dumps({'success':True, 'data':ans})


