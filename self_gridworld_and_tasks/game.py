#! /usr/bin/python3
import numpy as np
import time
import os
import sys
import random as rand
import time as t
np.set_printoptions(suppress=True,linewidth=sys.maxsize,threshold=sys.maxsize)

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

class Game():
    def __init__(self,size):
        self.world = np.full(size," ")
        self.size = size
        self.world[[0,self.size[0]-1] ,] = "#"
        self.world[:,[0,self.size[1]-1]] = "#"

        random_locations = [[8,12],[10,7],[17,17]]       
        self.goal = random_locations[rand.randint(0,2)]
        self.world[self.goal[0],self.goal[1]] = "X"
        
        
        self.world[7,10] = "P"
        self.world[8,10] = "P"
        self.world[9,10] = "P"
        self.world[10,10] = "P"
        self.world[11,10] = "P"

        self.world[3,2] = "@"
        self.pos = [3,2]
        self.prev_pos = [3,2]
        print(self.world)
        print(size)

    def move(self, direction):
        
        pitlist = [[7,10],[8,10],[9,10],[10,10],[11,10]]
        self.world[7,10] = "P"
        self.world[8,10] = "P"
        self.world[9,10] = "P"
        self.world[10,10] = "P"
        self.world[11,10] = "P"

        if direction == "w":self.pos[0] -= 1 #here we change the coordinates of our position
        if direction == "s":self.pos[0] += 1
        if direction == "a":self.pos[1] -= 1
        if direction == "d":self.pos[1] += 1
        if (self.pos[0] == 0) or (self.pos[1] == 0):self.pos = self.prev_pos.copy() # we check that the new position is valid, if not then we change it back to previous position
        if (self.pos[0] == self.size[0]-1) or (self.pos[1] == self.size[1]-1):self.pos = self.prev_pos.copy()

        # EXERCISE 7: CREATE A PIT.
        # For my model it was all about luck. Most often it ran straight into the pit,
        # and rarely it got around the pit while even then it was rare for the player to get 
        # to the goal.
        for i in pitlist:
            if self.pos == i:
                self.game_reset()
                return 'Game over'

        goal = np.where(self.world == 'X') #Get the coordinates of the goal 'X'
        print(self.world)
        if (goal[0][0] == self.pos[0]) & (goal[1][0] == self.pos[1]): #check if we reached the goal and reset if we did
            self.game_reset()
            return 'Game over'
        else:
            self.prev_pos = self.pos.copy()
            self.world[self.world == '@'] = " " #here we clear our map and move our character to new position
            self.world[self.pos[0],self.pos[1]] = "@"
            return 'Game not over'

        

    def game_reset(self):
        
        self.pos = [3,2]
        self.world[self.world == '@'] = " "
        self.world[3,2] = "@"
        

        # EXERCISE 6: HAVE THE GOAL BE AT 3 PLACES CHOSEN RANDOMLY.
        # At the start its all about luck, and after that it will have hard time with the goals
        # I set the learning rate to 0.00001 and it started slowly adapting. The furthest goal
        # was always the hardest to find and it didnt find a "use this always" path for it.
        random_locations = [[8,12],[10,7],[17,17]]       
        self.goal = random_locations[rand.randint(0,2)]
        self.world[self.goal[0],self.goal[1]] = "X"


        # EXERCISE 5: HAVE THE GOAL RANDOMLY CHANGE PLACES
        # I am not entirely sure what kind of a reward the model would have had,
        # but it would have been horrible, it took the model a very long time, and even then
        # it wasnt even done. With a random goal everytime, the model depends on luck so 
        # the reward has to be a very bad amount.
        #check_pos = True
        #self.world[self.goal[0],self.goal[1]] = " "
        #MUS = [len(self.world),len(self.world[0])]
        
        #goal_coordinates = [rand.randint(1,(MUS[0]-2)), rand.randint(1,(MUS[1]-2))]
        #while check_pos == True:
        #    if goal_coordinates == self.pos:
        #        goal_coordinates = [rand.randint(1,(MUS[0]-2)), rand.randint(1,(MUS[1]-2))]
        #    else:
        #        check_pos = False

        #self.goal = goal_coordinates
        #self.world[self.goal[0],self.goal[1]] = "X"
        # END OF EXERCISE 5


if __name__ == "__main__":

    grid = Game((20,20))

    while True:

        i = input("dir: ")
        grid.move(i)
        clearConsole()

        print(grid.world)