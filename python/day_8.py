import os

from python.utils import print_image

if __name__ == '__main__':
    result = 0
    with open(os.path.join('..', 'day_8_input.txt'), 'r') as f:
        data = f.read()

    final_image = {}

    WIDTH = 25
    HEIGHT = 6
    for i, c in enumerate(data):
        i = i % (WIDTH * HEIGHT)
        y = i // 25
        x = i - 25 * y

        if (x, y) in final_image:
            # We already know the color
            continue

        if c == '2':
            # Nothing to do with transparent
            continue

        final_image[(x, y)] = c

    print_image(final_image)

    # First part answer:  2048
    # Second part answer: HFYAK
