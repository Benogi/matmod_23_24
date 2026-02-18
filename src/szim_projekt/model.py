#
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import numpy as np

import src.szim_projekt as simulation


class SimulationModel(Model):
    """
    A class to represent the simulation model.

    This model simulates agents, special agents, traps, and a home base
    within a grid. It tracks agent movement, calculates distances, and
    collects data for analysis.

    Methods:
        __init__: Initializes the simulation model.
        step: Advances the simulation by one step.
        datacollector: Gather and report various statistics about the simulation,
        such as the number of returned agents, average distances, and other metrics related to
        agent movement and status.
    """

    def __init__(self,
                 height: int,
                 width: int,
                 n_agents: int,
                 step_size: int,
                 n_traps: int,
                 show_path: bool = False,
                 special_agent_Bence: bool = False,
                 special_agent_Zoli: bool = False,
                 special_agent_Zsolt: bool = False):
        """
        Initializes the simulation model with specified parameters.

        Args:
            height (int): The height of the grid.
            width (int): The width of the grid.
            n_agents (int): The number of agents to create.
            step_size (int): The step size for agent movement.
            n_traps (int): The number of traps to place on the grid.
            show_path (bool, optional): If True, show agent paths. Defaults to False.
            special_agent_Bence (bool, optional): If True, include special agent Bence.
            special_agent_Zoli (bool, optional): If True, include special agent Zoli.
            special_agent_Zsolt (bool, optional): If True, include special agent Zsolt.
        """
        super().__init__()
        #Other model variables
        self.n_agents = n_agents
        self.step_size = step_size
        self.n_traps = n_traps
        self.first_step_done = False
        self.total_returned_agents = 0
        self.simulation_message = ""

        # Special agent behaviour
        self.show_path = show_path
        self.special_agents_paths = {
            a: [] for a in simulation.SimulationAgent.special_agent_ids
        }
        self.special_agent_Bence = special_agent_Bence
        self.special_agent_Zoli = special_agent_Zoli
        self.special_agent_Zsolt = special_agent_Zsolt

        # Defining the grid
        self.height = height
        self.width = width
        self.center = (int(self.width / 2), int(self.height / 2))
        self.grid = MultiGrid(width=self.width, height=self.height, torus=True)
        self.schedule = RandomActivation(model=self)

        # Creating agents and objects
        generate_moving_agents(model=self)
        generate_special_agents(model=self)
        self.traps = generate_traps(model=self)
        create_home(model=self)

        # DataCollector
        self.datacollector = DataCollector(
            model_reporters={
                "Returned Agents": count_returned_agents,
                "Average X Distance": lambda model: avg_distance(
                    distance_method=euclid_x_distance, model=model),
                "Average Y Distance": lambda model: avg_distance(
                    distance_method=euclid_y_distance, model=model),
                "Average Distance": lambda model: avg_distance(
                    distance_method=euclidean_distance, model=model),
                "Agents Trapped": trapped_agents,
                "Agents Still Moving": count_moving_agents
            }
        )
        self.datacollector.collect(model=self)

    def step(self) -> None:
        """
        Advances the simulation by one step, updating agent actions and
        collecting data.

        This method executes one step in the simulation, checks if all
        special agents are trapped, and collects data for the model.
        """
        if not self.first_step_done:
            self.first_step_done = True

        marking_path(model=self, show_path=self.show_path)
        check_special_agent_status(model=self)
        check_moving_agent_status(model=self)

        self.schedule.step()
        self.datacollector.collect(model=self)


# Functions for agent and trap generation, path marking, and behaviour

def core_agent_generator(model: SimulationModel, unique_id: int, pos: tuple[int, int], **kwargs):
    """
    Generates an agent and adds it to the simulation model.

    Args:
        model (SimulationModel): The simulation model instance.
        unique_id (int): Unique ID for the agent.
        pos (tuple): Initial position of the agent.
        kwargs: Additional attributes for the agent.

    Returns:
        simulation.SimulationAgent: The created agent.
    """
    agent = simulation.SimulationAgent(unique_id=unique_id, model=model)
    model.schedule.add(agent)
    model.grid.place_agent(agent, pos)

    for attr, value in kwargs.items():
        setattr(agent, attr, value)

    return agent


def generate_moving_agents(model: SimulationModel):
    """Generate common moving agents, excluding special agents."""
    # Calculate the number of active special agents
    active_special_agents = sum([
        model.special_agent_Bence,
        model.special_agent_Zoli,
        model.special_agent_Zsolt
    ])
    # Ensure total agents match n_agents
    num_common_agents = model.n_agents - active_special_agents

    # Generate only the necessary number of common agents
    for a in range(1, num_common_agents + 1):
        core_agent_generator(
            model=model,
            unique_id=a,
            pos=model.center
        )


def generate_special_agents(model: SimulationModel):
    """Generate special agents based on model configuration."""
    special_agents_config = {
        simulation.SimulationAgent.special_agent_ids[0]: model.special_agent_Bence,
        simulation.SimulationAgent.special_agent_ids[1]: model.special_agent_Zoli,
        simulation.SimulationAgent.special_agent_ids[2]: model.special_agent_Zsolt
    }

    for special_id, is_enabled in special_agents_config.items():
        if is_enabled:
            core_agent_generator(
                model=model,
                unique_id=special_id,
                pos=model.center,
                special_agent=True
            )
            model.special_agents_paths[special_id] = []

def generate_traps(model: SimulationModel):
    """Generates traps and places them on the grid."""
    traps = []
    occupied_positions = set()

    for a in range(0, model.n_traps):
        while True:
            x, y = model.random.randint(0, model.width - 1), model.random.randint(0, model.height - 1)
            if (x, y) != model.center and (x, y) not in occupied_positions:
                trap = core_agent_generator(
                    model=model,
                    unique_id=a + model.n_agents + 1,
                    pos=(x, y),
                    trap=True,
                    moving=False
                )
                traps.append(trap)
                occupied_positions.add((x, y))
                break

    return traps


def create_home(model: SimulationModel):
    """Creates the home base at the center of the grid."""
    core_agent_generator(model=model, unique_id=0, pos=model.center, home=True, moving=False)


def marking_path(model: SimulationModel, show_path):
    """Marks the path of special agents on the grid if show_path is True."""
    if not show_path:
        return

    for agent in model.schedule.agents:
        if agent.special_agent:
            model.special_agents_paths[agent.unique_id].append(agent.pos)

            if len(model.special_agents_paths[agent.unique_id]) > 1:
                last_position = model.special_agents_paths[agent.unique_id][-1]

                path_agent = simulation.SimulationAgent(model=model, unique_id=agent.unique_id + 10000)
                path_agent.pos = last_position
                path_agent.special_agent = False
                path_agent.path_marker = True
                path_agent.moving = False
                model.schedule.add(path_agent)
                model.grid.place_agent(path_agent, last_position)


def check_special_agent_status(model: SimulationModel):
    """Checks if all special agents are trapped and stops the simulation if so."""
    all_special_agents_trapped = all(agent.trapped for agent in model.schedule.agents
                                     if agent.special_agent)

    if any([model.special_agent_Bence, model.special_agent_Zoli,
            model.special_agent_Zsolt]) and all_special_agents_trapped:
        model.simulation_message = "All special agents are trapped. Stopping simulation."
        print(model.simulation_message)
        model.running = False

def check_moving_agent_status(model: SimulationModel):
    """Checks if all special agents are trapped and stops the simulation if so."""
    all_agents_trapped = all(agent.trapped for agent in model.schedule.agents
                             if not (agent.trap or agent.home or agent.path_marker))

    if all_agents_trapped:
        model.simulation_message = "All agents are trapped. Stopping simulation."
        print(model.simulation_message)
        model.running = False


def trapped_agents(model: SimulationModel):
    """Freezes agents that step into a trap."""
    trapped = 0
    for agent in model.schedule.agents:
        for trap in model.traps:
            if agent.pos == trap.pos and not agent.trap and not agent.path_marker:
                agent.moving = False
                agent.trapped = True
                trapped += 1
    return trapped


def count_moving_agents(model: SimulationModel):
    """Counts how many agents are still moving."""
    moving_agents = sum(1 for agent in model.schedule.agents if agent.moving)
    return moving_agents

def count_returned_agents(model: SimulationModel) -> int:
    """
    Counts the number of agents that have returned to the center.

    An agent is counted only the first time it reaches the center. Once it is marked as
    returned, it will not be counted again, even if it leaves and returns to the center.
    """
    returned_count = 0

    if model.first_step_done:
        for agent in model.schedule.agents:
            if agent.pos == model.center and not agent.home and not agent.returned:
                returned_count += 1
                agent.returned = True  # Mark agent as returned

    model.total_returned_agents += returned_count  # Add to the cumulative total
    return model.total_returned_agents


def euclidean_distance(pos1: tuple, pos2: tuple) -> float:
    """
    Returns the Euclidean distance between two positions.
    """
    return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def euclid_x_distance(pos1: tuple, pos2: tuple) -> float:
    """
    Returns the Euclidean distance in the x direction.
    """
    return np.sqrt((pos1[0] - pos2[0]) ** 2)


def euclid_y_distance(pos1: tuple, pos2: tuple) -> float:
    """
    Returns the Euclidean distance in the y direction.
    """
    return np.sqrt((pos1[1] - pos2[1]) ** 2)


def avg_distance(distance_method, model: SimulationModel) -> float:
    """
    Returns the average distance of moving or trapped agents from the center.
    """
    total_distance = 0
    num_relevant_agents = 0

    for agent in (a for a in model.schedule.agents if a.moving or a.trapped):
        total_distance += distance_method(agent.pos, model.center)
        num_relevant_agents += 1

    return total_distance / num_relevant_agents if num_relevant_agents > 0 else 0





