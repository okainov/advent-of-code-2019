import itertools
import os


def get_param(data, index, mode):
    if mode == '0':
        return data[index]
    elif mode == '1':
        return index
    pass


def solve_day_7(data):
    # Make explicit copy to do not mess with initial data
    data = data[::]

    i = 0
    inputs = 0
    output = None
    while True:
        full_operation = f"{data[i]:05d}"

        operation = int(full_operation[-2:])
        params = full_operation[:-2]

        if operation == 99:
            break

        if operation == 1:
            result_pos = data[i + 3]
            data[result_pos] = data[get_param(data, i + 1, params[-1])] + data[get_param(data, i + 2, params[-2])]
            i += 4
        elif operation == 2:
            # Multiply
            result_pos = data[i + 3]
            data[result_pos] = data[get_param(data, i + 1, params[-1])] * data[get_param(data, i + 2, params[-2])]
            i += 4
        elif operation == 3:
            # Input
            result_pos = data[i + 1]
            data[result_pos] = yield
            inputs += 1
            i += 2
        elif operation == 4:
            # Print
            output = data[get_param(data, i + 1, params[-1])]
            yield output
            i += 2
        elif operation == 5:
            if data[get_param(data, i + 1, params[-1])]:
                i = data[get_param(data, i + 2, params[-2])]
            else:
                i += 3
        elif operation == 6:
            if data[get_param(data, i + 1, params[-1])] == 0:
                i = data[get_param(data, i + 2, params[-2])]
            else:
                i += 3
        elif operation == 7:
            # If less than
            if data[get_param(data, i + 1, params[-1])] < data[get_param(data, i + 2, params[-2])]:
                data[get_param(data, i + 3, params[-3])] = 1
            else:
                data[get_param(data, i + 3, params[-3])] = 0

            i += 4
        elif operation == 8:
            # if equal
            if data[get_param(data, i + 1, params[-1])] == data[get_param(data, i + 2, params[-2])]:
                data[get_param(data, i + 3, params[-3])] = 1
            else:
                data[get_param(data, i + 3, params[-3])] = 0
            i += 4

    return output


def calculate_squence(data, inputs):
    result = 0

    amplifiers = []

    for i in range(len(inputs)):
        amplifier = solve_day_7(data)
        next(amplifier)
        amplifier.send(inputs[i])

        amplifiers.append(amplifier)

    while True:
        for i in range(len(inputs)):
            result = amplifiers[i].send(result)
            try:
                next(amplifiers[i])
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
