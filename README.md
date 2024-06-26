# "90percent_predictionAccuracy_keras.html"
School assignment done with tensorflow with Python in Jupyter Lab (hence the .html file) 
Please download the file to see output, or open the "90percent_predictionAccuracy_keras.py" in GitHub to see the code

Assignment was to make a network that learns from fminst dataset and can predict 10 categories. Extra task was to make it better than 80% test accuracy while not using test set in training. Only dense and dropout layers were allowed. 


# neural_networks folder
Examples of a self created neural networks with Torch and an image of what it looks like


# self_gridworld folder
Self created gridworld with multiple different tasks completed by myself. 
Tasks included:
1. Use tensorboard to visualize the training process 
2. Find out how to save a model with stable baselines
3. What is the max reward in the default environment? How long does it take to achieve it
4. Increase the size of the game area to 25 by 25 and train the agent again, how long does the training take after increasing the size? What is the maximum reward now and why?
5. Have the goal randomly change positions after each reset to a place that is not the starting position of the character "@" or a wall "#". What is happening? What happened to average reward and why?
6. Have the goal randomly be at one of three locations, [8,12] [10,7] [17,17],  after each reset. What is the maximum reward? What kind of path is the agent taking now
7. Make a "pit" that is 5 squares long between two goal positions. If the character steps into the pit, reset game
8. Add the location of the goal to the observations


# style_transfer folder
Includes
1. A copy of my "to image style transfer" from colab using tensorflow with Python.
2. Image examples for proof

Code takes 2 folders from given parameters. In them are
1. Styles, example. Vincent van Gogh's "Starry Night" or random picked abstract art
2. Self-chosen images to be transferred styles to


# SQLAlchemy_Python_Engine folder
A school assignment where the task was to create a simple DBMS using SQLAlchemy with SQLite as the engine


# FinalTask folder
Object Oriented Programming C# final task. Simplified version of Trick-taking game. 
Fully functional game with screen clear user interface (in terminal that is). 
Many requirements are listed in the .PDF file.


# Train_RNN_Network
Train a RNN model to predict which class and name is most fit. 
Given tasks were:
 - split 70% to train and 20 % for validation and 10 % test set, take first lines 70 % from each category to train set, 20 % next to validation set, and last items to test set.
 - validate the model every 1000 iterations, and save the best model, over writing the previous best
 - Teach network with different hyper parameters: number of iterations, learning rate, number of neurons in hidden layer, at least 10 different combinations, using train set.
 - Run teaching with each parameters 10 times, test check accuracy with test set and calculate average accuracy with each parameters.


# LSTM_predict_underwater
A group project to predict future sonar images from under water using LSTM's.
My role was to create and tune the extraction tool inside the folder. The final product:
- Took out 100 images (can be changed by the user) through multiple .csv files.
- matched it up with the speed (data located in _speed.csv) and paired it up with 'cog', 'sog' and 'timestamp' from the topics_combined.csv
- At the end a graph is shown with possible outcomes
