import numpy as np

from pairwise_distance_calculator import PairwiseDistanceCalculator

class KMeansClustering:
    def __init__(self,
                 data: np.ndarray, #valtozo: tipus annotacio
                 k: int,
                 n_iter: int) -> None: #fugveny() -> visszateresi ertek:
        """
        Contstructor for the class executing k-means clustering algorithm
        :param np.ndarray data: Points to be clustered
        :param int k: Number of clusters
        :param int n_iter: Number of iterations
        :return: None
        """

        self.data = data
        self.k = k
        self.n_iter = n_iter

        self.__clusters = None  #__nev => privat valtozo, csak a program latja es modosithatja
        self.__centroids = None

        self.__prepare()

    def __prepare(self)\
            -> None:
        n_rows = self.data.shape[0]
        indexes = np.random.choice(n_rows,
                                   self.k,
                                   replace=False)
        self.__centroids = dict(zip(
            range(0, self.k),
            self.data[indexes, :]
        ))  # konvertalas dictionary formatumba
        # self.__centroids = self.data[indexes, :] #minden oszlop kivalasztasa
        self.__clusters = dict()
        for i in range(0, self.k):
            self.__clusters[i] = []

    @property
    def clusters(self)\
            -> dict: # privat valtozo ertekenek megmutatasa a felhasznalonak
        return self.__clusters

    @property
    def centroids(self)\
            -> dict:
        return self.__centroids

    # Run függvény
    def run(self)\
            -> None:
        for i in range(self.n_iter):
            self.__calculate_clusters()
            self.__calculate_centroids()

    # Run függvényei
    def __calculate_clusters(self)\
            -> None: #visszateresi ertek
        parwise_dists = self.calculate_pairwise_distances()
        nearest_centroid_indexes = self.calculate_nearest_centroid_index(
            dists=parwise_dists
        )
        clusters = self.group_by_index(indexes=nearest_centroid_indexes)
        self.__clusters = clusters

    def __calculate_centroids(self)\
            -> None:
        centroids = dict()
        for i in range(0, self.k):
            centroid = np.mean(self.clusters[i], axis=0)
            centroids[i] = centroid
        self.__centroids = centroids

    # segédfüggvények
    def calculate_pairwise_distances(self)\
            -> np.ndarray:
        vectors_1 = self.data
        #vectors_2 = self.centroids.values()
        vectors_2 = np.array(
            [self.centroids[i] for i in range(0, self.k)]
        ) #list comprehension
        calculator = PairwiseDistanceCalculator(
            vectors_1=vectors_1,
            vectors_2=vectors_2
        )
        return calculator.compute_distance_no_loop()

    @staticmethod
    def calculate_nearest_centroid_index(dists: np.ndarray)\
            -> np.ndarray:
        nearest_centroid_indexes = np.argmin(dists, axis=1)
        return nearest_centroid_indexes

    def group_by_index(self,
                       indexes: np.array)\
            -> dict:
        clusters = dict()
        for cl in range(0, self.k):
            clusters[cl] = self.data[indexes == cl]
        return clusters