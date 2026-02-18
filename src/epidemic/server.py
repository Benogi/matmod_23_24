from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import mesa.visualization

import src.epidemic as epidemic


def epi_model_portrayal(person):
    if person is None:
        return

    portrayal = {}
    if person.state == 0:  # 0 = Susceptible
        portrayal["Shape"] = "pics/susc.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
    elif person.state == 1:  # 1 = Infected
        portrayal["Shape"] = "pics/inf.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
    elif person.state == 2:  # 2 = Recovered
        portrayal["Shape"] = "pics/rec.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 0
    return portrayal


canvas_element = CanvasGrid(epi_model_portrayal, 15, 15, 500, 500)

model_params = {
    "height": 15,
    "width": 15,
    "n_agents": mesa.visualization.Slider("Nr of agents", #name
                                          100, #value (default)
                                          10, #min_value
                                          100, #max_value
                                          1) #step
}

server = ModularServer(
    epidemic.EpidemicModel, [canvas_element], "Simple SIR epidemic", model_params
)
