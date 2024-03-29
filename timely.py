from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
import datetime
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
import dateutils


app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
admin = Admin(app)



shift_employee_table = db.Table('shift-employees', db.Column('shift_id',db.Integer(), db.ForeignKey('shift.id')), db.Column('employee_id',db.Integer(), db.ForeignKey('employee.id')))
schedule_shift_table = db.Table('schedule-shifts', db.Column('schedule_id', db.Integer(), db.ForeignKey('schedule.id')), db.Column('shift_id', db.Integer(), db.ForeignKey('shift.id')))
class WorkWeek(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80))
    workdays = db.relationship(
        'WorkDay',
        backref='workweek'
        #lazy='dynamic'
    )
    def __init__(self,title):
        self.title = title
    def __repr__(self):
        return "<WorkWeek '{}'>".format(self.title)
    

class WorkDay(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    date = db.Column(db.Date())

    def __init__(self,title):
        self.title = title
    def __repr__(self):
        return "<WorkWeek '{}', '{}'>".format(self.title, self.date)
class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True)#notnull
    password = db.Column(db.String(255))#notnull
    email = db.Column(db.String(255))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return ">{}".format(self.username)

class Schedule(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80))
    #__tablename__ = 'Schedule'
    shifts = db.relationship(
        'Shift',
        secondary=schedule_shift_table,
        backref= db.backref('schedules')
        #lazy='dynamic'
    )

    def __init__(self,title):
        self.title = title
    
    def __repr__(self):
        return "<Schedule '{}'>".format(self.title)

class Shift(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))#notnull
    start_dt = db.Column(db.Time())#notnull
    end_dt = db.Column(db.Time())#notnull
    #sqlite3 may not enforce this constraint - check to make sure prod db does
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

class ScheduleView(ModelView):
    column_list =['title', 'shifts']
    column_editable_list=['title', 'shifts']
    edit_modal=True
class ShiftView(ModelView):
    column_list = ['title','schedules','start_dt', 'end_dt', 'employees']
    column_editable_list=['title', 'start_dt', 'end_dt', 'employees', 'schedules']
    edit_modal=True
class EmployeeView(ModelView):
    column_list = ['username', 'shifts', 'email']
    column_editable_list=['username', 'email', 'shifts']
    edit_modal=True

admin.add_view(ScheduleView(Schedule, db.session))
admin.add_view(ShiftView(Shift, db.session))
admin.add_view(EmployeeView(Employee, db.session))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/schedule')
def schedule2():
    WEEKS_IN_MONTH = 4
    month = dateutils.get_workweeks(WEEKS_IN_MONTH)
    shifts = Shift.query.all()
    today = datetime.date.today()
    return (render_template('schedule.html',shifts=shifts,month=month, weekdays=month[0], today=today   ))

#which schedule
#change back to filter - is this a jinja error because of query object?
#a gill for forgetting that the URL param must be passed to the route function
#as a parameter, otherwise it cannot be used inside the function
#expand to return full schedule object. instead of generating schedule by fitting 
#it into html via Jinja2, send it as JSON and let javascript do the formatting(alternative)
@app.route('/schedule/<title>')
def schedule(title):
    sched = Schedule.query.filter_by(title=title).first()
    return (render_template('schedule2.html', schedule=sched))

if __name__ == "__main__":
    app.run(debug=True) 
# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()