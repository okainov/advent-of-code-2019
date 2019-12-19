import copy
import json
import os
from collections import defaultdict

from pynput import keyboard

try:
    from intcode import Intcode, OutputException, InputNeededException
    from utils import print_image, substract_pairs, sum_pairs
except ImportError:
    from python.intcode import Intcode, OutputException, InputNeededException
    from python.utils import print_image, substract_pairs, sum_pairs


class Arcade:
    def __init__(self, data, x, y):
        self.state = defaultdict(int)
        self.x = x
        self.y = y
        self.output_buffer = []

        self.vm = Intcode(data)

    def handle_outputs(self):
        self.output_buffer = self.vm.unread_outputs

    def play(self):
        while True:

            try:
                self.vm.tick()

            except InputNeededException:
                self.handle_outputs()

                self.vm.add_input([self.x, self.y])

                continue

            except InterruptedError:
                self.handle_outputs()

                # print('\nGAME OVER!')

                break


if __name__ == '__main__':
    with open(os.path.join('..', 'day_19_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))
    result = 0
    for x in range(50):
        for y in range(50):
            automat = Arcade(data, x, y)
            automat.play()
            print(automat.output_buffer)
            if automat.output_buffer[0] == 1:
                result += 1
    print(result)

    # First part answer:  206
    # Second part answer:
