import time

# multi-agent environment
class BaseWorld(object):
    def __init__(self):
        self.episode_end = False
        self.display = False
        self.viewer = None
        self.sleep_time = 0

    # update state of the environment
    def step(self):
        pass
        #agent do actions
        # for i, agent in enumerate(self.agents):
        #     agent.do_actions(self)

    def link( self, agent ,experiment):
        # agent
        agent.act_space_length = self.act_space_length
        agent.obs_space_length=self.obs_space_length
        agent.initialize()
        self.agent=agent

        #experiment
        self.experiment = experiment

    def runOneEpisode( self ):
        self._reset()
        self.agent._reset()
        if self.experiment.display:
            self.render()

        while self.episode_end == False:
            self.agent.step()
            if self.experiment.display:
                self.render()

        self.agent.episodeEnd()
        self.experiment.loss = self.agent.loss.result().numpy()
        self.experiment.time = self.agent.time

    def runTutorial( self ):
        pass

    def render( self ):
        from environment.display.viewers.GridViewer import GridViewer
        if self.viewer == None:
            self.viewer=GridViewer( self.X, self.Y, self )

        self.viewer.render()
        time.sleep( self.sleep_time )
