import datetime
import calendar


def generate_calendar(year=datetime.datetime.now().year, month=datetime.datetime.now().month):
    if month > 12:
        year+=1
    month=month%12
    range_month=calendar.monthrange(month=month, year=year)
    first_week_day=range_month[0]
    range_days=[day for day in range(1,range_month[1]+1)]
    return (first_week_day, range_days, month, year)