This repository contains helping code that has been written in different projects. 


# util.py
This file contains basic IO and augmentation codes for image. 


# keras custom batch_generator
This is custom bach generator, could be used for any keras code

# keras custom callback
Contains sample callback codes 

GlobalSumPooling2D: Keras has GlobalMaxPooling2D class which has modified here for sum pooling. 

# save_prediction: 
This class is used as class_back function in autoencoder or Transfer learning models where we input some image and get image in output. To save generation on each epoch, for example, add the class in the list of class_back functions for model training. 
Parameters: 
batch_generator = object of batch generator function  
name: The name of the result files you want to save
encoder, decoder: These are model/s that can be used for generation 
path='' : The path  where you want to save result files

Note: Replace batch_generator with images, instead of encoder/decoder use own model, you are ready to go.

