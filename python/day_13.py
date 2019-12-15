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
        self.draw_progress = False
        # Stop for input to give human chance to play himself =)
        self.wait_for_input = False

        data[0] = n_quarters

        self.vm = Intcode(data)

        self.global_states_stack = []
        self.input_tick = 0
        self.hit_tick = None
        self.hit_position = None

        self.ball_position = (19, 19)
        self.paddle_position = (21, 22)
        self.previous_ball_position = (18, 18)
        self.score = 0
        with open('inputs.txt', 'r') as f:
            self.save_file = json.loads(f.read())

    def handle_outputs(self):
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

    def predict_ball_position_simple(self):
        """
        Find out where to move the paddle by using only current and previous ball positions:
        - Try to move the paddle to the same position as the ball would be (according to our prediction)

        Unfortunately, this strategy doesn't work all the time, sometimes it breaks after quick ball's change direction
        Minimal initial guidance required is:
        [1, 0, -1, 0, 0, 1, 1, 1]
        """
        ball_velocity = substract_pairs(self.ball_position, self.previous_ball_position)
        projected_next_ball_position = sum_pairs(self.ball_position, ball_velocity)
        if self.draw_progress:
            print(f'Velocity: {ball_velocity}')
            print(f'Projected next position at: {projected_next_ball_position}')
            if projected_next_ball_position[1] == 22:
                print(f'DECIDE THE DIRECTION!')

        automatic_input = 0
        if ball_velocity[1] > 0:
            # Autopilot only if ball is falling down
            while projected_next_ball_position[1] < 22:
                projected_next_ball_position = sum_pairs(projected_next_ball_position, ball_velocity)
        else:
            pass

        if self.draw_progress:
            print(f'Projected final position at: {projected_next_ball_position}')
        if projected_next_ball_position[0] > self.paddle_position[0]:
            automatic_input = 1
        elif projected_next_ball_position[0] < self.paddle_position[0]:
            automatic_input = -1
        return automatic_input

    def predict_ball_position_stupid_simple(self):
        """
        Just use the sign, nothing more, people say it works...
        """
        ball_x = self.ball_position[0]
        paddle_x = self.paddle_position[0]

        automatic_input = 0
        if ball_x > paddle_x:
            automatic_input = 1
        elif ball_x < paddle_x:
            automatic_input = -1
        return automatic_input

    def predict_ball_position_emulation(self):
        """
        Find out where to move the paddle by modelling the whole game to find the position of the ball
        :return: direction where to move the paddle
        """
        if self.hit_position is None or self.vm.ticks >= self.hit_tick:
            # Emulate the flow only if it's time =)
            emulator = copy.deepcopy(self)

            while True:
                try:
                    emulator.vm.tick()
                except InputNeededException:
                    emulator.handle_outputs()
                    if emulator.ball_position[1] == 21:
                        # Ball reached the line before the paddle, we can remember its position
                        break
                    emulator.vm.add_input(0)
                except InterruptedError:
                    # Nothing to predict, game will be finished
                    return 0
            self.hit_tick = emulator.vm.ticks
            self.hit_position = emulator.ball_position

        automatic_input = 0
        if self.draw_progress:
            print(f'Projected final position at: {self.hit_position}')
        if self.hit_position[0] > self.paddle_position[0]:
            automatic_input = 1
        elif self.hit_position[0] < self.paddle_position[0]:
            automatic_input = -1
        return automatic_input

    def play(self):
        while True:

            try:
                self.vm.tick()

            except InputNeededException:
                self.handle_outputs()

                if len(self.save_file) > self.input_tick:
                    # Restore&replay the sequence from save file
                    input_value = self.save_file[self.input_tick]
                else:
                    if self.draw_progress:
                        # Print the system
                        os.system('cls')
                        print_image(self.state)
                        print('')
                        print(f'VM tick {self.vm.ticks}')
                        print('Blocks: %s' % len([x for x in self.state if self.state[x] == 2]))
                        print(f'Paddle: {self.paddle_position}')
                        print(f'Ball was at: {self.previous_ball_position}')
                        print(f'Ball at: {self.ball_position}')
                        print('Score: %s' % self.score)

                    # automatic_input = self.predict_ball_position_simple()
                    # automatic_input = self.predict_ball_position_emulation()
                    automatic_input = self.predict_ball_position_stupid_simple()

                    if self.draw_progress:
                        print(f'Suggested autopilot: {automatic_input}')

                    if self.wait_for_input:
                        # ASk for user input
                        print('Use left, right, <Space> for autopilot or any other key for nothing')
                        with keyboard.Events() as events:
                            event = events.get(1000.0)
                            if event is None:
                                print('You did not press a key within one second')
                                input_value = 0
                            elif event.key == keyboard.Key.left:
                                input_value = -1
                            elif event.key == keyboard.Key.right:
                                input_value = 1
                            elif event.key == keyboard.Key.space:
                                input_value = automatic_input
                            else:
                                input_value = 0
                    else:
                        input_value = automatic_input
                    self.save_file.append(int(input_value))

                self.input_tick += 1
                self.vm.add_input(int(input_value))
                continue

            except InterruptedError:
                self.handle_outputs()
                print('GAME OVER!')
                print('Blocks: %s' % len([x for x in self.state if self.state[x] == 2]))
                print('Score: %s' % self.score)

                potential_save = self.save_file[:-3]
                if potential_save:
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
    with open(os.path.join('..', 'day_13_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))
    automat = Arcade(data, n_quarters=2)
    automat.play()

    # First part answer:  258
    # Second part answer: 12765
