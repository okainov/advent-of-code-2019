import os
from collections import defaultdict

from python.intcode import intcode
from python.utils import sum_pairs, print_image


def color_robot(input_path='day_11_input.txt', starting_color=0):
    with open(os.path.join('..', input_path), 'r') as f:
        data = list(map(int, f.read().split(',')))

    current_position = (0, 0)
    cells = defaultdict(int)
    cells[current_position] = starting_color
    current_facing = 0

    facing = ['U', 'R', 'D', 'L']
    increment_table = {
        'U': (0, 1),
        'D': (0, -1),
        'R': (1, 0),
        'L': (-1, 0)
    }

    hull_paint_robot = intcode(data)
    try:
        while True:
            next(hull_paint_robot)
            # Send the current color under robot
            current_color = hull_paint_robot.send(cells[current_position])
            turn_direction = next(hull_paint_robot)

            # Paint current cell
            cells[current_position] = current_color

            # Turn the robot
            if turn_direction == 0:
                current_facing = (current_facing + 3) % 4
            else:
                current_facing = (current_facing + 1) % 4

            # Move the robot
            current_position = sum_pairs(current_position, increment_table[facing[current_facing]])
    except StopIteration:
        pass

    return cells


if __name__ == '__main__':
    cells_1 = color_robot()
    print('Part 1: %s' % len(cells_1))
    cells_2 = color_robot(starting_color=1)
    print_image(cells_2, reversed_y=True)
    # First part answer:  1932
    # Second part answer: EGHKGJER
