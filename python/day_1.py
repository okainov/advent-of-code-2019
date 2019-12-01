import os


def calculate_fuel(mass):
    total_fuel_mass = 0

    while mass > 0:
        mass = mass // 3 - 2
        if mass <= 0:
            break
        total_fuel_mass += mass
    return total_fuel_mass


if __name__ == '__main__':
    result = 0
    with open(os.path.join('..', 'day_1_input.txt'), 'r') as f:
        for line in f:
            result += calculate_fuel(int(line))

    print(result)

    # First part answer:  3184233
    # Second part answer: 4773483
