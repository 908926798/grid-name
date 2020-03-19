import time

class BaseExperiment():
    def __init__( self):
        self.sleep_time = 0
        self.loss = None

    def run( self ):
        for  epoch in range(self.epochs):
            self.world.step()
            time.sleep(self.sleep_time)