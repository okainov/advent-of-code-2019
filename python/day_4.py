import re


def is_good_pass(password):
    password = 'Q' + str(password) + 'Q'

    double_digit = set()
    for i in range(1, len(password) - 2):
        if password[i] == password[i + 1]:
            double_digit.add(password[i])
        if password[i] > password[i + 1]:
            return False

    is_double_really_double = False
    for digit in double_digit:
        pattern = '[^%s]%s{2}[^%s]' % (digit, digit, digit)
        if re.findall(pattern, password):
            is_double_really_double = True
    return bool(double_digit) and is_double_really_double


if __name__ == '__main__':
    result = 0
    for i in range(278384, 824795):
        if is_good_pass(i):
            result += 1

    print(result)

    # First part answer:  921
    # Second part answer: 603
