import os


def get_number(mylist, i):
    pattern = produce_pattern(i)
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
        data = f.read().strip()

    offset = int(data[:7])
    data = list(map(int, list(data))) * 10000

    # Offset for the given input is 5 976 267 while the total length is 650*10k, so real message is faaaaar after
    # the first half.
    # Thus we'll end up with only lower part of upper triangular matrix having only ones

    interesting_data = data[offset:]

    n = len(interesting_data)

    result_list = [0] * (n + 1)
    # Just iterate required 100 times...
    for iteration in range(100):
        # But not over the whole input, but only on it's part starting from offset
        # And since it's in the lower part of the matrix, "pattern" is just sum of the items
        for i in reversed(range(n)):
            result_list[i] = result_list[i + 1] + interesting_data[i]
            result_list[i + 1] = int(str(result_list[i + 1])[-1])

        result_list[0] = int(str(result_list[0])[-1])
        # Output is the new input
        interesting_data, result_list = result_list, [0] * (n + 1)

    print(''.join(map(str, interesting_data[:8])))

    # First part answer:  94935919
    # Second part answer: 24158285
