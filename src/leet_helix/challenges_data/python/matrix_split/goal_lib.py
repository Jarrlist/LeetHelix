# TODO: Move 'sigmoid' function to matrix_processor.py


# dot_product here
def dot_product(v1, v2):
    """
    Calculate the dot product of two vectors.
    """
    if len(v1) != len(v2):
        raise ValueError("Vectors must be the same length")
    return sum(x * y for x, y in zip(v1, v2))


# transpose here
def transpose(matrix):
    """
    Transpose a matrix (swap rows and columns).
    """
    if not matrix:
        return []
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]
