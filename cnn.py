import tensorflow as tf
import numpy as np

from stable_baselines.a2c.utils import conv, linear, conv_to_fc

def cnn(scaled_images, **kwargs):
    activ = tf.nn.relu
    l1 = activ(conv(scaled_images, 'c1', n_filters=32, filter_size=2, stride=1, init_scale=np.sqrt(2), **kwargs))
    l2 = activ(conv(l1, 'c2', n_filters=64, filter_size=2, stride=1, init_scale=np.sqrt(2), **kwargs))
    l3 = activ(conv(l2, 'c3', n_filters=64, filter_size=2, stride=1, init_scale=np.sqrt(2), **kwargs))
    l4 = conv_to_fc(l3)
    l5 = activ(linear(l4, 'fc1', n_hidden=512, init_scale=np.sqrt(2)))
    return l5
