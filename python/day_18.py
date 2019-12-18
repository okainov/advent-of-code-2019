import os
from collections import defaultdict


def distance(data, a, b=None, check_doors=True, opened_doors=None):
    if opened_doors is None:
        opened_doors = []
    visited = set()
    markers = defaultdict(lambda: None)
    markers[a] = 0

    v_to_visit = [a]
    while v_to_visit:
        v = v_to_visit.pop(0)
        visited.add(v)

        neightbors = [(v[0] + 1, v[1]),
                      (v[0] - 1, v[1]),
                      (v[0], v[1] + 1),
                      (v[0], v[1] - 1)]
        for neightbor in neightbors:
            if neightbor not in visited and data[neightbor] != '#':
                if check_doors and data[neightbor].isalpha() and data[neightbor].upper() == data[neightbor] and data[
                    neightbor].lower() not in opened_doors:
                    # Closed door here
                    continue

                if neightbor in markers:
                    markers[neightbor] = min(markers[v] + 1, markers[neightbor])
                else:
                    markers[neightbor] = markers[v] + 1
                v_to_visit.append(neightbor)
    return markers


def open_doors(data, starting_position, passed_steps=0, opened_doors=None):
    if opened_doors is None:
        opened_doors = []
    distances = distance(data, starting_position, check_doors=True, opened_doors=opened_doors)
    possible_keys = []
    for pair in data:
        if data[pair].isalpha():
            if data[pair].lower() == data[pair] and pair in distances and data[pair].lower() not in opened_doors:
                possible_keys.append((data[pair], pair, distances[pair]))

    if not possible_keys:
        # Done already
        return passed_steps

    min_distance = None
    for key, key_position, dst in sorted(possible_keys, key=lambda x: x[2]):
        # Try to open every accessible key and see the outcome, then select the best option
        if min_distance is not None and passed_steps + dst > min_distance:
            # There is even no need to calculate this option, it cannot be better
            continue
        trial_distance = open_doors(data, key_position, passed_steps=passed_steps + dst,
                                    opened_doors=opened_doors + [key])
        if passed_steps == 0:
            print(f'Trial {trial_distance}')
        if min_distance is None or trial_distance < min_distance:
            min_distance = trial_distance

    return min_distance


if __name__ == '__main__':
    state = {}
    x = 0
    y = 0
    with open(os.path.join('..', 'day_18_input.txt'), 'r') as f:
        for line in f:
            for c in line:
                state[(x, y)] = c
                x += 1
            y += 1
            x = 0

    keys = []
    doors = []
    starting_position = None
    for pair in state:
        if state[pair].isalpha():
            if state[pair].lower() == state[pair]:
                keys.append(state[pair])
            else:
                doors.append(state[pair])
        elif state[pair] == '@':
            starting_position = pair
    # print(sorted(keys))
    # print(sorted(doors))
    print(starting_position)

    print(open_doors(state, starting_position))
    #
    # distances = distance(state, starting_position, check_doors=True)
    # #distances2 = distance(state, starting_position, check_doors=False)
    # #assert distances == distances2
    # for pair in state:
    #     if state[pair].isalpha():
    #         if state[pair].lower() == state[pair]:
    #             keys.append(state[pair])
    #             print(f'Key {state[pair]}, direct distance {distances[pair]}')
    #         else:
    #             doors.append(state[pair])
    #             print(f'Door {state[pair]}, direct distance {distances[pair]}')
    #     elif state[pair] == '@':
    #         starting_position = pair

    # First part answer:  8408
    # Second part answer: 1168948
