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
    def filter_scrubbers(binary_strs: list, function):
        bit_length = len(binary_strs[0])
        binary_ints = {*map(lambda l: int(l, base=2), set(binary_strs))}

        for bi in range(bit_length-1, -1, -1):
            leading_1 = set(filter(lambda x: x & (1 << bi) == (0x01 << bi), binary_ints))
            leading_0 = binary_ints - leading_1

            if function(len(leading_0), len(leading_1)):
                binary_ints = leading_1
            else:
                binary_ints = leading_0

            if len(binary_ints) == 1:
                return binary_ints.pop()

        # not found
        return 0

    # 1s greater than 0s
    oxygen_rating = filter_scrubbers(diag, lambda x, y: x <= y)
    # 0s greater than 1s
    carbon_dioxide_rating = filter_scrubbers(diag, lambda x, y: x > y)

    return oxygen_rating, carbon_dioxide_rating

dinput = get_input(3)
part1 = calculate_power_consumption(dinput)
part2 = calculate_life_support_rating(dinput)

print(f"Part 1 result: {part1[0] * part1[1]}")
print(f"Part 2 result: {part2[0] * part2[1]}")
