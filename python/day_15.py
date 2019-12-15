import os
from collections import defaultdict

try:
    from intcode import intcode
    from utils import print_image, substract_pairs, sum_pairs
except ImportError:
    from python.intcode import intcode
    from python.utils import print_image, substract_pairs, sum_pairs


def all_neightbors_visited(states, current_position):
    return sum_pairs(current_position, (1, 0)) in states \
           and sum_pairs(current_position, (-1, 0)) in states \
           and sum_pairs(current_position, (0, 1)) in states \
           and sum_pairs(current_position, (0, -1)) in states


def arcade(input_path='day_15_input.txt', n_quarters=1):
    with open(os.path.join('..', input_path), 'r') as f:
        data = list(map(int, f.read().split(',')))

    i = 0
    arcade_computer = intcode(data)
    state = dict()
    current_position = (0, 0)
    state[current_position] = 0
    next_direction_from_cell_map = defaultdict(int)
    directions_priority = [4, 1, 3, 2]
    increment_table = {
        1: (0, 1),
        2: (0, -1),
        4: (1, 0),
        3: (-1, 0)
    }

    try:
        while True:
            i += 1

            input_prompt = next(arcade_computer)
            assert input_prompt == 'I WANNA INPUT'

            next(arcade_computer)  # rewind to the input point

            # Select next direction using right-hand rule
            visited_ok = False
            if all_neightbors_visited(state, current_position):
                visited_ok = True

            direction_index = next_direction_from_cell_map[current_position]

            if visited_ok:
                # Get back to visted non-wall cell
                while sum_pairs(current_position, increment_table[directions_priority[direction_index]]) in state and \
                        state[sum_pairs(current_position, increment_table[directions_priority[direction_index]])] < 0:
                    direction_index = (1 + direction_index) % 4
            else:
                while sum_pairs(current_position, increment_table[directions_priority[direction_index]]) in state:
                    direction_index = (1 + direction_index) % 4
            direction = directions_priority[direction_index]
            next_direction_from_cell_map[current_position] = (direction_index + 1) % 4

            arcade_computer.send(direction)
            result = next(arcade_computer)

            if result == 1:
                old_distance = state[current_position]
                current_position = sum_pairs(current_position, increment_table[direction])
                if current_position not in state:
                    state[current_position] = old_distance + 1
                else:
                    state[current_position] = min(old_distance + 1, state[current_position])

            elif result == 2:
                old_distance = state[current_position]
                current_position = sum_pairs(current_position, increment_table[direction])
                if current_position not in state:
                    state[current_position] = old_distance + 1
                else:
                    state[current_position] = min(old_distance + 1, state[current_position])
                # Yahoo, found exit... need to count?
                print(state[current_position])
                break

            elif result == 0:
                state[sum_pairs(current_position, increment_table[direction])] = -1

    except StopIteration:
        print('GAME OVER!')

    return 1


if __name__ == '__main__':
    # cells_1 = arcade()
    # print('Part 1: %s' % cells_1)

    cells_1 = arcade(n_quarters=2)

    # First part answer:  258
    # Second part answer:
