from flask import Blueprint, request, session, render_template, redirect
from app.views.mw import is_employee, is_manager, is_admin
from .model import *
from flask_paginate import Pagination, get_page_parameter

import math

profile = Blueprint('profile', __name__)


@profile.route('/myprofile')
@is_employee
def myprofile():
    """
    renders profile template and shows the profile of current user
    """

    id = session['userID']

    basic_details = get_details_by_id(id)
    pos_and_date = get_position_and_date(id)
    dept_name = get_dept_name(id)
    report_approval_manager = get_report_and_approval_manager(id)


    

    return render_template("profile/profile.html", title='My Profile', 
                           basicDetail=basic_details,
                           posAndDate = pos_and_date,
                           deptName=dept_name,
                           reportApprovalManager=report_approval_manager)


from flask import Blueprint, request, session, render_template, redirect
from app.views.mw import is_employee, is_manager, is_admin
from .model import *

profile = Blueprint('profile', __name__)


@profile.route('/myprofile')
@is_employee
def myprofile():
    """
    renders profile template and shows the profile of current user
    """

    id = session['userID']

    basic_details = get_details_by_id(id)
    pos_and_date = get_position_and_date(id)
    dept_name = get_dept_name(id)
    report_approval_manager = get_report_and_approval_manager(id)


    

    return render_template("profile/profile.html", title='My Profile', 
                           basicDetail=basic_details,
                           posAndDate = pos_and_date,
                           deptName=dept_name,
                           reportApprovalManager=report_approval_manager)


@profile.route('/view/profile/employees')
@profile.route('/view/profile/employees/<int:emp_id>', methods=['GET'])
@is_manager
def viewMyEmployees(emp_id=None):
    """Shows all employees"""
    id = session['userID']

    if emp_id:
        # check if the employee is under the manager's
        # if not is_under_manager(emp_id, id):
        #     pass
        if not emp_exist(emp_id):
            return render_template("error_pages/error.html", title='Error', message="Employee doesn't exist!")

        if not is_under_manager(emp_id, id) and get_role_by_id(id) != 3:
            return render_template("error_pages/401.html", title='Error', message="You have no right to access.")
        basic_details = get_details_by_id(emp_id)
        
        pos_and_date = get_position_and_date(emp_id)
        dept_name = get_dept_name(emp_id)
        report_approval_manager = get_report_and_approval_manager(emp_id)

        return render_template("profile/profile.html", title=f'Profile of an {basic_details[4]}', 
                           basicDetail=basic_details,
                           posAndDate=pos_and_date,
                           deptName=dept_name,
                           reportApprovalManager=report_approval_manager)
        
    if get_role_by_id(id) == 3:
        all_employees = get_all_employees_except_id(id)
    else:
        all_employees = get_all_employees_by_id(id)

    all_employees_requests = get_all_employees_requests(id)

    search_name = request.args.get('search_name', '')
    search_status = request.args.get('search_status', '')

    if search_name:
        all_employees_requests = [r for r in all_employees_requests if search_name.lower() in r[2].lower()]
    if search_status:
        all_employees_requests = [r for r in all_employees_requests if search_status.lower() == r[5].lower()]

    # Pagination configuration
    page = request.args.get('page', type=int, default=1)
    per_page = 10  
    total = len(all_employees)  # Fix: Use the correct count of all_employees
    pages = math.ceil(total / per_page)
    
    # Calculate the indices for the current page
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total)
    
    # Get the current page of employee roles
    current_page_profile = all_employees[start_idx:end_idx]  # Fix: Use all_employees instead of get_all_employees_except_id(id)

    # Pagination configuration for requests
    request_page = request.args.get('request_page', type=int, default=1)
    request_per_page = 10  # Number of items to display per page
    request_total = len(all_employees_requests)
    request_pages = math.ceil(request_total / request_per_page)
    
    # Calculate the indices for the current request page
    request_start_idx = (request_page - 1) * request_per_page
    request_end_idx = min(request_start_idx + request_per_page, request_total)
    
    # Get the current page of employee requests
    current_page_requests = all_employees_requests[request_start_idx:request_end_idx]
    
    return render_template("profile/allEmployees.html", title='My Employees',
                   employees=current_page_profile,
                   allEmployeesRequests=current_page_requests,
                   page=page,
                   per_page=per_page,
                   total=total,
                   pages=pages,
                   start_idx=start_idx + 1,
                   end_idx=end_idx,
                   request_page=request_page,
                   request_per_page=request_per_page,
                   request_total=request_total,
                   request_pages=request_pages,
                   request_start_idx=request_start_idx + 1,
                   request_end_idx=request_end_idx)

