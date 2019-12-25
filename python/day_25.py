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
        output_buffer = [chr(x) for x in self.vm.unread_outputs]
        print(''.join(output_buffer))

    def provide_text_input(self, string):
        for c in string:
            self.vm.add_input(ord(c))

        self.vm.add_input(ord('\n'))

    def provide_series_of_inputs(self, commands_list):
        for command in commands_list:
            self.provide_text_input(command)

    def play(self):

        take_coin = ['north', 'east', 'take coin', 'west', 'south']
        take_rest = ['south', 'take food ration', 'west', 'take sand', 'north', 'north', 'east', 'take astrolabe',
                     'west', 'south', 'south', 'east', 'north']
        walk_to_check = ['east', 'east', 'east']
        take_south = ['east', 'take cake', 'south', 'take weather machine', 'west', 'take ornament', 'west', 'take jam',
                      'east', 'east', 'north']

        items = ['astrolabe',
                 'coin', 'cake', 'sand',
                 'food ration', 'ornament', 'jam', 'weather machine']
        drop_all = [f'drop {x}' for x in items]
        items = ['astrolabe',
                 # 'coin', 'cake', 'sand',
                 'food ration', 'ornament', 'jam', 'weather machine']
        self.provide_series_of_inputs(take_coin)
        self.provide_series_of_inputs(take_rest)
        self.provide_series_of_inputs(take_south)
        self.provide_series_of_inputs(walk_to_check)
        self.permutations = []
        for x in range(1, len(items) + 1):
            self.permutations.extend(list(itertools.combinations(items, x)))
            # for combo in itertools.combinations(items, x):
            #     self.permutations.extend(list(itertools.permutations(combo)))
        # self.permutations = list(itertools.permutations(['sand', 'astrolabe', 'food ration']))
        index = 0

        while True:

            try:
                self.vm.tick()

            except InputNeededException:
                self.handle_outputs()

                print('Use arrows, <Space> for autopilot or any other key for nothing')
                input_value = None
                with keyboard.Events() as events:
                    event = events.get(1000.0)
                    if event is None:
                        print('You did not press a key within one second')
                        input_value = 0
                    elif event.key == keyboard.Key.left:
                        input_value = "west"
                    elif event.key == keyboard.Key.right:
                        input_value = "east"
                    elif event.key == keyboard.Key.up:
                        input_value = "north"
                    elif event.key == keyboard.Key.down:
                        input_value = "south"
                    elif event.key == keyboard.Key.tab:
                        input_value = "inv"
                    elif event.key == keyboard.Key.caps_lock:
                        print('=' * 80)
                        print('Trying %s: %s' % (index, str(self.permutations[index])))
                        print('=' * 80)
                        self.provide_series_of_inputs(drop_all)
                        self.provide_series_of_inputs([f'take {x}' for x in self.permutations[index]])
                        self.provide_text_input('south')
                        index += 1
                        input_value = None
                    elif event.key == keyboard.Key.space:
                        item = input("Which item to take?")
                        input_value = f"take {item}".replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
                        print(f'Executing <{input_value}>')
                    elif event.key == keyboard.Key.backspace:
                        item = input("Which item to drop?")
                        input_value = f"drop {item}".replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
                        print(f'Executing <{input_value}>')
                    else:
                        print('Unknown command')

                if input_value is not None:
                    self.provide_text_input(input_value)
                time.sleep(0.2)
                continue

            except InterruptedError:
                self.handle_outputs()

                print('\nGAME OVER!')

                break


if __name__ == '__main__':
    with open(os.path.join('..', 'day_25_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))
    automat = Arcade(data, n_quarters=2)
    automat.play()

    # First part answer: 4206594 ('astrolabe', 'food ration', 'ornament', 'weather machine')
    # Second part answer: 1168948
