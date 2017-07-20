#!/usr/bin/env python

import os
import scipy as scp
import scipy.misc

import numpy as np
import logging
import tensorflow as tf
import sys

import fcn8_vgg
import utils

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

from tensorflow.python.framework import ops

img1 = scp.misc.imread("tabby_cat.png")
img1 = scipy.misc.imresize(img1,(224,224))
with tf.Session() as sess:
    images = tf.placeholder("float")
    feed_dict = {images: img1}
    batch_images = tf.expand_dims(images, 0)

    vgg_fcn = fcn8_vgg.FCN8VGG()
    with tf.name_scope("content_vgg"):
        vgg_fcn.build(batch_images, debug=True,train=True,random_init_fc8=False)

    print('Finished building Network.')

    logging.warning("Score weights are initialized random.")
    logging.warning("Do not expect meaningful results.")

    logging.info("Start Initializing Variabels.")

    init = tf.global_variables_initializer()
    sess.run(init)

    print('Running the Network')
    tensors = [vgg_fcn.pred, vgg_fcn.pred_up]
    down, up = sess.run(tensors, feed_dict=feed_dict)
    print(down[0])
    down_color = utils.color_image(down[0])
    up_color = utils.color_image(up[0])

    scp.misc.imsave('fcn8_downsampled_ball.png', down_color)
    scp.misc.imsave('fcn8_upsampled_ball.png', up_color)
