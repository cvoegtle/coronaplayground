import unittest
from rki_parser import RkiParser

class RkiParserTestCase(unittest.TestCase):
    def test_parse_october(self):
        parser = RkiParser(read_svg_data())
        daily_cases = parser.daily_cases_as_csv()
        self.assertEqual(3750, len(daily_cases))


def read_svg_data():
    with open('test_data/raw_corona_chart.svg') as input_svg_file:
        return input_svg_file.read()

if __name__ == '__main__':
    unittest.main()
