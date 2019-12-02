import os


def solve_day_2_part_1(data):
    i = 0
    data[1] = 12
    data[2] = 2
    while i < len((data)):
        if data[i] == 99:
            break
        elif data[i] in [1,2]:
            first_pos = data[i+1]
            second_pos = data[i + 2]
            result_pos = data[i+3]
            if data[i] == 1:
                data[result_pos] = data[first_pos] + data[second_pos]
            elif data[i] == 2:
                data[result_pos] = data[first_pos] * data[second_pos]
            i += 4
            continue
        i += 1
    return data[0]


#print(solve_day_2_part_1([1,1,1,4,99,5,6,0,99]))
#print(solve_day_2_part_1([1,1,1,4,99,5,6,0,99]))

if __name__ == '__main__':
    result = 0
    with open(os.path.join('..', 'day_2_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))

    print(solve_day_2_part_1(data))

    # First part answer:  3184233
    # Second part answer: 4773483
