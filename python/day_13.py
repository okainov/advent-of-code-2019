import os

from python.intcode import intcode


def arcade(input_path='day_13_input.txt'):
    with open(os.path.join('..', input_path), 'r') as f:
        data = list(map(int, f.read().split(',')))

    blocks = 0

    arcade_computer = intcode(data)
    try:
        while True:
            x = next(arcade_computer)
            y = next(arcade_computer)
            tile_id = next(arcade_computer)

            if tile_id == 2:
                blocks += 1
    except StopIteration:
        pass

    return blocks


if __name__ == '__main__':
    cells_1 = arcade()
    print('Part 1: %s' % cells_1)

    # First part answer:  258
    # Second part answer:
