import unittest

from sqltomongo.sql import Checker


class TestSql(unittest.TestCase):
    string = "select restaurant_id " \
             "from restaurants " \
             "where restaurant_id < '50018982' " \
             "and grades.grade = 'A' " \
             "ORDER by restaurant_id asc " \
             "skip 5"

    splited_string = ['select', 'restaurant_id',
                      'from', 'restaurants', 'where',
                      'restaurant_id', '<', "'50018982'",
                      'and', 'grades.grade', '=', "'A'",
                      'ORDER', 'by', 'restaurant_id', 'asc',
                      'skip', '5'
                      ]
    parsed_string = {'SELECT': ['restaurant_id'],
                     'WHERE': ['restaurant_id', '<', "'50018982'", 'and',
                               'grades.grade', '==', "'A'"],
                     'FROM': ['restaurants'],
                     'SKIP': ['5'], 'ORDER': ['restaurant_id', 'asc']
                     }

    def test_spliter(self):
        list_string = []
        self.assertEqual(Checker.spliter(self.string), self.splited_string)
        with self.assertRaises(ValueError):
            Checker.spliter(list_string)

    def test_parse(self):
        epmty_string = {}
        self.assertDictEqual(Checker(self.string).parse(), self.parsed_string)
        with self.assertRaises(ValueError):
            Checker(epmty_string).parse()

    def test_parse_first(self):
        self.assertEqual(Checker.parse_first(self.parsed_string), 'SELECT')
        with self.assertRaises(ValueError):
            Checker.parse_first('')

    def test_parse_select(self):
        self.assertDictEqual(Checker.parse_select(self.splited_string), self.parsed_string)


if __name__ == '__main__':
    unittest.main()
