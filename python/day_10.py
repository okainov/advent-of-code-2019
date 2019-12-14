import os
from copy import copy

import math


def simplify_delta(delta):
    gcd = math.gcd(delta[0], delta[1])
    return delta[0] // gcd, delta[1] // gcd


def calculate_visible(data, x, y):
    data = copy(data)
    start_point = (x, y)

    polar_points = []
    for p in data:
        if p == start_point:
            continue

        # Coordinates relative to start point
        relative_x = p[0] - x
        relative_y = p[1] - y
        # Convert to polar coordinates
        r = relative_x * relative_x + relative_y * relative_y

        delta = simplify_delta((relative_x, relative_y))

        if delta[1] == 0:
            if delta[0] > 0:
                fi = 90
            else:
                fi = 270
        else:
            fi = math.atan(delta[0] / delta[1])
            fi = math.degrees(fi)

            if relative_y < 0:
                fi += 180
            elif relative_x < 0:
                fi += 360

        polar_points.append({
            'point': p,
            'delta': delta,
            'r': r,
            'fi': fi
        })

    return polar_points


if __name__ == '__main__':
    data = {}
    with open(os.path.join('..', 'day_10_input.txt'), 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if c not in ['.', '\n']:
                    data[(x, -y)] = 1

    # O(n)
    max_dst = None
    station_pos = None
    good_polar_points = None
    for x, y in data:
        # O(n)
        polar_points = calculate_visible(data, x, y)
        curr_dst = len(set([x['fi'] for x in polar_points]))
        print(f'<{x}, {y}> = {curr_dst}')
        if max_dst is None or curr_dst > max_dst:
            max_dst = curr_dst
            station_pos = (x, y)
            good_polar_points = polar_points

    print(f'Station is placed at {station_pos} == {max_dst}')

    sort = sorted(good_polar_points, key=lambda x: (x['fi'], x['r']))

    n_total = len(sort)
    vaporization = []
    i = 0
    while len(vaporization) < n_total:
        vaporize = sort[i]
        vaporization.append(vaporize)
        sort.remove(vaporize)
        if not sort:
            break
        i = i % len(sort)

        if len(set([x['fi'] for x in sort])) == 1:
            # Finish stage, only asteroids on one line left, just vaporize them in order
            continue

        while vaporize['fi'] == sort[i]['fi']:
            i = (i + 1) % len(sort)

    print(vaporization[199]['point'][0] * 100 - vaporization[199]['point'][1])

    # First part answer:  256
    # Second part answer:
