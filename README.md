This repository contains helping code that has been written in different projects. 


## util.py
This file contains basic IO and augmentation codes for image. 


## keras_util

#### GlobalSumPooling2D: 
Keras has GlobalMaxPooling2D class which has modified here for sum pooling. 
    input                output 
  (None, L, W, ch)        (None, 1, 1, ch)      
  (None, ch, L, W)        (None, ch, 1, 1)      

#### save_prediction: 
This class is used as class_back function in autoencoder or Transfer learning models where we input some image and get image in output. To save generation on each epoch, for example, add the class in the list of class_back functions for model training. 
Parameters: 
batch_generator = object of batch generator function  
name: The name of the result files you want to save
encoder, decoder: These are model/s that can be used for generation 
path='' : The path  where you want to save result files

Note: Replace batch_generator with images, instead of encoder/decoder use own model, you are ready to go.

#### checkpoint
This is call_back class to be used to save model when conditions meets. 
If there are sub models in training and we need to save each sub model when its loss improve then use this as call_back for each model. All arguments are same to keras CheckPoint callback except it has one more argument of model itself.
