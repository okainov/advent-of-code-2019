import itertools
import os
from collections import defaultdict

if __name__ == '__main__':
    result = 0
    with open(os.path.join('..', 'day_8_input.txt'), 'r') as f:
        data = f.read()

    current_layer_numbers = defaultdict(int)
    min_zeroes = None
    min_layer = None

    for i, c in enumerate(data):
        if (i+1) % (25*6) == 0:
            if min_zeroes is None or current_layer_numbers['0'] < min_zeroes:
                min_layer = current_layer_numbers
                min_zeroes = current_layer_numbers['0']
            current_layer_numbers = defaultdict(int)
        if c not in current_layer_numbers:
            current_layer_numbers[c] = 0
        current_layer_numbers[c] += 1

    print(min_layer['1'] * min_layer['2'])

    # First part answer:  2048
    # Second part answer:
