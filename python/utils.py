def sum_pairs(pair_1, pair_2):
    return pair_1[0] + pair_2[0], pair_1[1] + pair_2[1]


def print_image(image, reversed_y=False):
    height = max(image.keys(), key=lambda x: x[1])[1] + 1
    height_start = min(image.keys(), key=lambda x: x[1])[1]
    width = max(image.keys(), key=lambda x: x[0])[0] + 1
    width_start = min(image.keys(), key=lambda x: x[0])[0]

    height_range = range(height_start, height)
    if reversed_y:
        height_range = reversed(height_range)
    for y in height_range:
        # Print newline
        print('')
        for x in range(width_start, width):
            char = chr(0x2588 + 9)
            if image[(x, y)] in [1, '1']:
                char = chr(0x2588)
            print(char, end='')
