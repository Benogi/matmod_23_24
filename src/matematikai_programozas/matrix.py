import random
random.seed(42)

# HINT FOR OPERATORS: https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
class Matrix:
      """
      A class to represent a matrix using nested lists.
      """
      def __init__(self, data):
          """
          Constructor for the Matrix class.

          Args:
              data: A list of lists representing the matrix.

          Raises:
              ValueError: If the input is not a rectangular table.

          Some commonly used subfunctions explained:
              all():    function returns True if
                        all the checks performed by the generator expression
                        (for every row in data) evaluate to True.

              .join():  It works with an iterable (like a list, tuple, or set) of strings
                        and concatenates the elements of the iterable into a single string.

              .data[0]: This gets the number of columns in the matrix
                        by checking the length of its first row.
          """
          if not data or not all(
              isinstance(row, list) and len(row) == len(data[0]) for row in data
          ):
              raise ValueError("Input must be a rectangular table.")


          self.data = data

      def __str__(self):
          """
          Returns a string representation of the matrix
          with elements rounded to 4 digits.
          """
          return "\n".join(
              [" ".join([f"{x:.4f}" for x in row]) for row in self.data]
          )

      def __add__(self, other):
          """
          Overloads the addition operator for matrix addition.

          Args:
              other: Another Matrix object.

          Returns:
              A new Matrix object representing the sum of the two matrices.

          Raises:
              ValueError: If the matrices have different dimensions.
          """
          if len(self.data) != len(other.data) or \
             len(self.data[0]) != len(other.data[0]):
              raise ValueError(
                  "Matrices must have the same dimensions for addition."
              )
          result_data = [
              [self.data[i][j] + other.data[i][j]
               for j in range(len(self.data[0]))]
              for i in range(len(self.data))
          ]
          return Matrix(result_data)

      def __sub__(self, other):
          """
          Overloads the subtraction operator for matrix subtraction.

          Args:
              other: Another Matrix object.

          Returns:
                A new Matrix object representing the difference of the two matrices.

            Raises:
                ValueError: If the matrices have different dimensions.
            """
          if len(self.data) != len(other.data) or \
             len(self.data[0]) != len(other.data[0]):
              raise ValueError(
                  "Matrices must have the same dimensions for subtraction."
              )
          result_data = [
              [self.data[i][j] - other.data[i][j]
               for j in range(len(self.data[0]))]
              for i in range(len(self.data))
          ]
          return Matrix(result_data)

      def __mul__(self, other):
          """
          Overloads the multiplication operator
          for element-wise multiplication or scalar multiplication.

          Args:
              other: Another Matrix object or a constant (int or float).

          Returns:
              A new Matrix object representing the product.

          Raises:
              ValueError: If the other operand is a Matrix with different dimensions.
              TypeError: If the other operand is not a Matrix, int, or float.
          """
          if isinstance(other, Matrix):
              if len(self.data) != len(other.data) or \
                 len(self.data[0]) != len(other.data[0]):
                  raise ValueError(
                      "Matrices must have the same dimensions for "
                      "element-wise multiplication."
                  )
              result_data = [
                  [self.data[i][j] * other.data[i][j]
                   for j in range(len(self.data[0]))]
                  for i in range(len(self.data))
              ]
              return Matrix(result_data)
          elif isinstance(other, (int, float)):
              result_data = [
                  [self.data[i][j] * other for j in range(len(self.data[0]))]
                  for i in range(len(self.data))
              ]
              return Matrix(result_data)
          else:
              raise TypeError(
                  "Operand must be a Matrix or a constant (int or float)."
              )


      def __rmul__(self, other):
           """
           Overloads the right multiplication operator for scalar multiplication.

           Args:
               other: A constant (int or float).

           Returns:
               A new Matrix object representing the scalar product.

           Raises:
               TypeError: If the other operand is not an int or float.
           """
           if isinstance(other, (int, float)):
               # Delegate to the __mul__ method for the actual multiplication
               return self.__mul__(other)
           else:
               return NotImplemented


      def __matmul__(self, other):
          """
          Overloads the matrix multiplication operator.

          Args:
              other: Another Matrix object.

          Returns:
              A new Matrix object representing the matrix product.

          Raises:
              ValueError: If the matrices cannot be multiplied (dimensions mismatch).
          """
          if len(self.data[0]) != len(other.data):
              raise ValueError(
                  "Number of columns in the first matrix must equal the "
                  "number of rows in the second matrix for matrix "
                  "multiplication."
              )

          result_data = [
              [0 for _ in range(len(other.data[0]))]
              for _ in range(len(self.data))
          ]
          for i in range(len(self.data)):
              for j in range(len(other.data[0])):
                  for k in range(len(other.data)):
                      result_data[i][j] += self.data[i][k] * other.data[k][j]
          return Matrix(result_data)

      def __eq__(self, other):
          """
          Overloads the equality operator for matrix comparison.

          Args:
              other: Another object to compare with.

          Returns:
              True if the matrices are equal, False otherwise.
          """
          if not isinstance(other, Matrix):
              return False
          if self.shape != other.shape:
              return False
          for i in range(self.shape[0]):
              for j in range(self.shape[1]):
                  if self.data[i][j] != other.data[i][j]:
                      return False
          return True

      def get_transposed(self):
          """
          Returns the transposed matrix.

          Returns:
              A new Matrix object representing the transposed matrix.
          """
          transposed_data = [
              [self.data[j][i] for j in range(len(self.data))]
              for i in range(len(self.data[0]))
          ]
          return Matrix(transposed_data)

      @property # Instead of matrix_instance.shape(), able to use matrix_instance.shape
      def shape(self):
          """
          Returns the shape of the matrix as a tuple (rows, columns).
          """
          return (len(self.data), len(self.data[0]))

      @classmethod # Methods that create and return instances of the class in different ways.
      def randmat(cls, rows, cols):
          """
          Generates a matrix with random integers between 0 and 9.

          Args:
              rows: The number of rows in the matrix.
              cols: The number of columns in the matrix.

          Returns:
              A new Matrix object with random integers.
          """
          random_data = [
              [random.randint(0, 9) for _ in range(cols)]
              for _ in range(rows)
          ]
          return cls(random_data)

      @classmethod # Operates on the class itself
      def test_property(cls, left_side, right_side):
          """
          Evaluates two expressions representing the left and right sides of an equation,
          prints the results, and checks for equality.

          Args:
              left_side: Expression for the left side.
              right_side: Expression for the right side.
          """

          print("left side: \n", left_side)
          print()
          print("right side: \n", right_side)
          print()

          print("Matrix equality:", left_side == right_side)