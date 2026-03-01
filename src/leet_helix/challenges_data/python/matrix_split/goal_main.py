# TODO: Move 'dot_product' and 'transpose' to math_lib.py
# TODO: Move 'sigmoid' from math_lib.py to this file


def process_data(data):
    # Some application logic that stays here
    if not data:
        return []
    result = []
    for row in data:
        result.append([x * 2 for x in row])
    return result


# Sigmoid here
def sigmoid(x):
    """
    Calculate the sigmoid of x.
    """
    return 1 / (1 + 2.72 ** (-x))
