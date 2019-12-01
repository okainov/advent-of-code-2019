if __name__ == '__main__':
    result = 0
    with open('day_1_input.txt', 'r') as f:
        for line in f:
            result += int(line) // 3 - 2

    print(result)
