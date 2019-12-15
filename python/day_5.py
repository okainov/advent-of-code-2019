import os

from python.intcode import intcode, single_input_intcode

if __name__ == '__main__':
    result = 0
    with open(os.path.join('..', 'day_5_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))

    outputs = single_input_intcode(data, 1)
    print(f'Part 1: {outputs}')

    outputs = single_input_intcode(data, 5)
    print(f'Part 2: {outputs}')

    # First part answer:  2845163
    # Second part answer: 9436229
