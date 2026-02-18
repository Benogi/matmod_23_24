import numpy as np


class PairwiseDistanceCalculator:
    def __init__(self, vectors_1, vectors_2):
        self.vectors_1 = vectors_1
        self.vectors_2 = vectors_2

    def compute_distance_no_loop(self):
        n_1 = len(self.vectors_1)
        n_2 = len(self.vectors_2)

        result = np.zeros((n_1, n_2))

        ab = self.vectors_1 @ self.vectors_2.T    #matrixok szorzas es transzponalt # dim = (n_1, n_2)
        a2 = np.sum(self.vectors_1 ** 2, axis = 1).reshape((n_1, 1))  # dim = (n_1, 1) # reshape a broadcasting ignoralasa miatt kell
        b2 = np.sum(self.vectors_2 ** 2, axis = 1)  # dim = (n_2, )
        result = a2 - 2 * ab + b2

        return result
