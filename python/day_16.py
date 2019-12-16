import os


def get_number(mylist, pattern):
    result = 0
    for i, c in enumerate(mylist):
        result += c * pattern[i % len(pattern)]
    return int(str(result)[-1])


def produce_pattern(repetition_times):
    pattern = [0] * repetition_times + [1] * repetition_times + [0] * repetition_times + [-1] * repetition_times
    # Shift the pattern
    pattern = pattern[1:] + [0]
    return pattern


if __name__ == '__main__':
    with open(os.path.join('..', 'day_16_input.txt'), 'r') as f:
        data = list(f.read().strip())

    data = list(map(int, data))
    pattern = produce_pattern(2)

    result_list = []

    for iteration in range(100):
        for i, c in enumerate(data, start=1):
            result_list.append(get_number(data, produce_pattern(i)))
        data = result_list
        result_list = []

        print(f'Iteration {iteration + 1}')
        print(''.joint(data[:8]))

    # First part answer:  94935919
    # Second part answer:
