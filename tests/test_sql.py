import unittest

from sqltomongo.sql import Checker


class TestSql(unittest.TestCase):
    def test_spliter(self):
        string = "select restaurant_id " \
                 "from restaurants " \
                 "where restaurant_id < '50018982' " \
                 "and grades.grade = 'A' " \
                 "ORDER by restaurant_id asc " \
                 "skip 5"
        list_string = []
        self.assertEqual(Checker.spliter(string), ['select', 'restaurant_id',
                                                   'from', 'restaurants', 'where',
                                                   'restaurant_id', '<', "'50018982'",
                                                   'and', 'grades.grade', '=', "'A'",
                                                   'ORDER', 'by', 'restaurant_id', 'asc',
                                                   'skip', '5'
                                                   ]
                         )
        with self.assertRaises(ValueError):
            Checker.spliter(list_string)



if __name__ == '__main__':
    unittest.main()
