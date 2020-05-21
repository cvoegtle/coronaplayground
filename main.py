from flask import Flask, render_template, Markup

import data_provider as dp
from charts import infection_chart, reproduction_rate_chart

app = Flask(__name__)


@app.route('/')
def root():
    values = dp.provide_latest()

    data = {
        'values': values,
        'last_date': dp.last_date_readable(values)
    }
    corona_charts = {'infections': Markup(infection_chart(values)),
                     'reproduction_rate': Markup(reproduction_rate_chart(values))}
    return render_template('index.html', corona_charts=corona_charts, data=data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
