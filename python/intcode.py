from collections import defaultdict

import sys


class InputNeededException(Exception):
    pass


class HaltException(Exception):
    pass


class OutputException(Exception):
    pass


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


class Intcode:
    def __init__(self, source):
        self.memory = Program(source)

        self.ip = 0
        self.relative_base = 0
        self.input = []

        self.ticks = 0

        self.unread_outputs = []

    def execute(self):
        qq = self.tick()
        try:
            while True:
                value = qq.send(None)
                yield value
                if value == "I WANNA INPUT":
                    yield value
        except StopIteration:
            print('Execution done')
        except InterruptedError:
            print('Halt')

    def add_input(self, input_value):
        if isinstance(input_value, list):
            self.input.extend(input_value)
        else:
            self.input.append(input_value)

    def tick(self):
        self.ticks += 1
        full_operation = f"{self.memory[self.ip]:05d}"

        operation = int(full_operation[-2:])
        params = full_operation[:-2]

        if operation == 99:
            raise InterruptedError

        if operation == 1:
            # Add
            result_pos = get_param(self.memory, self.ip + 3, params[-3], self.relative_base)
            self.memory[result_pos] = self.memory[get_param(self.memory, self.ip + 1, params[-1], self.relative_base)] + \
                                      self.memory[get_param(self.memory, self.ip + 2, params[-2], self.relative_base)]
            self.ip += 4
        elif operation == 2:
            # Multiply
            result_pos = get_param(self.memory, self.ip + 3, params[-3], self.relative_base)
            self.memory[result_pos] = self.memory[get_param(self.memory, self.ip + 1, params[-1], self.relative_base)] * \
                                      self.memory[get_param(self.memory, self.ip + 2, params[-2], self.relative_base)]
            self.ip += 4
        elif operation == 3:
            # Input
            result_pos = get_param(self.memory, self.ip + 1, params[-1], self.relative_base)

            if not self.input:
                raise InputNeededException

            input_value = self.input.pop(0)
            # Flush outputs buffer, assuming all of it have been read already
            self.unread_outputs = []

            self.memory[result_pos] = input_value

            self.ip += 2
        elif operation == 4:
            result = self.memory[get_param(self.memory, self.ip + 1, params[-1], self.relative_base)]
            self.unread_outputs.append(result)
            self.ip += 2
        elif operation == 5:
            if self.memory[get_param(self.memory, self.ip + 1, params[-1], self.relative_base)]:
                self.ip = self.memory[get_param(self.memory, self.ip + 2, params[-2], self.relative_base)]
            else:
                self.ip += 3
        elif operation == 6:
            if self.memory[get_param(self.memory, self.ip + 1, params[-1], self.relative_base)] == 0:
                self.ip = self.memory[get_param(self.memory, self.ip + 2, params[-2], self.relative_base)]
            else:
                self.ip += 3
        elif operation == 7:
            # If less than
            if self.memory[get_param(self.memory, self.ip + 1, params[-1], self.relative_base)] < \
                    self.memory[get_param(self.memory, self.ip + 2, params[-2], self.relative_base)]:
                self.memory[get_param(self.memory, self.ip + 3, params[-3], self.relative_base)] = 1
            else:
                self.memory[get_param(self.memory, self.ip + 3, params[-3], self.relative_base)] = 0

            self.ip += 4
        elif operation == 8:
            # if equal
            if self.memory[get_param(self.memory, self.ip + 1, params[-1], self.relative_base)] == \
                    self.memory[get_param(self.memory, self.ip + 2, params[-2], self.relative_base)]:
                self.memory[get_param(self.memory, self.ip + 3, params[-3], self.relative_base)] = 1
            else:
                self.memory[get_param(self.memory, self.ip + 3, params[-3], self.relative_base)] = 0
            self.ip += 4
        elif operation == 9:
            # Increase relative base
            self.relative_base += self.memory[get_param(self.memory, self.ip + 1, params[-1], self.relative_base)]
            self.ip += 2


def single_input_intcode(data, input_value):
    """
    Creates and executes Intcode Computer with a single input
    :param data: Intcode source
    :param input: single input value
    :return: list of outputs
    """

    calculator = Intcode(data)
    calculator.add_input(input_value)

    while True:
        try:
            calculator.tick()
        except InputNeededException as e:
            # Should not happen for single input program
            raise e
        except InterruptedError:
            break
    return calculator.unread_outputs
