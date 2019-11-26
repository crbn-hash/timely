from flask import Flask, render_template
import datetime

app = Flask(__name__)

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