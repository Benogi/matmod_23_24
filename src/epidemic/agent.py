from mesa import Agent

import src.epidemic as epidemic


class EpidemicAgent(Agent):
    def __init__(self, model, unique_id):
        super().__init__(model=model,
                         unique_id=unique_id)
        #self.unique_id = unique_id
        # 0: Susceptible
        # 1: Infected & Infectious
        # 2: Recovered
        self.state = 0

    def step(self):
        self.move()
        self.action()

    def move(self):
        self.model: epidemic.EpidemicModel
        cells_to_move = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False,
            radius=4,
        )
        destination_cell = self.model.random.choice(cells_to_move)
        self.model.grid.move_agent(agent=self,
                                   pos=destination_cell)

    def action(self):
        self.infect()
        self.recover()

    def infect(self):
        self.model: epidemic.EpidemicModel
        infection_threshold = 0.8
        if self.state == 1:
            agents_in_same_cell = self.model.grid.get_cell_list_contents(
                [self.pos]
            )
            for agent in agents_in_same_cell:
                if agent.state == 0:
                    if self.model.random.random() < infection_threshold:
                        agent.state = 1


    def recover(self):
        recovering_days = 10
        if self.state == 1:
            if self.model.random.random() < 1 / recovering_days:
                self.state = 2

