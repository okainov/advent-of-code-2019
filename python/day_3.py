import os


def sum_pairs(pair_1, pair_2):
    return (pair_1[0] + pair_2[0], pair_1[1] + pair_2[1])


def fill_grid(grid, wire, first_wire=True):
    current_point = (0, 0)
    grid[current_point] = 0

    increment_table = {
        'U': (0, 1),
        'D': (0, -1),
        'R': (1, 0),
        'L': (-1, 0)
    }
    min_distance = None
    step = 0
    for sector in wire:
        length = int(sector[1:])
        direction = sector[0]
        for i in range(length):
            current_point = sum_pairs(current_point, increment_table[direction])
            step += 1
            if not first_wire and current_point in grid:
                # Check the second wire
                current_distance = grid[current_point] + step
                if min_distance is None or current_distance < min_distance:
                    min_distance = current_distance
            elif first_wire:
                # Fill the table only for the first wire
                grid[current_point] = step

    return min_distance


if __name__ == '__main__':
    result = 0
    grid = {}

    with open(os.path.join('..', 'day_3_input.txt'), 'r') as f:

        first_wire = True
        for line in f:
            wire = line.split(',')
            result = fill_grid(grid, wire, first_wire)
            first_wire = False

    print(f'Part 2 answer: {result}')

    # First part answer:  1431
    # Second part answer: 48012
