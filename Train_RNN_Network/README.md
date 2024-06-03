# Character-Level RNN for Name Classification

This document provides an overview of the implementation of a character-level Recurrent Neural Network (RNN) for classifying names by their origin. The script trains the RNN on a dataset of names from different languages and evaluates its performance.

---

## Overview
The goal is to classify names into their respective languages using an RNN. The RNN processes each character of a name sequentially and learns patterns that are indicative of different languages.

## Key Steps:
1. **Data Preparation**:
   - **Input Data**: Read and preprocess the names from text files, converting Unicode strings to ASCII.
   - **Data Splitting**: Split the names into training (70%), validation (20%), and test (10%) sets for each category (language).

2. **Model Definition**:
   - **RNN Architecture**: Define an RNN with an input layer, a hidden layer, and an output layer. The hidden state is updated at each time step as the RNN processes each character of the name.

3. **Training**:
   - **Training Loop**: Train the model using the training set. Track the loss and periodically print the training progress.
   - **Validation**: Evaluate the model on the validation set every 1000 iterations. Save the model if it achieves the best validation loss observed so far.

4. **Hyperparameter Tuning**:
   - **Different Configurations**: Train the model with different hyperparameters such as the number of iterations, learning rate, and the number of neurons in the hidden layer.
   - **Multiple Runs**: Perform multiple runs (10 times) for each set of hyperparameters to ensure robust results.

5. **Evaluation**:
   - **Test Set Evaluation**: After training, evaluate the best model on the test set to check its accuracy.
   - **Average Accuracy**: Calculate the average accuracy across different runs and hyperparameter configurations.

## Example Output:
During training, the script periodically prints the current iteration, elapsed time, loss, the name being processed, the most likely class predicted by the model, and the correct label. Validation accuracy and loss are also printed every 1000 iterations. The best model is saved based on the lowest validation loss.

iterations5000 5% time:5m 24s loss: 2.0548 line:Kumar most likely class:2 correct label:2
Validation loss: 1.9034, Validation accuracy: 0.4764

