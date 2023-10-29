"""
This file only handles login feature and its related functions.
This file saved user in the session and generated corresponding token.

Author: Leon Huang


"""


from . import auth
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user
from flask import render_template, redirect, url_for, request, session, flash
from .forms import LoginForm
from .forms import RegistrationForm
from .model import * 
from app.views.mw import is_employee, is_manager, is_admin


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Checks if a user has the correct password that matched its username

    :returns: renders a template with given values
    :rtype: function
    """

    form=LoginForm()
    message = None

    if session.get('userID') and session.get('role'):
        return redirect("/")

    print("validating ...")
    if form.validate_on_submit():
        print("form validated.")

        if not user_exists(form.email.data):
            message = "This email doesn't exist, please try another one!"
            
        elif not check_password(form.email.data, form.password.data):
            message = "Password entered is incorrect!"

        else:
            session['userID'] = get_user_id_by_username(form.email.data)
            session['userName'] = get_full_name_by_userid(session['userID'])
            session['role'] = get_role_by_userid(session['userID'])
            print("login successfully!")
            print("Token: ")
            print(encode_auth_token(session['userID']))
            return redirect("/")
    
    return render_template("accounts/login.html", title='Sign in', form=form, message=message)


@auth.route('/logout')
@is_employee
def logout():
    """
    Logs out a user.
    """

    session.pop('userID', None)
    session.pop('userName', None)
    session.pop('role', None)

    return redirect("/login", code=302)


# @auth.route('/test')
# def test():
#     """
#     test
#     """


#     return render_template("test.html")

# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()

#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data

#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#         try:
#             connection = getCursor()
#             query = f"INSERT INTO users (user_name, pwd) VALUES ('{username}', '{hashed_password.decode('utf-8')}');"
#             connection.execute(query)
#             flash("User registered successfully!")
#             return redirect(url_for('/'))
#         except mysql.connector.Error as err:
#             flash(f"Error: {err}")
#             return redirect(url_for('auth.register'))

#     return render_template('accounts/register.html', form=form)