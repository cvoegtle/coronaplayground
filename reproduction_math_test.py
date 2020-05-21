import unittest
import pandas as pd
import datetime as dt
from reproduction_math import reproduction_rate
from reproduction_math import four_days_average


class ReproductionRateTestCase(unittest.TestCase):
    def test_total_calculation(self):
        data = self.provide_data()
        self.assertEqual(data['infections'][5] + data['reports'][5], data['total'][5])

    def test_average_calculation(self):
        data = self.provide_data()
        t = data['total']
        average = data['four_day_average']
        for i in range(3, len(average)):
            av = (t[i-3] + t[i-2] + t[i-1] + t[i])/4
            print(f'({t[i-3]} + {t[i-2]} + {t[i-1]} + {t[i]})/4 = {av} - {average[i]}')
            self.assertEqual(av, average[i])

    def test_r_calculation(self):
        data = self.provide_data()
        av = data['four_day_average']
        r = data['reproduction_rate']
        for i in range(7, len(av)):
            reproduction_rate = av[i] / av[i-4]
            print (f'{i}: {av[i]} / {av[i-4]} = {reproduction_rate} - {r[i]}')
            self.assertEqual(reproduction_rate, r[i])


    def provide_data(self):
        data = pd.read_csv("static/rki_latest.csv", header=0, names=["day", "infections", "reports"])
        data["day"] = [dt.datetime.strptime(d + ' 2020', "%b %d %Y") for d in data["day"]]
        data = data.assign(total=lambda x: x["infections"] + x["reports"])
        data = data.assign(four_day_average=[four_days_average(data['total'], index) for index in range(len(data['total']))])
        data = data.assign(reproduction_rate=[reproduction_rate(data['four_day_average'], index) for index in range(len(data['four_day_average']))])
        return data

if __name__ == '__main__':
    unittest.main()
