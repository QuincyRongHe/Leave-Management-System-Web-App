from functools import wraps
from flask import Response, request, g, session, redirect




def is_employee(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
            
        if session.get('userID') and session.get('role'):
            if session.get('role') >= 1:
                return func(*args, **kwargs)
            else:
                return Response('Access Denied', mimetype='text/plain', status=401)
            
            
        return redirect('/login')
    return decorated_function


def is_manager(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
            
        if session.get('userID') and session.get('role'):
            if session.get('role') >= 2:
                return func(*args, **kwargs)
            else:
                return Response('Access Denied', mimetype='text/plain', status=401)
                
            
            
        return redirect('/login')
    return decorated_function


def is_admin(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
            
        if session.get('userID') and session.get('role'):
            if session.get('role') >= 3:
                return func(*args, **kwargs)
            else:
                return Response('Access Denied', mimetype='text/plain', status=401)
            
            
        return redirect('/login')
    return decorated_function
 