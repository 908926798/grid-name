import numpy as np
import time
from environment.world.base.BaseWorld import BaseWorld
from environment.world.base.BaseItem import *

class Key( Item ):
    def __init__( self ):
        super( Key, self ).__init__()
        self.looks_like=2

    def touched( self ):
        self.world.key_num += 1
        self.grid.contents.remove(self)
        return True

class Door():
    def __init__( self):
        super( Door, self ).__init__( )
        self.looks_like=3

    def touched( self ):
        if self.world.key_num <2:
            return False
        self.world.door_opened = True
        self.grid.contents.remove(self)
        return True

class World( BaseWorld ):
    def __init__( self ):
        super( World, self ).__init__()
        self.X=3
        self.Y=4
        # agent
        self.agent=None
        self.act_space_length=4  # (left,up,right,down)
        self.obs_space_length=self.X*self.Y
        self.agent_start_pos=(1, 0)
        #experiment
        self.experiment = None



    def _reset( self ):
        # enviroment
        self.grids=[[Grid( (x, y), self ) for y in range( self.Y )] for x in range( self.X )]
        self.grids[0][1].addContent( Key() )
        self.grids[2][1].addContent( Key() )
        self.grids[1][3].addContent( Door() )
        # agent
        x, y=self.agent_start_pos
        self.agent.pos = self.agent_start_pos
        self.grids[x][y].contents.append( self.agent )
        # rule
        self.key_num = 0
        self.door_opened = False
        self.episode_end = False

    def getObs( self, agent ):
        obs=[]
        for raw_grid in self.grids:
            for grid in raw_grid:
                obs.append( grid.contents[0].looks_like if grid.contents!=[] else 0 )
        return obs

    def runTutorial( self ):
        self._reset()
        self.agent._reset()
        if self.experiment.display:
            self.render()

        def tutorial_choose_action( world ):
            # find key
            for raw_grids in world.grids:
                for grid in raw_grids:
                    for item in grid.contents:
                        if item.looks_like==2:
                            dx=grid.pos[0]-world.agent.pos[0]
                            if dx > 0: return [0, 0, 1, 0]
                            if dx < 0: return [1, 0, 0, 0]
                            dy=grid.pos[1]-world.agent.pos[1]
                            if dy > 0: return [0, 1, 0, 0]
                            if dy < 0: return [0, 0, 0, 1]
                            assert 1!=1
            # find door
            for raw_grids in world.grids:
                for grid in raw_grids:
                    for item in grid.contents:
                        if item.looks_like==3:
                            dx=grid.pos[0]-world.agent.pos[0]
                            if dx > 0: return [0, 0, 1, 0]
                            if dx < 0: return [1, 0, 0, 0]
                            dy=grid.pos[1]-world.agent.pos[1]
                            if dy > 0: return [0, 1, 0, 0]
                            if dy < 0: return [0, 0, 0, 1]
                            assert 1!=1


        while self.episode_end==False:
            act=tutorial_choose_action( self )
            self.agent.step(act=act)
            if self.experiment.display:
                self.render()

        self.agent.episodeEnd()
        self.experiment.loss=self.agent.loss.result().numpy()
        self.experiment.time=self.agent.time

    def step( self, agent, act ):
        x, y = new_x,new_y =agent.pos
        # move
        if act[0]==1: new_x-=1
        if act[1]==1: new_y+=1
        if act[2]==1: new_x+=1
        if act[3]==1: new_y-=1

        if new_x >= 0 and new_x < self.X and new_y >= 0 and new_y < self.Y:
            can_go = True
            for item in self.grids[new_x][new_y].contents:
                if not item.touched():
                    can_go = False
                    break

            if can_go:
                self.grids[x][y].contents.remove( agent )
                self.grids[new_x][new_y].contents.append( agent )
                agent.pos = (new_x,new_y)

        rew = 0
        if self.door_opened:
            rew = 1
            self.episode_end = True

        return rew,self.episode_end
