import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

#Look for available gpus
tf.config.list_physical_devices('GPU')

#load mnist dataset
fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images,test_labels) = fashion_mnist.load_data()

#def class names for dataset
class_names = ['T-shirt/top','Sneakers','Pullover','Dress','Sandals','Coat','Shirt','Trousers','Ankle boot','Bag']

#normalize image data to values between 0 and 1
renew_count = 255.0
train_images = train_images / renew_count
test_images = test_images / renew_count

# make neural network model
prediction_model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape = (28,28)), 
    tf.keras.layers.Dropout(0.2), 
    tf.keras.layers.Dense(500,activation = 'sigmoid'), 
    tf.keras.layers.Dropout(0.25), 
    tf.keras.layers.Dense(128,activation = 'relu'), 
    tf.keras.layers.Dense(10,activation = 'softmax')])

# Setup the optimizer and early stop
sgd=tf.keras.optimizers.SGD(learning_rate = 0.013,momentum = 0.9, nesterov = True)
es = tf.keras.callbacks.EarlyStopping(monitor = 'acc', mode = 'min', verbose = 2, patience = 0)

prediction_model.compile(optimizer = sgd, loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True), metrics = ['accuracy'])
prediction_model.summary()

# training here
prediction_model_information = prediction_model.fit(train_images, train_labels, epochs = 130, batch_size = 28, verbose=2, validation_data = (test_images, test_labels))

print(prediction_model.evaluate(train_images, train_labels))

# Evaluate, save and load
test_loss,test_acc = prediction_model.evaluate(test_images, test_labels, verbose = 2)
prediction_model.save('90_percent_acc_model.h5')
updated_prediction_model = tf.keras.models.load_model('90_percent_acc_model.h5')


