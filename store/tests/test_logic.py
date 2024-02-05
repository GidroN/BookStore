from django.test import TestCase
from store.logic import operations


class LogicTestCase(TestCase):
    def test_plus(self):
        """ Test plus """
        a, b, c = 4, 6, '+'
        result = operations(a, b, c)
        self.assertEqual(result, 10)

    def test_minus(self):
        """ Test minus """
        a, b, c = 6, 2, '-'
        result = operations(a, b, c)
        self.assertEqual(result, 4)
    
    def test_multiply(self):
        """ Test multiply """
        a, b, c = 5, 6, '*'
        result = operations(a, b, c)
        self.assertEqual(result, 30)

    def test_something_other(self):
        self.assertEqual(True, True)