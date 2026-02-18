
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import mesa.visualization
import src.szim_projekt as simulation


def model_portrayal(obj):
    """
    Defines how the agents and other objects in the simulation are portrayed on the grid.

    Args:
        obj: The object (agent, trap, home, etc.) to portray.

    Returns:
        portrayal (dict): A dictionary defining the visual properties of the object.
    """
    if obj is None:
        return

    portrayal = {}

    # Handle agents that are not traps, special agents, or path markers
    if isinstance(obj, simulation.SimulationAgent) and not (
            obj.trap or obj.special_agent or obj.path_marker):

        if obj.moving:
            portrayal["Shape"] = "pics/susc.png"
            portrayal["scale"] = 1
            portrayal["Layer"] = 1
        if obj.trapped:
            portrayal["Shape"] = "pics/inf.png"
            portrayal["scale"] = 1
            portrayal["Layer"] = 3
        if obj.returned and obj.moving:
            portrayal["Shape"] = "pics/rec.png"
            portrayal["scale"] = 1
            portrayal["Layer"] = 2

    # Handle traps (light red cells)
    if isinstance(obj, simulation.SimulationAgent) and obj.trap:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "rgba(255, 0, 0, 0.25)"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    # Handle home (blue cell)
    if isinstance(obj, simulation.SimulationAgent) and obj.home:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "rgba(0, 0, 255, 1)"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 9
        portrayal["w"] = 1
        portrayal["h"] = 1

    # Handle special agents and their paths
    special_agents_info = {
        obj.special_agent_ids[0]: {
            "shape": "pics/bence.png", "color": "rgba(144, 20, 144, 0.1)", "layer": 5},  # Bence
        obj.special_agent_ids[1]: {
            "shape": "pics/zoli.png", "color": "rgba(20, 200, 20, 0.1)", "layer": 5},  # Zoli
        obj.special_agent_ids[2]: {
            "shape": "pics/zsolt.png", "color": "rgba(20, 20, 200, 0.1)", "layer": 5}  # Zsolt
    }

    if isinstance(obj, simulation.SimulationAgent) and obj.special_agent:
        agent_info = special_agents_info.get(obj.unique_id)
        if agent_info:
            portrayal["Shape"] = agent_info["shape"]
            portrayal["scale"] = 3
            portrayal["Layer"] = agent_info["layer"]

    # Handle path markers with different colors for each special agent's path
    if isinstance(obj, simulation.SimulationAgent) and obj.path_marker:
        agent_info = special_agents_info.get(
            obj.unique_id - 10000)  # Offset by 10000 for path agents
        if agent_info:
            portrayal["Shape"] = "rect"
            portrayal["Color"] = agent_info["color"]
            portrayal["Filled"] = "true"
            portrayal["Layer"] = 4
            portrayal["w"] = 1
            portrayal["h"] = 1

    # Display the message if it's set
    if isinstance(obj, simulation.SimulationAgent) and hasattr(obj.model, "simulation_message") and obj.home:
        message = obj.model.simulation_message
        if message:
            # Show "gameoverr.png" if any special agents are active
            if any([
                obj.model.special_agent_Bence,
                obj.model.special_agent_Zoli,
                obj.model.special_agent_Zsolt
            ]):
                portrayal["Shape"] = "pics/gameoverr.png"
            else:  # Otherwise, show the regular "gameover.png"
                portrayal["Shape"] = "pics/gameover.png"
            portrayal["scale"] = 30
            portrayal["Layer"] = 10

    return portrayal


visualization_elements = [
    CanvasGrid(
        model_portrayal,
        grid_width=100,
        grid_height=100,
        canvas_width=1000,
        canvas_height=1000
    ),
    ChartModule(
        series=[{"Label": "Average Distance", "Color": "Green"},
                {"Label": "Average X Distance", "Color": "Black"},
                {"Label": "Average Y Distance", "Color": "Grey"}],
        data_collector_name="datacollector",
        canvas_height=200,
        canvas_width=500
    ),
    ChartModule(
        series=[{"Label": "Returned Agents", "Color": "Blue"}],
        data_collector_name="datacollector",
        canvas_height=200,
        canvas_width=500
    ),
    ChartModule(
        series=[{"Label": "Agents Trapped", "Color": "Red"},
                {"Label": "Agents Still Moving", "Color": "Green"}],
        data_collector_name="datacollector",
        canvas_height=200,
        canvas_width=500
    )
]

model_params = {
    "height": 100,
    "width": 100,
    "step_size": mesa.visualization.Slider(
        name="Step size", value=1, min_value=1, max_value=10, step=1),
    "n_agents": mesa.visualization.Slider(
        name="Number of agents", value=100, min_value=1, max_value=1000, step=10),
    "n_traps": mesa.visualization.Slider(
        name="Number of Traps", value=100, min_value=0, max_value=1000, step=10),
    "show_path": mesa.visualization.Checkbox(
        name="Show Path of Special Agents", value=False),
    "special_agent_Bence": mesa.visualization.Checkbox(
        name="Activate special agent Bence", value=False),
    "special_agent_Zoli": mesa.visualization.Checkbox(
        name="Activate special agent Zoli", value=False),
    "special_agent_Zsolt": mesa.visualization.Checkbox(
        name="Activate special agent Zsolt", value=False),
}

# Initialize and run the server
server = ModularServer(
    model_cls=simulation.SimulationModel,
    visualization_elements=visualization_elements,
    name="360 Random Walk",
    model_params=model_params
)
