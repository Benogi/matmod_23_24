
import matplotlib.pyplot as plt

from k_means_clustering import KMeansClustering

class ClusterPlotting:
    def __init__(self, clustering):
        self.clustering = clustering


    def run(self):
        colors = ['lightblue', 'pink', 'lightgreen']
        centr_colors = ['blue', 'red', 'darkgreen']

        for cl_idx in range(0, self.clustering.k):
            clust = self.clustering.clusters[cl_idx]
            centr = self.clustering.centroids[cl_idx]
            color = colors[cl_idx]
            centr_color = centr_colors[cl_idx]

            x = clust[:, 0]
            y = clust[:, 1]
            plt.scatter(x, y, c=color)
            plt.scatter(centr[0], centr[1], c=centr_color, s=50)