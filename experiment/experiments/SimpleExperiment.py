from experiment.base.BaseExperiment import BaseExperiment
from environment.world.worlds import KeyPuzzleWorld2,KeyPuzzleWorld,EasyWorld

from agent.agents.DQNAgent import DQNAgent

class SimpleExperiment(BaseExperiment):
    def __init__( self ):
        super(SimpleExperiment,self).__init__()
        self.world = KeyPuzzleWorld.World()
        self.agent = DQNAgent(self.world)
        self.world.link(self.agent,self)
        self.sleep_time = 0.2
        # experiments
        self.epochs = 100
        self.agent.save_epochs = 20
        self.experiment_name = 'good'
        self.load = False
        self.display = False

        # process
        if self.load==True:
            self.display = True
            self.agent.epsilon = 1
            self.agent.learning = False

        if self.display == True:
            self.world.sleep_time = self.sleep_time

        self.load_path = f'./experiment/result/{self.experiment_name}.ckpt'
        self.agent.save_path = self.load_path

    def run( self ):
        if self.load:
            self.agent.load()

        print( 'run tutorial' )

        #tutorial
        self.world.runTutorial()
        print( f"epochs:tutorial,loss:{self.loss:.5f},time={self.time},epsilon={self.agent.epsilon}" )

        # train
        for i in range(1,self.epochs):
            self.world.runOneEpisode()
            print(f"epochs:{i},loss:{self.loss:.5f},time={self.time},epsilon={self.agent.epsilon}")
        # display
        for i in range(self.epochs,self.epochs+50):
            self.display=True
            self.world.sleep_time=self.sleep_time
            self.world.runOneEpisode()
            print( f"epochs:{i},loss:{self.loss},time={self.time}" )


