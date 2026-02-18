from src.matematikai_programozas.matrix import Matrix

"""
Table of contents of main.py
    - predefined functions
    - main function (scroll down)
"""

# ______________________________________________________________________________
def generate_test_matrices():
    matrices = {}
    matrix_configs = [
        ("matrix1", 3, 3),
        ("matrix2", 3, 3),
        ("matrix3", 2, 2),
        ("matrix4", 2, 2),
        ("matrix5", 3, 2),
        ("matrix6", 2, 3)
    ]

    for name, rows, cols in matrix_configs:
        matrix = Matrix.randmat(rows, cols)
        matrices[name] = matrix
        print(f"{name.capitalize()}: \n", matrix)
        print()

    return matrices

def test_overloaded_operations(matrices):
    # Test addition with matrices
    print("Matrix 1 + Matrix 2:")
    print(matrices["matrix1"] + matrices["matrix2"])
    print()

    # Test subtraction with matrices
    print("Matrix 1 - Matrix 2:")
    print(matrices["matrix1"] - matrices["matrix2"])
    print()

    # Test element-wise multiplication with matrices
    print("Matrix 1 * Matrix 2 (element-wise):")
    print(matrices["matrix1"] * matrices["matrix2"])
    print()

    # Test scalar multiplication with a matrix
    print("Matrix 3 * 2 (scalar multiplication):")
    print(matrices["matrix3"] * 2)
    print()

    # Test scalar multiplication with a matrix
    print("2 * Matrix 3 (scalar multiplication):")
    print(2 * matrices["matrix3"])
    print()

    # Test matrix multiplication with compatible matrices
    print("Matrix 5 @ Matrix 6 (matrix multiplication):")
    print(matrices["matrix5"] @ matrices["matrix6"])
    print()

def test_transposition(matrices):
    # Test transposition with a random matrix
    print("Original Matrix 1: \n", matrices["matrix1"])
    print()
    print("Transposed Matrix 1: \n", matrices["matrix1"].get_transposed())

def test_algebraic_properties(matrices):
    #--------------------------------
    # @title Associativity of addition
    print("Test of associativity of addition \n \
          ((Matrix 1 + Matrix 2) + Matrix new == Matrix 1 + (Matrix 2 + Matrix new)):")

    # Create a new random matrix of the same dimensions as matrix1 and matrix2
    matrix_new = Matrix.randmat(3, 3)

    Matrix.test_property(
        left_side=((matrices['matrix1'] + matrices['matrix2']) + matrix_new),
        right_side=(matrices['matrix1'] + (matrices['matrix2'] + matrix_new))
    )
    print()
    #--------------------------------
    # @title Commutativity of addition
    print("Test of commutativity of addition \n \
          (Matrix 1 + Matrix 2 == Matrix 2 + Matrix 1):")

    Matrix.test_property(left_side=(matrices['matrix1'] + matrices['matrix2']),
                         right_side=(matrices['matrix2'] + matrices['matrix1']))
    print()
    #--------------------------------
    # @title Associativity of matrix multiplication
    print("Test of associativity of matrix multiplication \n \
          ((Matrix 5 @ Matrix 6) @ Matrix 5 == Matrix 5 @ (Matrix 6 @ Matrix 5)):")

    # Note: For associativity of matrix multiplication (A @ B) @ C == A @ (B @ C),
    # the dimensions must be compatible for both operations.
    # If A is m x n, B is n x p, and C is p x q, then (A @ B) is m x p and (A @ B) @ C is m x q.
    # Also, (B @ C) is n x q and A @ (B @ C) is m x q.
    # So, the inner dimensions must match: n=n and p=p. The outer dimensions determine the result size: m x q.

    # Using matrices 5 (3x2) and 6 (2x3), we can test (Matrix 5 @ Matrix 6) @ Matrix 5
    # Matrix 5 (3x2) @ Matrix 6 (2x3) results in a 3x3 matrix.
    # A 3x3 matrix @ Matrix 5 (3x2) results in a 3x2 matrix.
    # For the right side: Matrix 6 (2x3) @ Matrix 5 (3x2) results in a 2x2 matrix.
    # Matrix 5 (3x2) @ a 2x2 matrix results in a 3x2 matrix.
    # The dimensions are compatible for this specific test using matrix5 and matrix6.

    Matrix.test_property(left_side=((matrices['matrix5'] @ matrices['matrix6']) @ matrices['matrix5']),
                         right_side=(matrices['matrix5'] @ (matrices['matrix6'] @ matrices['matrix5'])))

    print()
    #--------------------------------
    # @title Commutativity of matrix multiplication
    print("Test of commutativity of matrix multiplication \n \
          (Matrix 1 @ Matrix 2 == Matrix 2 @ Matrix 1):")

    # Note: Matrix multiplication is generally not commutative.
    # This test will likely show that the result is False.

    # Use square matrices of the same dimensions for this test, e.g., matrix1 (3x3) and matrix2 (3x3).
    # If A is m x n and B is n x m, then A @ B is m x m and B @ A is n x n.
    # For commutativity (A @ B == B @ A), the resulting matrices must have the same dimensions,
    # which requires m = n.

    Matrix.test_property(left_side=(matrices['matrix1'] @ matrices['matrix2']),
                         right_side=(matrices['matrix2'] @ matrices['matrix1']))
    print()
    #--------------------------------
    # @title Distributive property of matrix multiplication over addition
    print("Test of distributive property of matrix multiplication over addition \n \
          (Matrix 5 @ (Matrix 6 + Matrix 5.get_transposed()) \n \
          == \n \
          Matrix 5 @ Matrix 6 + Matrix 5 @ Matrix 5.get_transposed()):")

    # Note: For the distributive property A @ (B + C) == A @ B + A @ C,
    # the dimensions must be compatible for both addition and multiplication.
    # If A is m x n, B and C must be n x p. Then A @ B and A @ C are m x p, and A @ (B + C) is also m x p.
    # We can use Matrix 5 (3x2) as A, Matrix 6 (2x3) as B, and the transpose of Matrix 5 (2x3) as C.
    # This satisfies the dimension requirements: A is 3x2, B is 2x3, and C is 2x3.

    Matrix.test_property(left_side=matrices['matrix5'] @ (matrices['matrix6'] +
                          matrices['matrix5'].get_transposed()),
                         right_side=(matrices['matrix5'] @ matrices['matrix6']) +
                          (matrices['matrix5'] @ matrices['matrix5'].get_transposed()))

    print()
# ______________________________________________________________________________

def main():
    # matrices
    matrices = generate_test_matrices()
    print(matrices)

    # tests
    test_overloaded_operations(matrices)
    test_transposition(matrices)
    test_algebraic_properties(matrices)

if __name__ == '__main__':
    main()
