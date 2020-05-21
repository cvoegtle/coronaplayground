import datetime as dt
import pandas as pd

from reproduction_math import reproduction_rate
from reproduction_math import four_days_average

def provide_latest():
    data = pd.read_csv("static/rki_latest.csv", header=0, names=["day", "infections", "reports"])
    data["day"] = [dt.datetime.strptime(d + ' 2020', "%b %d %Y") for d in data["day"]]
    data = data.assign(total=lambda x: x["infections"] + x["reports"])
    data = data.assign(four_day_average=[four_days_average(data['total'], index) for index in range(len(data['total']))])
    data = data.assign(reproduction_rate=[reproduction_rate(data['four_day_average'], index) for index in range(len(data['four_day_average']))])
    return data

def last_date_readable(data):
    last_date = data['day'][len(data['day']) - 1]
    return last_date.strftime("%d.%m.%y")