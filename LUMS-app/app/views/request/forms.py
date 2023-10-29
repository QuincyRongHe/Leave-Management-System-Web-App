from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField, TextAreaField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email
from ..request.model import getCursor, get_leave_requests_except_status



class LeaveRequestForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(LeaveRequestForm, self).__init__(*args, **kwargs)

        conn = getCursor()
        query = "SELECT leave_code, leave_name FROM leave_type WHERE is_active = 1;"
        conn.execute(query)
        result = conn.fetchall()

        self.leave_type.choices = [(leave[0], leave[1]) for leave in result]



    leave_type = SelectField('Leave Type', validators=[DataRequired()], coerce=str)
    
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    reason = StringField('Additional Information')
    save = SubmitField('Save')
    submit = SubmitField('Submit')

    def validate_end_date(form, field):
        start = form.start_date.data
        end = field.data
        if end < start:
            raise ValidationError('Start date cannot be later than end date!')
        
        requests = get_leave_requests_except_status(session['userID'], 'AL')

        overlapped = False

        size = len(requests)
        i = 0

        print("size: ", size)
        

        while not overlapped:  
            overlapped = True
            print("i: ", i)
            

            if i == size:
                break

            print("start: ", start)
            print("end: ", end)
            print("request_start: ", requests[i][1])
            print("request_end: ", requests[i][2])
            print("overlapped: ", overlapped)

            if end < requests[i][1] :
                overlapped =  False
          
            elif start > requests[i][2]:
                overlapped =  False
            if overlapped:
                raise ValidationError('Leave request not valid. There is a request from {} to {}!'.format(requests[i][1], requests[i][2]))
            i += 1
            


class LeaveRequestEditForm(FlaskForm):


    def __init__(self, *args, **kwargs):
        super(LeaveRequestEditForm, self).__init__(*args, **kwargs)

        conn = getCursor()
        query = "SELECT leave_code, leave_name FROM leave_type WHERE is_active = 1;"
        conn.execute(query)
        result = conn.fetchall()

        self.leave_type.choices = [(leave[0], leave[1]) for leave in result]


    request_id = IntegerField('Request ID', validators=[DataRequired()])
    leave_type = SelectField('Leave Type', validators=[DataRequired()], coerce=str)
    
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    
    reason = TextAreaField('Additional Information')

    # status = SelectField('Status', validators=[], coerce=str, choices=[])
    comment = TextAreaField('Comment')
    save = SubmitField('Save')
    submit = SubmitField('Submit Request')


    def validate_end_date(form, field):
        start = form.start_date.data
        end = field.data
        if end < start:
            raise ValidationError('Start date cannot be later than end date!')
        
        requests = get_leave_requests_except_status(session['userID'], 'AL')

        overlapped = False

        size = len(requests)
        i = 0

        print("size: ", size)
        

        while not overlapped:  
            overlapped = True
            print("i: ", i)
            

            if i == size:
                break

            print("request_id: ", form.request_id.data)
            print("request_id: ", requests[i][0])
            print("start: ", start)
            print("end: ", end)
            print("request_start: ", requests[i][1])
            print("request_end: ", requests[i][2])
            print("overlapped: ", overlapped)

            if requests[i][5] == form.request_id.data:
                overlapped = False
    
            elif end < requests[i][1] :
                overlapped =  False
          
            elif start > requests[i][2]:
                overlapped =  False
            if overlapped:
                raise ValidationError('it has overlapped requests! There is a request from {} to {}!'.format(requests[i][1], requests[i][2]))
            i += 1
            
               
                

        
            
        
        

