#! /usr/bin/python3
import time as T
import gym
from gym import spaces
from gym.spaces import Box, Dict, Discrete, MultiBinary, MultiDiscrete
import numpy as np
import math
import time as t
import torch
from tensorboardX import SummaryWriter
from game import Game
from stable_baselines3 import PPO

class GridworldEnv(gym.Env):
    def __init__(self,game):
        self.action_space = Discrete(4)

        # EXERCISE 4: INCREASE SIZE TO 25 BY 25. EXPLAIN CONSEQUENCES
        # The area is now bigger by 5x5, so the model will have harder time finding the goal.
        # The reward ended up being -312 with A2C.
        self.observation_space = MultiDiscrete(np.array((25,25)))

        # EXERCISE 8: ADD THE GOAL LOCATION TO OBSERVATIONS
        # I am not sure if this is how its meant to be.
        goal_location = np.array(self.game.goal)
        self.observation_space.goal_location = goal_location
        
        
        
        self.game = game

    def step(self, action):
        info = {}
        reward = 0
        done = False
        game_over = self.game.move(self.do_action(action))
        if game_over == 'Game over':

            reward = 1000
            done = True
            self.reset()
        else: 
            reward = -1
            
        obs = self.game.pos 

        # Return step information

        return obs, reward, done, info
        
        
            

    def reset(self):
        # Reset sim
        self.game.game_reset()
        return self.game.pos, self.game.goal
        

    def do_action(self,action):
        if action == 0:
            return('w')
        if action == 1:
            return('a')
        if action == 2:
            return('s')            
        if action == 3:
            return('d')

from stable_baselines3 import A2C

if __name__ == "__main__":
    env = GridworldEnv(Game((20,20)))
#    model = PPO("MlpPolicy", env, verbose=2)
    # EXERCISE 1: FIND OUT HOW TO VISUALIZE TRAINING PROCESS
    model = A2C("MlpPolicy", env, verbose=1,n_steps=20,gamma=0.85,learning_rate=0.00001,tensorboard_log="./runs")
    

    model.learn(total_timesteps=100000)

# EXERCISE 2: FIND OUT HOW TO SAVE MODEL WITH STABLE BASELINES
model.save("gridworld_path_finder")

# EXERCISE 3: WHAT IS THE MAX REWARD?
# Max reward this time is 984. Code is not by me, I just changed it to fit SB3.
def calculate_reward_func():
    calculate_reward = -np.inf
    for i in range(100):
        ep_reward = 0
        done = False
        state = env.reset()
        while not done:
            action, _ = model.predict(state)
            state, reward, done, _ = env.step(action)
            ep_reward += reward
        max_reward = max(calculate_reward, ep_reward)
    print(max_reward)
calculate_reward_func()
print("DONE")
