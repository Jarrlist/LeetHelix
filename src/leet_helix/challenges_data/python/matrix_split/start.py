# TODO: Move 'dot_product' and 'transpose' to math_lib.py
# TODO: Move 'sigmoid' from math_lib.py to this file


def dot_product(v1, v2):
    """
    Calculate the dot product of two vectors.
    """
    if len(v1) != len(v2):
        raise ValueError("Vectors must be the same length")
    return sum(x * y for x, y in zip(v1, v2))


def process_data(data):
    # Some application logic that stays here
    if not data:
        return []
    result = []
    for row in data:
        result.append([x * 2 for x in row])
    return result


def transpose(matrix):
    """
    Transpose a matrix (swap rows and columns).
    """
    if not matrix:
        return []
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


# Sigmoid here
