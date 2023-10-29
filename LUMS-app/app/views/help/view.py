from flask import Blueprint, render_template

help_page = Blueprint('help', __name__)

@help_page.route('/help')
def help():
    return render_template('help/help.html', title='Contact Us') 
