import numpy as np
class DataBase():
    def __init__( self,exp_length ):
        self.SIZE = 100000
        self.exp_length = exp_length
        self._reset()

    def store(self,d,end):
        if self.buffer == None:
            self.buffer = d
            return
        if end:
            self.buffer = None
            self.data[self.cur, :] = np.hstack(d)
        else:
            self.buffer[3]=d[0]
            self.data[self.cur,:] = np.hstack(self.buffer)
            self.buffer = d

        self.cur = (self.cur+1) % self.SIZE
        if self.size < self.SIZE:
            self.size += 1

    def _reset( self ):
        self.data = np.zeros((self.SIZE,self.exp_length))
        self.size = 0
        self.cur = 0
        self.buffer = None

    def sample( self,batch_size):
        sample_index = np.random.choice( self.size, batch_size )
        s = self.data[sample_index,:]
        return s

class BaseAgent():
    def __init__( self,world):
        self.time = 0
        self.pos = None
        self.geom = None
        self.world = world
        self.looks_like = 1
        self.save_epochs = None
        self.save_path = None

        self.act_space_length = None
        self.obs_space_length = None
        self.loss = None
        self.database = None

    def initialize( self ):
        raise NotImplementedError

    def observe( self ):
        return self.world.getObs(self)

    def choose_action( self ):
        raise NotImplementedError

    def train( self ):
        raise NotImplementedError


