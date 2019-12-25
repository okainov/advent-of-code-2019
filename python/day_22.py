import copy
import math
import os


def apply_operations(operations, length=10007):
    deck = list(range(length))

    for operation, value in operations:
        if operation == 'reverse':
            deck = list(reversed(deck))
        elif operation == 'cut':
            deck = deck[value:] + deck[:value]
        elif operation == 'increment':
            new_deck = [None] * len(deck)
            i = 0
            for q in range(len(deck)):
                new_deck[i] = deck[q]
                i = (i + value) % len(deck)
            deck = new_deck

    return deck


def simplify_operations(operations, N=10007):
    operations = copy.deepcopy(operations)
    while len(operations) > 2:
        last_three = operations[-3:]
        ops = [x[0] for x in last_three]

        if ops == ['increment', 'cut', 'increment']:
            operations.pop()
            operations.pop()
            operations.pop()

            operations.append(('increment', last_three[0][1] * last_three[2][1] % N))
            operations.append(('cut', last_three[1][1] * last_three[2][1] % N))
        elif ops == ['cut', 'increment', 'cut']:
            operations.pop()
            operations.pop()
            operations.pop()

            operations.append(last_three[1])
            operations.append(('cut', (last_three[0][1] * last_three[1][1] + last_three[2][1]) % N))
        elif ops == ['reverse', 'increment', 'cut']:
            operations.pop()
            operations.pop()
            operations.pop()

            operations.append(('cut', -1))
            operations.append(('increment', -last_three[1][1] % N))
            operations.append(last_three[2])
        elif ops == ['increment', 'increment', 'cut']:
            operations.pop()
            operations.pop()
            operations.pop()

            operations.append(('increment', last_three[1][1] * last_three[0][1] % N))
            operations.append(last_three[2])

    return operations


def combine(increment_1, cut_1, increment_2, cut_2, N):
    increment_arg = (increment_1 * increment_2) % N
    cut_arg = (increment_2 * cut_1 + cut_2) % N
    return increment_arg, cut_arg


def decompose_to_binary(number):
    powers = {}
    current_power = math.floor(math.log(number, 2))
    while current_power >= 0:
        if number >= 2 ** current_power:
            powers[current_power] = 1
        else:
            powers[current_power] = 0
        number = number % 2 ** current_power
        current_power -= 1
    return powers


def xgcd(a, b):
    """
    return (g, x, y) such that a*x + b*y = g = gcd(a, b)
    See https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    """
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def solve_part_2(operations, N, number_of_shuffles, required_position):
    base_simple_operations = simplify_operations(operations, N)

    # For our input, all the shuffling is equal to 1 increment + 1 cut
    base_increment_arg = base_simple_operations[0][1]
    base_cut_arg = base_simple_operations[1][1]

    # Decompose out amount of shuffles to binary powers
    powers = decompose_to_binary(number_of_shuffles)

    # Calculate coefficients for our shuffling 2^i times
    transform_power_args = {0: (base_increment_arg, base_cut_arg)}
    for i in range(1, len(powers)):
        transform_power_args[i] = combine(transform_power_args[i - 1][0], transform_power_args[i - 1][1],
                                          transform_power_args[i - 1][0], transform_power_args[i - 1][1],
                                          N)

    # Neutral values for increment and shuffling
    result_inc = 1
    result_cut = 0

    # Apply coefficients to get final shuffling coefficients
    for i in range(len(powers)):
        if powers[i] == 1:
            result_inc, result_cut = combine(result_inc, result_cut, transform_power_args[i][0],
                                             transform_power_args[i][1], N)

    # print('Final shuffling corresponds to <increment> <cut>:')
    # print(result_inc, result_cut)
    # 7105969895355 107599871118268

    # Need position 107599871118268 + 2020 after increment

    # Trying to solve
    # 7105969895355*x = 107599871120288  (mod 119315717514047)
    #  ^ increment      ^cut_amount + 2020       ^ length of cards
    # Wolfram is quite good at that
    # https://www.wolframalpha.com/input/?i=7105969895355*x+%3D+107599871120288++mod+119315717514047

    # result_inc* b + N*a = 1
    # result_inc*b = 1 (mod N)
    _, a, b = xgcd(N, result_inc)

    result = ((result_cut + required_position) * b) % N
    return result


if __name__ == '__main__':

    operations = []
    with open(os.path.join('..', 'day_22_input.txt'), 'r') as f:
        for line in f:
            if line.startswith('deal into new stack'):
                operations.append(('reverse', None))
            elif line.startswith('cut'):
                cut = int(line[3:])
                operations.append(('cut', cut))
            elif line.startswith('deal with increment'):
                increment = int(line[19:])
                operations.append(('increment', increment))

    # Part 1
    N = 10007
    simple_operations = simplify_operations(operations, N)
    simple_deck = apply_operations(simple_operations, N)
    for i, card in enumerate(simple_deck):
        if card == 2019:
            print(f'Part 1: {i}')
            break

    # Part 2
    N = 119315717514047
    number_of_shuffles = 101741582076661
    result = solve_part_2(operations, N, number_of_shuffles, 2020)
    print(f'Part 2: {result}')

    # First part answer: 7665
    # Second part answer: 41653717360577
