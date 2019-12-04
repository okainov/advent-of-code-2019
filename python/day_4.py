import os


def is_good_pass(password):
    password = str(password)

    double_digit = False
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            double_digit = True
        if password[i] > password[i + 1]:
            return False
    return double_digit


if __name__ == '__main__':
    result = 0
    for i in range(278384, 824795):
        if is_good_pass(i):
            result += 1

    print(result)

    # First part answer:  1431
    # Second part answer: 48012
