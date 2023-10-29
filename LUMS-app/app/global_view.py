import os
from app import app
from flask import render_template, request, url_for
from datetime import datetime as dt
from app.views.mw import *
from app.views.admin.view import get_last_pay_date

@app.template_filter()
def nz_date(value, symbol='-'):
    if value:
        return value.strftime(f'%d{symbol}%m{symbol}%Y')
    return value

    

@app.template_filter()
def time(value):

    actual_time = (dt.datetime.min + value).time()

    return actual_time.strftime('%I:%M %p')

@app.template_filter()
def format_date_time(value):

    # return dt.now(pytz.timezone('Pacific/Auckland')).strftime("%d-%m-%Y %I:%M %p")

    return value.strftime('%d-%m-%Y %I:%M %p')

@app.context_processor
def global_function():

    return dict()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_pages/404.html')

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error_pages/500.html')

@app.errorhandler(401)
def page_not_found(e):
    return render_template('error_pages/401.html')


@app.before_request
def hook():
    # request - flask.request
    print('endpoint: %s, url: %s, path: %s' % (
        request.endpoint,
        request.url,
        request.path))
    




@app.route('/')
@is_employee
def home():

    if session.get("userID"):
        return redirect("/dashboard")

    return redirect(url_for('request.dashboard'))

@app.route('/test')
def test():


    return render_template('profile/projectedLeaves.html')


@app.route('/myorg')
def myorg():
    return render_template('myorg.html')
