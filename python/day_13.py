import json
import os
from collections import defaultdict
from pynput import keyboard

try:
    from intcode import intcode
    from utils import print_image, substract_pairs, sum_pairs
except ImportError:
    from python.intcode import intcode
    from python.utils import print_image, substract_pairs, sum_pairs


def arcade(input_path='day_13_input.txt', n_quarters=1):
    with open(os.path.join('..', input_path), 'r') as f:
        data = list(map(int, f.read().split(',')))

    data[0] = n_quarters
    blocks = 0

    i = 0
    arcade_computer = intcode(data)
    state = defaultdict(int)
    with open('inputs.txt', 'r') as f:
        inputs = json.loads(f.read())
    # inputs.txt = []
    last_score = 0
    input_tick = 0
    ball_position = (19, 19)
    paddle_position = (21, 22)
    previous_ball_position = (18, 18)
    try:
        while True:
            i += 1

            action = next(arcade_computer)

            if action == 'I WANNA INPUT':
                # 1010 is the first tick asking for input
                if len(inputs) > input_tick:
                    # Restore sequence from save file
                    qq = inputs[input_tick]
                else:
                    # Print the system
                    os.system('cls')
                    print_image(state)
                    print('')
                    print(f'Tick {i}')
                    print('Walls: %s' % len([x for x in state if state[x] == 1]))
                    print('Blocks: %s' % len([x for x in state if state[x] == 2]))
                    print(f'Paddle: {paddle_position}')
                    print(f'Ball was at: {previous_ball_position}')
                    print(f'Ball at: {ball_position}')
                    print('Score: %s' % last_score)

                    # Try to autopilot
                    ball_velocity = substract_pairs(ball_position, previous_ball_position)
                    projected_next_ball_position = sum_pairs(ball_position, ball_velocity)
                    print(f'Velocity: {ball_velocity}')
                    print(f'Projected next position at: {projected_next_ball_position}')
                    if projected_next_ball_position[1] == 22:
                        print(f'DECIDE THE DIRECTION!')

                    automatic_input = 0
                    if ball_velocity[1] >= 0:
                        # Autopilot only if ball is falling down
                        while projected_next_ball_position[1] < 22:
                            projected_next_ball_position = sum_pairs(projected_next_ball_position, ball_velocity)

                        print(f'Projected final position at: {projected_next_ball_position}')
                        if projected_next_ball_position[0] > paddle_position[0]:
                            automatic_input = 1
                        elif projected_next_ball_position[0] < paddle_position[0]:
                            automatic_input = -1
                    else:
                        pass

                    print(f'Suggested autopilot: {automatic_input}')
                    # ASk for user input
                    print('Use left, right, <Space> for autopilot or any other key for nothing')
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
                        else:
                            qq = 0

                    inputs.append(int(qq))

                input_tick += 1
                next(arcade_computer)  # rewind to the input point
                arcade_computer.send(int(qq))
                continue
            else:
                x = action

            y = next(arcade_computer)
            tile_id = next(arcade_computer)
            if x == -1 and y == 0 and tile_id > last_score:
                last_score = tile_id
            else:
                state[(x, y)] = tile_id
                if tile_id == 4:
                    # Ball
                    previous_ball_position = ball_position
                    ball_position = (x, y)
                elif tile_id == 3:
                    # Paddle
                    paddle_position = (x, y)

            if tile_id == 2:
                blocks += 1

    except StopIteration:
        print('GAME OVER!')
        print('Score: %s' % last_score)

        print('Press any but ESC to save inputs')
        with keyboard.Events() as events:
            event = events.get(1000.0)
            if event is None:
                print('You did not press a key within one second')
            elif event.key == keyboard.Key.esc:
                pass
            else:
                with open('inputs.txt', 'w') as f:
                    f.write(json.dumps(inputs[:-3]))
                print('Saved')

    return blocks


if __name__ == '__main__':
    # cells_1 = arcade()
    # print('Part 1: %s' % cells_1)

    cells_1 = arcade(n_quarters=2)

    # First part answer:  258
    # Second part answer:
