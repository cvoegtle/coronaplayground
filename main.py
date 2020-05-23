import io
import datetime as dt

from google.cloud import datastore

from flask import Flask, render_template, Markup, request
import pandas as pd

from reproduction_math import reproduction_rate
from reproduction_math import four_days_average
from rki_parser import RkiParser
from charts import infection_chart, reproduction_rate_chart

datastore_client = datastore.Client()

app = Flask(__name__)


@app.route('/')
def root():
    values = provide_latest()

    data = {
        'values': values,
        'last_date': last_date_readable(values)
    }
    corona_charts = {'infections': Markup(infection_chart(values)),
                     'reproduction_rate': Markup(reproduction_rate_chart(values))}
    return render_template('index.html', corona_charts=corona_charts, data=data)

@app.route('/upload', methods=("GET", "POST"))
def upload():
    if request.method == "POST":
        process(request.form["snippet"])

    values = provide_latest()

    data = {
        'last_date': last_date_readable(values)
    }
    return render_template('upload.html', data=data)

def process(snippet):
    parser = RkiParser(snippet)
    csv = parser.daily_cases_as_csv()
    save_latest(csv)

def provide_latest():
    csv = read_latest()
    data = pd.read_csv(io.StringIO(csv), header=0, names=["day", "infections", "reports"])
    data["day"] = [dt.datetime.strptime(d + ' 2020', "%b %d %Y") for d in data["day"]]
    data = data.assign(total=lambda x: x["infections"] + x["reports"])
    data = data.assign(four_day_average=[four_days_average(data['total'], index) for index in range(len(data['total']))])
    data = data.assign(reproduction_rate=[reproduction_rate(data['four_day_average'], index) for index in range(len(data['four_day_average']))])
    return data

def last_date_readable(data):
    last_date = data['day'][len(data['day']) - 1]
    return last_date.strftime("%d.%m.%y")

def save_latest(csv):
    with datastore_client.transaction():
        entity = datastore.Entity(key=datastore_client.key('corona'))
        entity.update({
            'timestamp': dt.datetime.now(),
            'csv': csv
        })

        datastore_client.put(entity)

def read_latest():
    query = datastore_client.query(kind='corona')
    query.order = ['-timestamp']

    corona_data = list(query.fetch(limit=1))

    return corona_data[0]['csv']


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
