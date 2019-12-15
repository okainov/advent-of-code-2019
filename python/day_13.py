import copy
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

        data[0] = n_quarters

        self.vm = Intcode(data)

        self.global_states_stack = []
        self.i = 0
        self.input_tick = 0

        self.ball_position = (19, 19)
        self.paddle_position = (21, 22)
        self.previous_ball_position = (18, 18)
        self.score = 0
        with open('inputs.txt', 'r') as f:
            self.save_file = json.loads(f.read())

    def play(self):
        while True:
            self.i += 1

            try:
                self.vm.tick()


            except InputNeededException:
                output_buffer = self.vm.unread_outputs
                # Handle state refresh
                while output_buffer:
                    x = output_buffer.pop(0)
                    y = output_buffer.pop(0)
                    tile_id = output_buffer.pop(0)

                    if x == -1 and y == 0 and tile_id > self.score:
                        self.score = tile_id
                    else:
                        self.state[(x, y)] = tile_id
                        if tile_id == 4:
                            # Ball
                            self.previous_ball_position = self.ball_position
                            self.ball_position = (x, y)
                        elif tile_id == 3:
                            # Paddle
                            self.paddle_position = (x, y)

                # 1010 is the first tick asking for input
                if len(self.save_file) > self.input_tick:
                    # Restore sequence from save file
                    qq = self.save_file[self.input_tick]
                else:
                    # Print the system
                    os.system('cls')
                    print_image(self.state)
                    print('')
                    print(f'Tick {self.i}')
                    print(f'VM tick {self.vm.ticks}')
                    print('Walls: %s' % len([x for x in self.state if self.state[x] == 1]))
                    print('Blocks: %s' % len([x for x in self.state if self.state[x] == 2]))
                    print(f'Paddle: {self.paddle_position}')
                    print(f'Ball was at: {self.previous_ball_position}')
                    print(f'Ball at: {self.ball_position}')
                    print('Score: %s' % self.score)

                    # Try to autopilot
                    self.ball_velocity = substract_pairs(self.ball_position, self.previous_ball_position)
                    self.projected_next_ball_position = sum_pairs(self.ball_position, self.ball_velocity)
                    print(f'Velocity: {self.ball_velocity}')
                    print(f'Projected next position at: {self.projected_next_ball_position}')
                    if self.projected_next_ball_position[1] == 22:
                        print(f'DECIDE THE DIRECTION!')

                    automatic_input = 0
                    if self.ball_velocity[1] > 0:
                        # Autopilot only if ball is falling down
                        while self.projected_next_ball_position[1] < 22:
                            self.projected_next_ball_position = sum_pairs(self.projected_next_ball_position,
                                                                          self.ball_velocity)
                    else:
                        pass

                    print(f'Projected final position at: {self.projected_next_ball_position}')
                    if self.projected_next_ball_position[0] > self.paddle_position[0]:
                        automatic_input = 1
                    elif self.projected_next_ball_position[0] < self.paddle_position[0]:
                        automatic_input = -1

                    print(f'Suggested autopilot: {automatic_input}')
                    # ASk for user input
                    print(
                        'Use left, right, <Space> for autopilot, backspace to go back in time or any other key for nothing')
                    with keyboard.Events() as events:
                        event = events.get(1000.0)
                        if event is None:
                            print('You did not press a key within one second')
                            qq = 0
                        elif event.key == keyboard.Key.left:
                            qq = -1
                        elif event.key == keyboard.Key.right:
                            qq = 1
                        elif event.key == keyboard.Key.space:
                            qq = automatic_input
                        elif event.key == keyboard.Key.backspace:
                            # Go backwards in time
                            self.global_states_stack.pop()
                            self.global_states_stack.pop()
                            self.global_states_stack.pop()
                            state_to_restore = self.global_states_stack.pop()
                            self.state = state_to_restore['state']
                            self.score = state_to_restore['score']
                            self.save_file = state_to_restore['save_file']
                            self.paddle_position = state_to_restore['paddle_position']
                            self.ball_position = state_to_restore['ball_position']
                            self.previous_ball_position = state_to_restore['previous_ball_position']
                            self.vm = state_to_restore['vm']
                            self.input_tick = state_to_restore['input_tick']
                            self.i = state_to_restore['i']
                            continue
                        else:
                            qq = 0

                    self.save_file.append(int(qq))

                self.input_tick += 1
                self.vm.add_input(int(qq))

                # Find out input
                self.global_states_stack.append({
                    'vm': copy.deepcopy(self.vm),
                    'state': copy.deepcopy(self.state),
                    'save_file': copy.deepcopy(self.save_file),
                    'score': self.score,
                    'ball_position': self.ball_position,
                    'paddle_position': self.paddle_position,
                    'previous_ball_position': self.previous_ball_position,
                    'input_tick': self.input_tick,
                    'i': self.i
                })
                continue

            except InterruptedError:
                print('GAME OVER!')
                print('Score: %s' % self.score)

                print('Press any but ESC to save inputs')
                with keyboard.Events() as events:
                    event = events.get(1000.0)
                    if event is None:
                        print('You did not press a key within one second')
                    elif event.key == keyboard.Key.esc:
                        pass
                    else:
                        with open('inputs.txt', 'w') as f:
                            f.write(json.dumps(self.save_file[:-3]))
                        print('Saved')

                break


if __name__ == '__main__':
    # cells_1 = arcade()
    # print('Part 1: %s' % cells_1)

    with open(os.path.join('..', 'day_13_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))
    automat = Arcade(data, n_quarters=2)
    automat.play()

    # First part answer:  258
    # Second part answer:
