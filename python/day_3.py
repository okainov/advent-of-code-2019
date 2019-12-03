import os


def sum_pairs(pair_1, pair_2):
    return (pair_1[0] + pair_2[0], pair_1[1] + pair_2[1])


def fill_grid(grid, wire):
    current_point = (0, 0)
    grid[current_point] = 1

    increment_table = {
        'U': (0, 1),
        'D': (0, -1),
        'R': (1, 0),
        'L': (-1, 0)
    }
    min_distance = None
    for sector in wire:
        length = int(sector[1:])
        direction = sector[0]
        for i in range(length):
            current_point = sum_pairs(current_point, increment_table[direction])
            if current_point in grid:
                current_distance = abs(current_point[0]) + abs(current_point[1])
                if min_distance is None or current_distance < min_distance:
                    min_distance = current_distance
            else:
                grid[current_point] = 1

    return min_distance


if __name__ == '__main__':
    result = 0
    grid = {}

    with open(os.path.join('..', 'day_3_input.txt'), 'r') as f:

        for line in f:
            wire = line.split(',')
            result = fill_grid(grid, wire)

    print(f'Part 1 answer: {result}')

    # First part answer:  3790689
    # Second part answer: 6533
