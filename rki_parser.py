from bs4 import BeautifulSoup
import sys


class RkiParser:

    def __init__(self, snippet):
        self.soup = BeautifulSoup(snippet, 'html.parser')

    def extract_daily_cases(self):
        chart_elements = self.soup.find_all('g', attrs={"aria-label": lambda AL: AL and AL.startswith("Erkrankungsdatum")})
        chart_data = [split('infections', element['aria-label']) for element in chart_elements]

        chart_elements = self.soup.find_all('g', attrs={"aria-label": lambda AL: AL and AL.startswith("Meldedatum")})
        for element in chart_elements:
            reports = split('reports', element['aria-label'])
            dataset = find(reports['date'], chart_data)
            if dataset:
                dataset['reports'] = reports['reports']
            else:
                chart_data.append(reports)

        return chart_data

    def daily_cases_as_csv(self):
        csv = 'date, infections, reports\n'
        daily_cases = self.extract_daily_cases()
        for case in daily_cases:
            csv += case['date'] + ', ' + case.get('infections', '0') + ', ' + case.get('reports', '0') + '\n'
        return csv


def split(identifier, label):
    part = label.split()
    return {
        'date': english_date(part[1] + ' ' + part[2][:-1]),
        identifier: plain_number(part[4])
    }


def english_date(date):
    return date.replace('Mär', 'Mar').replace('Mai', 'May')


def plain_number(value):
    return value.replace(',', '')


def find(date, chart_data):
    for chart_ds in chart_data:
        if chart_ds['date'] == date:
            return chart_ds
    return None


def write(daily_cases):
    print('date, infections, reports')
    for case in daily_cases:
        print(case['date'] + ', ' + case.get('infections', '0') + ', ' + case.get('reports', '0'))


if __name__ == '__main__':
    daily_cases = RkiParser(sys.argv[1]).extract_daily_cases()
    write(daily_cases)
