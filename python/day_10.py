import os
from copy import copy

import math


def dst(a, b):
    return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def add_points(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, c):
    return (a[0] * c, a[1] * c)


def simplify_delta(delta):
    gcd = math.gcd(delta[0], delta[1])
    if gcd > 1:
        return delta[0] // gcd, delta[1] // gcd
    return delta


def calculate_visible(data, x, y):
    data = copy(data)
    del data[(x, y)]
    count = 0
    start_point = (x, y)
    points = sorted(data.keys(), key=lambda p: dst(start_point, p))
    while points:
        p = points.pop(0)
        x_1, y_1 = p
        count += 1
        # Need to simplify delta since it might not be minimal
        delta = simplify_delta((x_1 - x, y_1 - y))
        for i in range(1, 34):
            if add_points(start_point, mul(delta, i)) in points:
                points.remove(add_points(start_point, mul(delta, i)))
        if delta[0] == 0:
            for i in range(1, 34):
                delt = add_points(delta, (0, i * delta[1] / abs(delta[1])))
                if add_points(start_point, delt) in points:
                    points.remove(add_points(start_point, delt))
        if delta[1] == 0:
            for i in range(1, 34):
                delt = add_points(delta, (i * delta[0] / abs(delta[0]), 0))
                if add_points(start_point, delt) in points:
                    points.remove(add_points(start_point, delt))
        if abs(delta[1]) == abs(delta[0]):
            for i in range(1, 34):
                delt = add_points(delta, (i * delta[0] / abs(delta[0]), i * delta[1] / abs(delta[1])))
                if add_points(start_point, delt) in points:
                    points.remove(add_points(start_point, delt))

    return count


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
        # O(n^2)
        curr_dst = calculate_visible(data, x, y)
        print(f'<{x}, {y}> = {curr_dst}')
        if max_dst is None or curr_dst > max_dst:
            max_dst = curr_dst

    print(max_dst)

    # First part answer:  256
    # Second part answer:
