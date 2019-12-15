from unittest import TestCase
import os

from python.intcode import single_input_intcode


class TestIntcode(TestCase):
    def test_intcode_day_5_part_1(self):
        with open(os.path.join('..', 'day_5_input.txt'), 'r') as f:
            data = list(map(int, f.read().split(',')))

        outputs = single_input_intcode(data, 1)
        self.assertEquals(2845163, outputs[-1])

    def test_intcode_day_5_part_2(self):
        with open(os.path.join('..', 'day_5_input.txt'), 'r') as f:
            data = list(map(int, f.read().split(',')))

        outputs = single_input_intcode(data, 5)
        self.assertEquals(9436229, outputs[-1])

    def test_intcode_day_9_part_1(self):
        with open(os.path.join('..', 'day_9_input.txt'), 'r') as f:
            data = list(map(int, f.read().split(',')))

        outputs = single_input_intcode(data, 1)
        self.assertEquals(3742852857, outputs[-1])

    def test_intcode_day_9_part_2(self):
        with open(os.path.join('..', 'day_9_input.txt'), 'r') as f:
            data = list(map(int, f.read().split(',')))

        outputs = single_input_intcode(data, 2)
        self.assertEquals(73439, outputs[-1])
