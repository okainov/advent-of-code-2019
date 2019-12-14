import os
from collections import defaultdict, namedtuple

import math


def parse_component(text):
    amount, component = text.strip().split(' ')
    return int(amount), component


def get_min_ore(ingridient, amount, reaction_data, cache):
    if ingridient in cache:
        if amount <= cache[ingridient]:
            cache[ingridient] -= amount
            if cache[ingridient] == 0:
                del cache[ingridient]
            return 0
        else:
            amount -= cache[ingridient]
            del cache[ingridient]
    if ingridient == 'ORE':
        return amount

    assert len(reaction_data[ingridient]) == 1
    recipe = reaction_data[ingridient][0]
    required_ore = 0
    for i in recipe['ingridients']:
        required_ore += get_min_ore(i['name'], i['amount'] * math.ceil(amount / recipe['amount']), reaction_data, cache)
    leftovers = recipe['amount'] * math.ceil(amount / recipe['amount']) - amount
    if leftovers > 0:
        if ingridient not in cache:
            cache[ingridient] = 0
        cache[ingridient] += leftovers
    return required_ore


if __name__ == '__main__':
    reaction_data = defaultdict(list)
    Person = namedtuple('Person', 'name age gender')
    with open(os.path.join('..', 'day_14_input.txt'), 'r') as f:
        for line in f:
            ingridients, outcome = line.split('=>')
            ingridients = list(map(parse_component, ingridients.split(',')))
            out_amount, out_thing = parse_component(outcome)
            reaction_data[out_thing].append({
                'amount': out_amount,
                'ingridients': [{'amount': i[0], 'name': i[1]} for i in ingridients]

            })

    cache = {}
    ore_per_fuel = get_min_ore('FUEL', 1, reaction_data, cache)
    print(ore_per_fuel)

    fuel = 2370000
    while get_min_ore('FUEL', fuel, reaction_data, {}) < 1000000000000:
        fuel += 1
    print(fuel - 1)

    # First part answer:  741927
    # Second part answer: 2371699
