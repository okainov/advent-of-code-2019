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
    def __init__(self, data, n_quarters=2):
        self.state = defaultdict(int)

        data[0] = n_quarters

        self.vm = Intcode(data)

    def handle_outputs(self):
        output_buffer = self.vm.unread_outputs
        x = 0
        y = 0
        for i in output_buffer:
            if i == 35:
                # Scaffold
                self.state[(x, y)] = 1
                x += 1
            elif i == 46:
                self.state[(x, y)] = '.'
                x += 1
            elif i == 10:
                # Newline
                y += 1
                x = 0
            else:
                x += 1

    def play(self):
        while True:

            try:
                self.vm.tick()

            except InputNeededException:

                print_image(self.state)

                self.handle_outputs()
                # self.vm.add_input(int(input_value))
                continue

            except InterruptedError:
                self.handle_outputs()
                print_image(self.state)

                result = 0
                states_copy = copy.deepcopy(self.state)
                for coord in states_copy:
                    if self.state[coord] == 1 and self.state[sum_pairs(coord, (0, 1))] == 1 and \
                            self.state[sum_pairs(coord, (0, -1))] == 1 and \
                            self.state[sum_pairs(coord, (1, 0))] == 1 and \
                            self.state[sum_pairs(coord, (-1, 0))] == 1:
                        result += coord[0] * coord[1]
                        print(coord[0] * coord[1])
                print(f'Part 1: {result}')

                print('GAME OVER!')

                break


if __name__ == '__main__':
    with open(os.path.join('..', 'day_17_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))
    automat = Arcade(data, n_quarters=1)
    automat.play()

    # First part answer:  8408
    # Second part answer: 12765
