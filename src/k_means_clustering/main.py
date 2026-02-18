import matplotlib.pyplot as plt

from dataloader import Dataloader
from k_means_clustering import KMeansClustering
from clustering_plotter import ClusterPlotting


def main():
    file_url = "https://cs.joensuu.fi/sipu/datasets/s1.txt"
    file_name = "s1.txt"
    dl = Dataloader(file_url=file_url,
                    file_name=file_name)

    clust = KMeansClustering(data=dl.data,
                             k=3,
                             n_iter=10)
    # print(clust.centroids)
    # print(clust.clusters)

    clust.run()
    plotter = ClusterPlotting(clustering=clust)
    plotter.run()
    plt.show()




if __name__ == "__main__":
    main()