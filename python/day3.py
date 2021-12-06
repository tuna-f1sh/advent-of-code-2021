from inputs import get_input

def calculate_power_consumption(diag):
    """
    >>> example = get_input(3, example=True)
    >>> calculate_power_consumption(example)
    (22, 9)
    """
    # get bit length for shift
    bit_length = len(diag[0])
    binary = [*map(lambda l: int(l, base=2), diag)]

    ones_count = [0] * bit_length

    for b in binary:
        for bit in range(bit_length):
            ones_count[bit] += (b >> bit) & 0x01

    gamma_rate = 0
    epsilon_rate = 0

    for i, b in enumerate(map(lambda r: r > len(diag)/2, ones_count)):
        gamma_rate += 1 << i if b else 0
        epsilon_rate += 1 << i if not b else 0

    return gamma_rate, epsilon_rate

def calculate_life_support_rating(diag):
    """
    >>> example = get_input(3, example=True)
    >>> calculate_life_support_rating(example)
    (23, 10)
    """
    # get bit length for shift
    bit_length = len(diag[0])
    binary = [*map(lambda l: int(l, base=2), diag)]

    ones_count = [0] * bit_length

    for b in binary:
        for bit in range(bit_length):
            ones_count[bit] += (b >> bit) & 0x01

    gamma_rate = 0
    epsilon_rate = 0

    for i, b in enumerate(map(lambda r: r > len(diag)/2, ones_count)):
        gamma_rate += 1 << i if b else 0
        epsilon_rate += 1 << i if not b else 0

    return gamma_rate, epsilon_rate

dinput = get_input(3)
part1 = calculate_power_consumption(dinput)

print(f"Part 1 result: {part1[0] * part1[1]}")
# print(f"Part 2 result: {sub2.horizontal * sub2.depth}")
