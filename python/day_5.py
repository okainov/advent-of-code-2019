import os


def solve_day_2(data, first=12, second=2):
    # Make explicit copy to do not mess with initial data
    data = data[::]

    data[1] = first
    data[2] = second

    i = 0
    while i < len((data)):
        if data[i] == 99:
            break
        elif data[i] in [1, 2]:
            first_pos = data[i + 1]
            second_pos = data[i + 2]
            result_pos = data[i + 3]
            if data[i] == 1:
                data[result_pos] = data[first_pos] + data[second_pos]
            elif data[i] == 2:
                data[result_pos] = data[first_pos] * data[second_pos]
            i += 4
            continue
        i += 1
    return data[0]


if __name__ == '__main__':
    result = 0
    with open(os.path.join('..', 'day_2_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))

    print('First part answer: %s' % solve_day_2(data))
    for i in range(100):
        for j in range(100):
            if solve_day_2(data, i, j) == 19690720:
                print('Second part answer: %s' % str(100 * i + j))
                break

    # First part answer:  3790689
    # Second part answer: 6533
