import os

from python.intcode import intcode, single_input_intcode

if __name__ == '__main__':
    result = 0
    with open(os.path.join('..', 'day_9_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))

    outputs = single_input_intcode(data, 1)
    print(f'Part 1: {outputs}')

    outputs = single_input_intcode(data, 2)
    print(f'Part 2: {outputs}')

    # First part answer:  3742852857
    # Second part answer: 73439
