import os
from collections import defaultdict

from python.utils import sum_pairs, print_image


class Program:
    def __getitem__(self, item):
        try:
            return self.data[item]
        except IndexError:
            return self.additional_memory[item]

    def __setitem__(self, key, value):
        try:
            self.data[key] = value
        except IndexError:
            self.additional_memory[key] = value

    def __init__(self, data):
        self.data = data[::]
        self.additional_memory = defaultdict(int)


def get_param(data, index, mode, relative_base=0):
    if mode == '0':
        return data[index]
    elif mode == '1':
        return index
    elif mode == '2':
        return data[index] + relative_base
    pass


def solve_day_9(data):
    # Make explicit copy to do not mess with initial data
    data = Program(data)

    i = 0
    relative_base = 0
    while True:
        full_operation = f"{data[i]:05d}"

        operation = int(full_operation[-2:])
        params = full_operation[:-2]

        if operation == 99:
            break

        if operation == 1:
            # Add
            result_pos = get_param(data, i + 3, params[-3], relative_base)
            data[result_pos] = data[get_param(data, i + 1, params[-1], relative_base)] + \
                               data[get_param(data, i + 2, params[-2], relative_base)]
            i += 4
        elif operation == 2:
            # Multiply
            result_pos = get_param(data, i + 3, params[-3], relative_base)
            data[result_pos] = data[get_param(data, i + 1, params[-1], relative_base)] * \
                               data[get_param(data, i + 2, params[-2], relative_base)]
            i += 4
        elif operation == 3:
            # Input
            result_pos = get_param(data, i + 1, params[-1], relative_base)
            data[result_pos] = yield
            i += 2
        elif operation == 4:
            # Print
            result = data[get_param(data, i + 1, params[-1], relative_base)]
            yield result
            i += 2
        elif operation == 5:
            if data[get_param(data, i + 1, params[-1], relative_base)]:
                i = data[get_param(data, i + 2, params[-2], relative_base)]
            else:
                i += 3
        elif operation == 6:
            if data[get_param(data, i + 1, params[-1], relative_base)] == 0:
                i = data[get_param(data, i + 2, params[-2], relative_base)]
            else:
                i += 3
        elif operation == 7:
            # If less than
            if data[get_param(data, i + 1, params[-1], relative_base)] < \
                    data[get_param(data, i + 2, params[-2], relative_base)]:
                data[get_param(data, i + 3, params[-3], relative_base)] = 1
            else:
                data[get_param(data, i + 3, params[-3], relative_base)] = 0

            i += 4
        elif operation == 8:
            # if equal
            if data[get_param(data, i + 1, params[-1], relative_base)] == \
                    data[get_param(data, i + 2, params[-2], relative_base)]:
                data[get_param(data, i + 3, params[-3], relative_base)] = 1
            else:
                data[get_param(data, i + 3, params[-3], relative_base)] = 0
            i += 4
        elif operation == 9:
            # Increase relative base
            relative_base += data[get_param(data, i + 1, params[-1], relative_base)]
            i += 2

    return


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

    amplifier = solve_day_9(data)
    try:
        while True:
            next(amplifier)
            # Send the current color under robot
            current_color = amplifier.send(cells[current_position])
            turn_direction = next(amplifier)

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
