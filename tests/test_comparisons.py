import unittest

from sqltomongo.comparisons import comparison_converter
from sqltomongo.exceptions import SqmongoComparisonError


class TestComparisons(unittest.TestCase):
    def test_comparison_converter(self):
        self.assertEqual(comparison_converter('='), '==')
        self.assertEqual(comparison_converter('<>'), '!=')
        self.assertEqual(comparison_converter('>'), '>')
        self.assertEqual(comparison_converter('>='), '>=')
        self.assertEqual(comparison_converter('<'), '<')
        self.assertEqual(comparison_converter('<='), '<=')
        with self.assertRaises(SqmongoComparisonError):
            comparison_converter('')
        with self.assertRaises(SqmongoComparisonError):
            comparison_converter(' ')
        with self.assertRaises(SqmongoComparisonError):
            comparison_converter('bla-bla-bla')


if __name__ == '__main__':
    unittest.main()
