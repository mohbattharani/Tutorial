from keras import backend as K
from keras.engine.topology import Layer, InputSpec
import numpy as np
from keras.legacy import interfaces
import keras 
import sys, os, cv2

class _GlobalPooling2D(Layer):
    """Abstract class for different global pooling 2D layers.
    """

    @interfaces.legacy_global_pooling_support
    def __init__(self, data_format=None, **kwargs):
        super(_GlobalPooling2D, self).__init__(**kwargs)
        self.data_format = 'channels_last'#(data_format)
        self.input_spec = InputSpec(ndim=4)

    def compute_output_shape(self, input_shape):
        if self.data_format == 'channels_last':
            return (input_shape[0], input_shape[3])
        else:
            return (input_shape[0], input_shape[1])

    def call(self, inputs):
        raise NotImplementedError

    def get_config(self):
        config = {'data_format': self.data_format}
        base_config = super(_GlobalPooling2D, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class GlobalSumPooling2D(_GlobalPooling2D):

    def call(self, inputs):
        if self.data_format == 'channels_last':
            #out = K.sum(inputs, axis=1)
            #out = K.sum(inputs, axis=1)
            return K.sum(inputs, axis=[1, 2])
        else:
            return K.sum(inputs, axis=[2, 3])

# ===================================================================== 
# This call back class is used to save prediction of encoder, decoder network the end of each epoch

class save_prediction(keras.callbacks.Callback):
    def __init__(self , batch_generator, name, encoder, decoder, path=''):
        self.batch_generator = batch_generator 
        self.name = name
        self.encoder = encoder
        self.decoder = decoder
        self.path = path
    
    def on_epoch_end(self, epoch, logs=None):
        if (sys.version_info >= (3,0)):
            images,y2 = self.batch_generator.__next__()
        else:
            images,y2 = self.batch_generator.next()
        
        features = self.encoder.predict(images[0])
        fake_images = self.decoder.predict (features)
        
        n = images[0].shape[0]
        if (n>8):
            n = 8        
        
        im1 = np.hstack( (np.asarray(images[0][i,:,:,:]) for i in range(n) ) )
        im2 = np.hstack( (np.asarray(fake_images[i,:,:,:]) for i in range(n) ) )
        imgs_comb = np.concatenate ((im1,im2), axis=0)
        cv2.imwrite(os.path.join(self.path,self.name+str(epoch)+'.png'), imgs_comb)
        
# =============================================================================
# This call back function is used to save check point of the model
# If we have more than one model comined, we need to change each ones learning rate 
# one improvement of its loss then this custom call back is used

class checkpoint(keras.callbacks.Callback):

    def __init__(self, model, path,monitor='val_loss', patience = 3, factor = 0.1):
        self.model_to_save = model
        self.path = path
        self.monitor = monitor
        self.best = np.Inf
        self.count = 0
        self.patience = patience
        self.factor = factor
    def on_epoch_end(self, epoch, logs={}):
        current = logs.get(self.monitor)
        if current < self.best: 
            self.model_to_save.save(self.path)
            print ('Loss improved from %s to %s. model saved.'%(self.best,current))
            self.best = current
        else:
            print ('loss did not improve')
            self.count += 1
        
        if (self.count >= self.patience ):
            self.model_to_save.optimizer.lr *= self.factor
            self.count = 0
            
GlobalSumPool2D = GlobalSumPooling2D