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
    def __init__(self, data, n_quarters=2):
        self.state = defaultdict(int)

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

    def play(self):
        while True:

            try:
                self.vm.tick()

            except InputNeededException:
                self.handle_outputs()
                self.provide_series_of_inputs([
                    'NOT A J',
                    'NOT B T',
                    'AND D T',
                    'OR T J',
                    'NOT C T',
                    'AND D T',
                    'OR T J',
                    'WALK'
                ])

                continue

            except InterruptedError:
                self.handle_outputs()

                print('\nGAME OVER!')

                break


if __name__ == '__main__':
    with open(os.path.join('..', 'day_21_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))
    automat = Arcade(data, n_quarters=2)
    automat.play()

    # First part answer: 19358870
    # Second part answer:
