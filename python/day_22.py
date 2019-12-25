import os

if __name__ == '__main__':
    deck = list(range(10007))
    with open(os.path.join('..', 'day_22_input.txt'), 'r') as f:
        for line in f:
            if line.startswith('deal into new stack'):
                deck = list(reversed(deck))
            elif line.startswith('cut'):
                cut = int(line[3:])

                deck = deck[cut:] + deck[:cut]
            elif line.startswith('deal with increment'):
                increment = int(line[19:])

                new_deck = [None] * len(deck)
                i = 0
                for q in range(len(deck)):
                    new_deck[i] = deck[q]
                    i = (i + increment) % len(deck)
                deck = new_deck

    print(deck)

    for i, card in enumerate(deck):
        if card == 2019:
            print(f'Part 1: {i}')
            break

    # First part answer: 7665
    # Second part answer:
