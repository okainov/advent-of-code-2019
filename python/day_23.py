import copy
import itertools
import json
import os
import time
from collections import defaultdict

import sys
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

        self.n = 50
        self.vms = []
        for i in range(self.n):
            current_vm = Intcode(data)
            current_vm.add_input(i)
            self.vms.append(current_vm)

    def play(self):
        while True:
            for vm in self.vms:
                try:
                    vm.tick()

                except InputNeededException:
                    while vm.unread_outputs:
                        address = vm.unread_outputs.pop(0)

                        x = vm.unread_outputs.pop(0)
                        y = vm.unread_outputs.pop(0)
                        if address == 255:
                            print(f'Finish, {x}, {y}')
                            sys.exit(0)
                        self.vms[address].add_input(x)
                        self.vms[address].add_input(y)

                    vm.add_input(-1)
                    continue

                except InterruptedError:
                    print('\nGAME OVER!')
                    break


if __name__ == '__main__':
    with open(os.path.join('..', 'day_23_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))

    print('=============Part 1============')
    automat = Arcade(data, part=1)
    automat.play()


    # First part answer: 23815
    # Second part answer:
