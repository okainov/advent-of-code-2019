import os
from copy import copy

import math


def simplify_delta(delta):
    gcd = math.gcd(delta[0], delta[1])
    return delta[0] // gcd, delta[1] // gcd


def calculate_visible(data, x, y):
    data = copy(data)
    start_point = (x, y)
    deltas = set()

    for p in data:
        if p == start_point:
            continue
        delta = simplify_delta((p[0] - x, p[1] - y))
        deltas.add(delta)

    return len(deltas)


if __name__ == '__main__':
    data = {}
    with open(os.path.join('..', 'day_10_input.txt'), 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c not in ['.', '\n']:
                    data[(x, y)] = 1

    # O(n)
    max_dst = None
    for x, y in data:
        # O(n)
        curr_dst = calculate_visible(data, x, y)
        print(f'<{x}, {y}> = {curr_dst}')
        if max_dst is None or curr_dst > max_dst:
            max_dst = curr_dst

    print(max_dst)

    # First part answer:  256
    # Second part answer:
