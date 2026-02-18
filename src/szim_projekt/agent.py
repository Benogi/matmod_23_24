#
from mesa import Agent
import src.szim_projekt as simulation


class SimulationAgent(Agent):
    """
    A class representing an agent in the simulation.

    This class handles the agent's movement, tracking of status attributes (e.g., moving,
    returned, trapped), and interaction with the grid.

    Attributes:
        special_agent_ids (list): IDs of special agents.
        distance (float): Distance traveled by the agent.
        moving (bool): Whether the agent is currently moving.
        returned (bool): Whether the agent has returned to the home.
        trap (bool): Whether the agent is in a trap.
        trapped (bool): Whether the agent is trapped.
        home (bool): Whether the agent is at home.
        special_agent (bool): Whether the agent is a special agent.
        path_marker (bool): Whether the agent is a path marker.

    Methods:
        __init__: Initializes the agent with default attributes.
        step: Moves the agent if it is active.
        move: Moves the agent to a new position on the grid.
    """

    special_agent_ids = [1, 7, 42]

    def __init__(self, model, unique_id):
        """
        Initializes a new agent.

        Args:
            model: The simulation model instance.
            unique_id: Unique identifier for the agent.
        """
        super().__init__(model=model, unique_id=unique_id)
        self.distance = 0
        self.moving = True
        self.returned = False
        self.trap = False
        self.trapped = False
        self.home = False
        self.special_agent = False
        self.path_marker = False

    def step(self):
        """
        Executes the agent's actions for the current step.

        If the agent is moving, it calls the move method to update its position.
        """
        if self.moving:
            self.move()

    def move(self):
        """
        Moves the agent to a new position on the grid.

        The agent selects a neighboring cell based on the model's step size and
        randomly moves to one of the neighboring cells, updating its position.
        """
        self.model: simulation.SimulationModel
        cells_to_move = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=self.model.step_size,
        )
        destination_cell = self.model.random.choice(cells_to_move)
        self.model.grid.move_agent(agent=self, pos=destination_cell)
