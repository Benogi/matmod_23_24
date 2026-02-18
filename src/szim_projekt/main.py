from matplotlib import pyplot as plt
from src.szim_projekt.model import SimulationModel

def main():
    """
    Main function to run the simulation.

    Initializes a `SimulationModel` with predefined parameters for grid size,
    number of agents, step size, number of traps, and special agent configuration.
    Runs the simulation for `t_max` steps and visualizes the data collected.
    """
    height = 100
    width = 100
    number_of_agents = 100
    step_size = 1
    n_traps = 100
    show_path = False
    special_agent_Bence = False
    special_agent_Zoli = False
    special_agent_Zsolt = False

    model = SimulationModel(height=height,
                            width=width,
                            n_agents=number_of_agents,
                            step_size=step_size,
                            n_traps=n_traps,
                            show_path=show_path,
                            special_agent_Bence=special_agent_Bence,
                            special_agent_Zoli=special_agent_Zoli,
                            special_agent_Zsolt=special_agent_Zsolt
                            )

    t_max = 100
    for t in range(0, t_max):
        model.step()

    model_data = model.datacollector.get_model_vars_dataframe()
    model_data.plot()
    plt.show()

if __name__ == '__main__':
    main()
