from matplotlib import pyplot as plt

from src.epidemic.model import EpidemicModel


def main():
    height = 15
    width = 15
    number_of_agents = 100
    model = EpidemicModel(height=height,
                          width=width,
                          n_agents=number_of_agents)
    t_max = 100
    for t in range(0, t_max):
        model.step()

    model_data = model.datacollector.get_model_vars_dataframe()
    model_data.plot()
    plt.show()


if __name__ == '__main__':
    main()
