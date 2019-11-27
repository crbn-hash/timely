from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
import datetime
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
admin = Admin(app)



shift_employee_table = db.Table('shift-employees', db.Column('shift_id',db.Integer(), db.ForeignKey('shift.id')), db.Column('employee_id',db.Integer(), db.ForeignKey('employee.id')))

class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<Employee '{}'>".format(self.username)

class Schedule(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80))
    #__tablename__ = 'Schedule'
    shifts = db.relationship(
        'Shift',
        backref='schedule',
        #lazy='dynamic'
    )

    def __init__(self,title):
        self.title = title
    
    def __repr__(self):
        return "<Schedule '{}'>".format(self.title)

class Shift(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    #start_dt = db.Column(db.DateTime())
    #end_dt = db.Column(db.DateTime())
    schedule_id = db.Column(db.Integer(), db.ForeignKey('schedule.id'))
    
    employees = db.relationship (
        'Employee',
        secondary = shift_employee_table,
        backref = db.backref('shifts')
        #lazy=dynamic
    )
    def __init__(self,title):
        self.title = title
    
    def __repr__(self):
        return "<Shift '{}'>".format(self.title)

class ShiftView(ModelView):
    column_list = ['title', 'schedule', 'employees']
    column_editable_list=['title']
    edit_modal=True
class EmployeeView(ModelView):
    column_list = ['username', 'shifts', 'email']
    column_editable_list=['username', 'email']
    edit_modal=True

admin.add_view(ShiftView(Shift, db.session))
admin.add_view(EmployeeView(Employee, db.session))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule')
def schedule():
    days_in_week = 7
    weekdays = []
    today = datetime.date.today()
    tdelta = datetime.timedelta(days=today.weekday())
    monday = today - tdelta

    for day in range(days_in_week):
        weekdays.append(monday + datetime.timedelta(days=day))
    return render_template('schedule.html', weekdays=weekdays)

if __name__ == "__main__":
    app.run(debug=True) 


# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()