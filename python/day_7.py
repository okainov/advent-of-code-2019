import itertools
import os

from python.intcode import intcode


def calculate_squence(data, inputs):
    result = 0

    amplifiers = []

    for i in range(len(inputs)):
        amplifier = intcode(data)

        input_prompt = next(amplifier)
        assert input_prompt == 'I WANNA INPUT'
        next(amplifier)  # Rewind to the input place
        amplifier.send(inputs[i])  # Provide input

        amplifiers.append(amplifier)

    while True:
        for i in range(len(inputs)):
            try:
                input_prompt = next(amplifiers[i])
                assert input_prompt == 'I WANNA INPUT'
                next(amplifiers[i])
                amplifiers[i].send(result)
                result = next(amplifiers[i])
            except StopIteration:
                if i == len(inputs) - 1:
                    return result
                else:
                    continue


if __name__ == '__main__':
    result = 0
    with open(os.path.join('..', 'day_7_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))

    max_res = None
    for seq in itertools.permutations([0, 1, 2, 3, 4]):
        current_res = calculate_squence(data, seq)
        if max_res is None or current_res > max_res:
            max_res = current_res
    print('Part 1: %s' % max_res)

    max_res = None
    for seq in itertools.permutations([5, 6, 7, 8, 9]):
        current_res = calculate_squence(data, seq)
        if max_res is None or current_res > max_res:
            max_res = current_res
    print('Part 2: %s' % max_res)

    # First part answer:  67023
    # Second part answer: 7818398
