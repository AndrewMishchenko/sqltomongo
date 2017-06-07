import unittest

from sqltomongo.filters import (coma_filter,
                                project_filter,
                                unwind_filter,
                                order_filter,
                                order_filter_find
                                )


class TestFilters(unittest.TestCase):
    projection = ['restaurant_id,', 'address.coord.*']
    order_list = ['restaurant_id', 'desc,', 'borough', 'asc']

    def test_coma_filter(self):
        list_with_coma = ['select', 'restaurant_id,']
        list_without_coma = ['select', 'restaurant_id']
        self.assertEqual(coma_filter(list_with_coma), ['select', 'restaurant_id'])
        self.assertEqual(coma_filter(list_without_coma), list_without_coma)
        with self.assertRaises(ValueError):
            coma_filter({})

    def test_project_filter(self):
        result = {'address.coord': 1, 'restaurant_id,': 1}
        self.assertEqual(project_filter(self.projection), result)
        with self.assertRaises(ValueError):
            project_filter({})

    def test_unwind_filter(self):
        result = ['address.coord']
        self.assertEqual(unwind_filter(self.projection), result)
        with self.assertRaises(ValueError):
            unwind_filter({})

    def test_order_filter(self):
        result = {'$sort': {'borough': 1, 'restaurant_id': -1}}
        self.assertDictEqual(order_filter(self.order_list), result)
        with self.assertRaises(ValueError):
            unwind_filter({})

    def test_order_filter_find(self):
        result = [('restaurant_id', -1), ('borough', 1)]
        self.assertEqual(order_filter_find(self.order_list), result)
        with self.assertRaises(ValueError):
            order_filter_find({})


if __name__ == '__main__':
    unittest.main()
