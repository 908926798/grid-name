import numpy as np
import tensorflow as tf

from tensorflow_core.python.keras import Sequential,Model
from tensorflow_core.python.keras.layers import Dense, Flatten, Conv2D,concatenate,Input,Activation

from agent.agents.base.BaseAgent import BaseAgent,DataBase

class DQNAgent(BaseAgent):
    def __init__( self ,world):
        super(DQNAgent, self).__init__(world)
        self.model_changing = None
        self.model_stable = None
        self.batch_size = 1000
        self.optimizer=tf.keras.optimizers.RMSprop(0.00005)
        self.loss_object=tf.math.squared_difference
        self.loss = tf.keras.metrics.Mean()
        self.epochs = 0
        self.time_update_stable_model = 100 #time_update_stable_model
        self.gamma = 0.8
        self.epsilon = 0.3
        self.epsilon_increase_factor = 1.02
        self.epsilon_max = 0.99
        self.learning = True

    def _reset( self ):
        self.time = 0
        self.loss.reset_states()

    def createNetwork( self ):
        input1 = Input(shape=(self.obs_space_length,))
        d1 = Dense(units=32,batch_size=self.batch_size,activation='relu')(input1)
        d2 = Dense(units=32,batch_size=self.batch_size,activation='relu')(d1)
        output1 = Dense(units=self.act_space_length,batch_size=self.batch_size,activation='softmax')(d2)

        model = Model(inputs=input1,outputs=output1)
        return model

    def copyWeight( self ):
        model_stable_layers=self.model_changing.layers
        for i,layers in enumerate( self.model_stable.layers ):
            layers.set_weights( model_stable_layers[i].get_weights() )

    def initialize( self ):
        #database
        self.database = DataBase(self.obs_space_length*2+self.act_space_length+1)

        tf.keras.backend.set_floatx( 'float64' )
        self.model_changing = self.createNetwork()
        self.model_stable = self.createNetwork()
        self.copyWeight()

    def load( self ):
        self.model_changing.load_weights(self.save_path)
        self.model_stable.load_weights(self.save_path)

    def step( self, act = None):
        obs=self.observe()
        # react to observation
        act=self.choose_action( obs ) if act is None else act
        rew,end=self.world.step( self, act )
        # learning
        self.database.store( [obs, act, rew,obs] , end=end )
        # print(self.model_changing(np.array([obs])))
        self.time += 1
        if self.learning and self.database.size >= self.batch_size:
            data=self.database.sample( self.database.size )
            self.train( data )


    def choose_action( self, obs ):
        if np.random.uniform() <= self.epsilon:
            # forward feed the observation and get q value for every actions
            index = np.argmax( self.model_changing(np.array([obs])))
        else:
            index = np.random.choice(self.act_space_length)

        act = np.zeros(self.act_space_length)
        act[index] = 1
        return act

    def episodeEnd( self ):
        # train
        if self.epsilon * self.epsilon_increase_factor < self.epsilon_max:
            self.epsilon *= self.epsilon_increase_factor
        else:
            self.epsilon = self.epsilon_max

        # np.savetxt( "a.csv", self.database_test.data, delimiter=',' )

        self.epochs += 1
        if self.epochs % self.save_epochs ==0:
            self.model_changing.save_weights(self.save_path)
            print(self.save_path)
            print('模型已保存')


    def train( self ,data):
        obs_batch,rew_target_batch = self.train_preprocess( data )
        self.train_learn(obs_batch,rew_target_batch)

        if self.time % self.time_update_stable_model ==0:
            self.copyWeight()

    def train_preprocess( self,data ):
        obs_batch=data[:, :self.obs_space_length]
        act_batch=data[:, self.obs_space_length:self.obs_space_length+self.act_space_length]
        act_index_batch=np.argmax( act_batch, axis=1 )

        obs_next_batch=data[:, -self.obs_space_length:]
        rew_real_batch=data[:, self.obs_space_length+self.act_space_length]
        # print(obs_next_batch)
        rew_target_batch=self.model_changing( obs_batch ).numpy()
        rew_next_batch=self.model_stable( obs_next_batch ).numpy()

        rew_target_batch[np.arange(self.database.size), act_index_batch]=rew_real_batch+self.gamma*np.max( rew_next_batch, axis=1 )

        return obs_batch,rew_target_batch

    @tf.function(experimental_relax_shapes=True)
    def train_learn( self,obs_batch,rew_target_batch ):
        with tf.GradientTape() as tape:
            rew_pred_batch=self.model_changing( obs_batch )
            loss=self.loss_object( rew_target_batch , rew_pred_batch )
            # print(loss)
        gradients=tape.gradient( loss, self.model_changing.trainable_variables )
        self.optimizer.apply_gradients( zip( gradients, self.model_changing.trainable_variables ) )

        self.loss(loss)
        # train_accuracy( accuracy_object( labels, predictions ) )

