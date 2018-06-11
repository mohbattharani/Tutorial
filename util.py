import math
import cv2
import numpy as np
import random
import os
import sys
import glob
import h5py
from  keras.utils import to_categorical
from PIL import Image

from keras.preprocessing.image import array_to_img, img_to_array, load_img


seq = iaa.Sequential([
    iaa.Crop(px=(0, 40)),
    iaa.GaussianBlur(sigma=(0, 3.0)), # blur images with a sigma of 0 to 3.0
    
    iaa.Affine(translate_px={"x": (-40, 40)},
               rotate = (-20, 20)  ),
    
])
def augment(batch):
    batch = seq.augment_images(batch)
    return batch


def rotate(image, angle):
    """
    Rotate an OpenCV 2 / NumPy image around it's centre by the given angle
    (in degrees). The returned image will have the same size as the new image.
    Adapted from: http://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
    """

    # Get the image size
    # No that's not an error - NumPy stores image matricies backwards
    image_size = (image.shape[1], image.shape[0])
    image_center = tuple(np.array(image_size) / 2 - 0.5)

    # Convert the OpenCV 3x2 rotation matrix to 3x3
    rot_mat = np.vstack(
        [cv2.getRotationMatrix2D(image_center, angle, 1.0), [0, 0, 1]]
    )

    # We require a translation matrix to keep the image centred
    trans_mat = np.matrix([
        [1, 0, int(image_size[0] * 0.5 - image_center[1])],
        [0, 1, int(image_size[0] * 0.5 - image_center[1])],
        [0, 0, 1]
    ])

    # Compute the tranform for the combined rotation and translation
    affine_mat = (np.matrix(trans_mat) * np.matrix(rot_mat))[0:2, :]

    # Apply the transform
    result = cv2.warpAffine(
        image,
        affine_mat,
        image_size,
        flags=cv2.INTER_LINEAR
    )

    return result

def imread(image_path, angle=None):
    im = cv2.imread(image_path)
    image_size = (256, 256)
    im = cv2.resize(im, (256, 256))
    if (angle!=None):
        im = rotate(im, angle)

    im = cv2.resize(im, (256, 256))

    return im

def load_batch(batch_path, angle=None, aug= False):
    if (len(batch_path)<1):
    	print('Error: empty batch')
    	return batch_path
    	
    batch  =np.array([imread(image_name, angle) for image_name in batch_path])
    if (aug):
        batch = augment(batch) 

    return batch


# reads paths to all images in GTCrossView dataset.
# im_type = streetview, overhead
def read_GTCrossView(dataset_path, folders, im_type, ext ='.jpg'):

    paths_X = []    
    for folder in folders:
        paths_X += sorted(glob.glob(os.path.join(dataset_path,folder+'/*'+im_type+ext)))
    
    if(len(paths_X)==0):
    	print ('Dataset could not found. Please provide correct path.')

    return paths_X

def read_landUse(dataset_path, im_type):
    import glob
    paths_X = []   
    labels = [] 
    i = 0
    folders = sorted(os.listdir(dataset_path))
    for folder in folders:
        temp = sorted (glob.glob(os.path.join(dataset_path,folder+'/*'+im_type)))
        for k in range(len(temp)):
            labels.append (i)
        paths_X += temp
        i += 1
        
    if(len(paths_X)==0):
        print ('Dataset could not found. Please provide correct path.')

    return paths_X, labels

def read_imPaths(dataset_path, folders, im_type):
    import glob
    paths_X = []    
    for folder in folders:
        paths_X += sorted (glob.glob(os.path.join(dataset_path,folder+'/*'+im_type)))
    
    if(len(paths_X)==0):
    	print ('Dataset could not found. Please provide correct path.')

    return paths_X


def train_val_splitx(X):
    train_x = []
    val_x = []

    for i in range(len(X)):
        if (i%5==0):
            val_x.append(X[i])
        else:
            train_x.append(X[i])

    return train_x, val_x

# ===================================================================================
# This function load features in .mat file from given directroy. This was developed to load features 
# used by Napoletano
def load_cnn_features(path, dataset, feature_name):
    path_features = os.path.join(path, dataset)+'/featuresIR'
    path_label = os.path.join(path,dataset)+'/util/labels.mat'
    features = h5py.File(os.path.join(path_features, feature_name))['features']
    features = np.array(features).T
    r,c = features.shape
    features = features.reshape(r,c,1)
    return features

def load_encoder_features (path, feature_name):
    path_features = os.path.join(path, feature_name+'.npy')
    features = np.load(path_features)
    return features                             
                              
