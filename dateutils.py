#returns a list of date objects for all days of the current month
import datetime

def get_month_dates():
    dates_before = []
    dates_after = []
    dates_in_month = []
    today = datetime.date.today()
    daysbefore = today.day - 1
    while (daysbefore >= 1):
        tdelta = datetime.timedelta(days=daysbefore)
        dates_before.append(today - tdelta)
        daysbefore -= 1
    
    daysafter = 0
    while(today.month == (today+datetime.timedelta(days=daysafter)).month):
        tdelta = datetime.timedelta(days=daysafter)
        dates_after.append(today + tdelta)
        daysafter += 1
    dates_before.extend(dates_after)
    dates_in_month.extend(dates_before)
    #clean up this mongrel code
    return dates_in_month

def get_workmonth(today = datetime.date.today()):
    #clean this mongrel code. timedelta(weeks=1) is probably an option
    ww1 = get_workweek(today)
    ww2 = get_workweek(today+datetime.timedelta(days=7))
    ww3 = get_workweek(today+datetime.timedelta(days=14))
    ww4 = get_workweek(today+datetime.timedelta(days=21))
    workmonth = []
    workmonth.extend(ww1)
    workmonth.extend(ww2)
    workmonth.extend(ww3)
    workmonth.extend(ww4)
    return workmonth
    
def get_workweek(today = datetime.date.today()):

    days_in_week = 7
    weekdays = []
    tdelta = datetime.timedelta(days=today.weekday())
    monday = today - tdelta

    for day in range(days_in_week):
        weekdays.append(monday + datetime.timedelta(days=day))
    return weekdays

def number_to_name(date):
    #confirm that param is a valid date
    switch = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
        }
    return switch.get(date.weekday(), 'Error generating day name from given number')
