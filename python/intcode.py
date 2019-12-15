from collections import defaultdict

import sys


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


def intcode(data, print_output=False):
    # Version of Intcode program which returns back waiting for input and also yields the output
    # Make explicit copy to do not mess with initial data
    data = Program(data)

    i = 0
    relative_base = 0
    print('========================INIT INTCODE=================')
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

            yield "I WANNA INPUT"
            data[result_pos] = yield
            yield "DUMMY YIELD STUPID PYTHON"
            if data[result_pos] is None:
                print('========================ASKING FOR INPUT=================')
                sys.exit(-3)
            i += 2
        elif operation == 4:
            # Print
            result = data[get_param(data, i + 1, params[-1], relative_base)]
            if print_output:
                print(result)
            yield result
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


def single_input_intcode(data, input_value):
    """
    Creates and executes Intcode Computer with a single input
    :param data: Intcode source
    :param input: single input value
    :return: list of outputs
    """

    outputs = []

    calculator = intcode(data)
    try:
        while True:
            next(calculator)
            outputs.append(calculator.send(input_value))
            while True:
                outputs.append(next(calculator))
    except StopIteration:
        pass
    return outputs
