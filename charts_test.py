import unittest
import io

import altair as alt

from charts import infection_chart
from data_provider import provide_latest


class ChartTestCase(unittest.TestCase):
    def test_serialisation(self):
        data = provide_latest()
        chart = infection_chart(data)
        chart_as_html = io.StringIO()
        chart.save('test1.html', 'html')
        print(chart_as_html.getvalue())


if __name__ == '__main__':
    unittest.main()
