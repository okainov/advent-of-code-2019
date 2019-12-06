import os

if __name__ == '__main__':
    result = 0
    data = {}
    with open(os.path.join('..', 'day_6_input.txt'), 'r') as f:
        for line in f:
            a, b = line.split(')')
            b = b.strip()
            data[b] = [a, False]

    stack = list(data.keys())
    while stack:
        v = stack.pop()
        result += 1
        if data[v][0] in data:
            stack.append(data[v][0])
    print('Part 1: %s' % result)

    stack = ['YOU']
    i = 0
    while stack:
        v = stack.pop()
        data[v][1] = i
        if data[v][0] in data:
            stack.append(data[v][0])

        i += 1

    stack = ['SAN']
    i = 0
    while stack:
        v = stack.pop()
        if data[v][1] is not False:
            print('Part 2: %s' % str(i + data[v][1] - 2))
            break
        stack.append(data[v][0])
        i += 1

    # First part answer:  162439
    # Second part answer: 367
