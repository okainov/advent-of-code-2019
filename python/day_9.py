import os
from collections import defaultdict


class Program:
    def __getitem__(self, item):
        try:
            return self.data[item]
        except IndexError:
            return self.additional_memory[item]

    def __setitem__(self, key, value):
        try:
            self.data[key] = value
        except IndexError:
            self.additional_memory[key] = value

    def __init__(self, data):
        self.data = data[::]
        self.additional_memory = defaultdict(int)


def get_param(data, index, mode, relative_base=0):
    if mode == '0':
        return data[index]
    elif mode == '1':
        return index
    elif mode == '2':
        return data[index] + relative_base
    pass


def solve_day_9(data, input_value=1):
    # Make explicit copy to do not mess with initial data
    data = Program(data)

    i = 0
    relative_base = 0
    while True:
        full_operation = f"{data[i]:05d}"

        operation = int(full_operation[-2:])
        params = full_operation[:-2]

        if operation == 99:
            break

        if operation == 1:
            # Add
            result_pos = get_param(data, i + 3, params[-3], relative_base)
            data[result_pos] = data[get_param(data, i + 1, params[-1], relative_base)] + \
                               data[get_param(data, i + 2, params[-2], relative_base)]
            i += 4
        elif operation == 2:
            # Multiply
            result_pos = get_param(data, i + 3, params[-3], relative_base)
            data[result_pos] = data[get_param(data, i + 1, params[-1], relative_base)] * \
                               data[get_param(data, i + 2, params[-2], relative_base)]
            i += 4
        elif operation == 3:
            # Input
            result_pos = get_param(data, i + 1, params[-1], relative_base)
            data[result_pos] = input_value
            i += 2
        elif operation == 4:
            # Print
            print(data[get_param(data, i + 1, params[-1], relative_base)])
            i += 2
        elif operation == 5:
            if data[get_param(data, i + 1, params[-1], relative_base)]:
                i = data[get_param(data, i + 2, params[-2], relative_base)]
            else:
                i += 3
        elif operation == 6:
            if data[get_param(data, i + 1, params[-1], relative_base)] == 0:
                i = data[get_param(data, i + 2, params[-2], relative_base)]
            else:
                i += 3
        elif operation == 7:
            # If less than
            if data[get_param(data, i + 1, params[-1], relative_base)] < \
                    data[get_param(data, i + 2, params[-2], relative_base)]:
                data[get_param(data, i + 3, params[-3], relative_base)] = 1
            else:
                data[get_param(data, i + 3, params[-3], relative_base)] = 0

            i += 4
        elif operation == 8:
            # if equal
            if data[get_param(data, i + 1, params[-1], relative_base)] == \
                    data[get_param(data, i + 2, params[-2], relative_base)]:
                data[get_param(data, i + 3, params[-3], relative_base)] = 1
            else:
                data[get_param(data, i + 3, params[-3], relative_base)] = 0
            i += 4
        elif operation == 9:
            # Increase relative base
            relative_base += data[get_param(data, i + 1, params[-1], relative_base)]
            i += 2

    return


if __name__ == '__main__':
    result = 0
    with open(os.path.join('..', 'day_9_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))

    solve_day_9(data, input_value=2)

    # First part answer:  3742852857
    # Second part answer: 73439