from unittest import TestCase

from python.day_22 import simplify_operations, apply_operations


class TestSimplify_operations(TestCase):
    def test_simplify_operations(self):
        data = [
            ('reverse', None)
        ]
        self.assertEqual(simplify_operations(data, 10), data)

    def test_simplify_operations2(self):
        data = [
            ('increment', 3),
            ('cut', 2),
            ('increment', 5),
        ]

        expected_data = [
            ('increment', 1),
            ('cut', 3),
        ]

        self.assertEqual(expected_data, simplify_operations(data, 7))
        self.assertEqual(apply_operations(data, 7), apply_operations(simplify_operations(data, 7), 7))


    def test_simplify_operations3(self):
        data = [
            ('cut', 2),
            ('increment', 3),
            ('cut', 2),
        ]

        expected_data = [
            ('increment', 3),
            ('cut', 1),
        ]

        self.assertEqual(expected_data, simplify_operations(data, 7))
        self.assertEqual(apply_operations(data, 7), apply_operations(simplify_operations(data, 7), 7))