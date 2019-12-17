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
            if i > 200:
                # Assuming it's a final score
                print(f'Part 2 final score: {i}')
                continue
            if i == 10:
                # Newline
                y += 1
                x = 0
                continue
            self.state[(x, y)] = chr(i)
            x += 1

    def provide_text_input(self, string):
        for c in string:
            self.vm.add_input(ord(c))

        self.vm.add_input(ord('\n'))

    def play(self):
        while True:

            try:
                self.vm.tick()

            except InputNeededException:
                os.system('cls')
                print('')
                self.handle_outputs()

                print_image(self.state, interpret_as_ascii=True)

                # Full R6 L10 R8 R8 R12 L8 L10 R6 L10 R8 R8 R12 L10 R6 L10 R12 L8 L10 R12 L10 R6 L10 R6 L10 R8 R8 R12 L8 L10 R6 L10 R8 R8 R12 L10 R6 L10
                # Just remap the values:
                # D E F F G K E D E F F G E D E G K E G E D E D E F F G K E D E F F G E D E

                # D = R6
                # E = L10
                # F = R8
                # G = R12
                # K = L8

                # D E F F | G K E | D E F F | G E D E | G K E | G E D E | D E F F | G K E | D E F F | G E D E
                # =>
                # A = GKE = R12 L8 L10
                # B = DEFF = R6 L10 R8 R8
                # C = GEDE = R12 L10 R6 L10

                self.provide_text_input('B,A,B,C,A,C,B,A,B,C')
                self.provide_text_input('R,12,L,8,L,10')
                self.provide_text_input('R,6,L,10,R,8,R,8')
                self.provide_text_input('R,12,L,10,R,6,L,10')
                self.provide_text_input('n')
                continue

            except InterruptedError:
                os.system('cls')
                print('')
                self.handle_outputs()
                print_image(self.state, interpret_as_ascii=True)

                print('\nGAME OVER!')

                break


if __name__ == '__main__':
    with open(os.path.join('..', 'day_17_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))
    automat = Arcade(data, n_quarters=2)
    automat.play()

    # First part answer:  8408
    # Second part answer: 1168948
