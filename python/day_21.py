import copy
import itertools
import json
import os
import time
from collections import defaultdict

from pynput import keyboard

try:
    from intcode import Intcode, OutputException, InputNeededException
    from utils import print_image, substract_pairs, sum_pairs
except ImportError:
    from python.intcode import Intcode, OutputException, InputNeededException
    from python.utils import print_image, substract_pairs, sum_pairs


class Arcade:
    def __init__(self, data, part=1):
        self.part = part

        self.vm = Intcode(data)

    def handle_outputs(self):
        output_buffer = ''
        for c in self.vm.unread_outputs:
            try:
                output_buffer += chr(c)
            except ValueError:
                output_buffer += '<%s>' % str(c)

        print(output_buffer)

    def provide_text_input(self, string):
        for c in string:
            self.vm.add_input(ord(c))

        self.vm.add_input(ord('\n'))

    def provide_series_of_inputs(self, commands_list):
        for command in commands_list:
            self.provide_text_input(command)

    def get_program(self, part):
        if part == 1:
            # Up to 4 next tiles visible, jumping over next three
            return [
                # In we're just before the hole - jump, no choice
                # @..
                # #.#
                'NOT A J',
                # Try to jump over two if there is ground after, because there can be hole outside of line of sight
                # @....|.
                # ##..#|.
                'NOT B T',
                'AND D T',
                'OR T J',
                # The other way around, jump over one if there is ground and possible holes outside of sight
                # @....|.
                # ###.#|..
                'NOT C T',
                'AND D T',
                'OR T J',
                'WALK'
            ]
        else:
            # Up to 9 next tiles visible
            return [
                'NOT A J',
                'NOT B T',
                'AND D T',
                'OR T J',
                'NOT C T',
                'AND D T',
                'AND H T',
                # The only addition to the Part one, to avoid the case when we can wait a bit
                # @............
                # ####.#.##.###
                #      ^ - landing here would be really bad
                #          ^ so we can check this tile it's good
                'OR T J',
                'RUN'
            ]

    def play(self):
        self.provide_series_of_inputs(self.get_program(self.part))
        while True:
            try:
                self.vm.tick()

            except InputNeededException:
                self.handle_outputs()
                # Should not happen really since we've already provided all the input
                continue

            except InterruptedError:
                self.handle_outputs()
                print('\nGAME OVER!')
                break


if __name__ == '__main__':
    with open(os.path.join('..', 'day_21_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))

    print('=============Part 1============')
    automat = Arcade(data, part=1)
    automat.play()

    print('=============Part 2============')
    automat = Arcade(data, part=2)
    automat.play()

    # First part answer: 19358870
    # Second part answer: 1143356492
