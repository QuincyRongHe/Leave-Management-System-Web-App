from flask import Blueprint,render_template, url_for, flash, redirect, request, abort,session
from .model import get_al_liability_data, get_leave_expetion_data
from app.views.mw import is_manager

report = Blueprint('report', __name__)


@report.route('/report')
@is_manager
def reportPage():

    

    return render_template('report/reportLandingPage.html', title='Report')

@report.route('/alreport')
@is_manager
def annualRport():

    data = get_al_liability_data(session['userID'])
    

    return render_template('report/annualLeaveReport.html', title='Report', data=data)




@report.route('/lereport')
@is_manager
def exceptionReport():

    data = get_leave_expetion_data(session['userID'])
    

    return render_template('report/leaveExceptionReport.html', title='Report', data=data)



