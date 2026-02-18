from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

import src.epidemic as epidemic

class EpidemicModel(Model):
    def __init__(self,
                 height: int,
                 width: int,
                 n_agents: int):
        super().__init__()
        self.height = height
        self.width = width
        self.n_agents = n_agents

        self.grid = MultiGrid(
            width=self.width,
            height=self.height,
            torus=True
        )
        self.schedule = RandomActivation(model=self)

        for a in range(0, self.n_agents):
            agent = epidemic.EpidemicAgent(unique_id=a,
                                           model=self)
            self.schedule.add(agent=agent)
            x = self.random.randrange(start=0, stop=self.width, step=1)
            y = self.random.randrange(start=0, stop=self.height, step=1)
            self.grid.place_agent(agent=agent,
                                  pos=(x, y))

        agent_infected = self.random.choice(self.schedule.agents)
        agent_infected.state = 1

        self.datacollector = DataCollector(
            model_reporters={
                "Susceptibles": susceptibles, #lambda model: count_states(model=model, state=0),
                "Infected": infected,
                "Recovered": recovered
            }
        )
        self.datacollector.collect(model=self)


    def step(self) -> None:
        self.schedule.step()
        self.datacollector.collect(model=self)



def count_states(model: EpidemicModel,
                 state: int):
    result = 0
    for agent in model.schedule.agents:
        agent: epidemic.EpidemicAgent
        if agent.state == state:
            result += 1
    return result


def susceptibles(model: EpidemicModel):
    return count_states(model=model, state=0)
def infected(model: EpidemicModel):
    return count_states(model=model, state=1)
def recovered(model: EpidemicModel):
    return count_states(model=model, state=2)
