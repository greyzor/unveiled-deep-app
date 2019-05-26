"""
Image classifier based in InceptionV3 (keras implementation).
"""
from PIL import Image
from keras.preprocessing import image
import keras.applications.inception_v3 as inception_v3
import keras.backend
import tensorflow as tf
import numpy as np
import requests
import pprint

keras.backend.clear_session()

MODEL_INPUT_SIZE_DEFAULT = (299, 299) # default size expected by inception v3 input.

class InceptionV3Classifier(object):
	""" InceptionV2 classifier class. """
	def __init__(self, weights='imagenet', target_size=MODEL_INPUT_SIZE_DEFAULT):
		""" Constructor. """
		self.inception_model = inception_v3.InceptionV3(weights=weights)
		self.target_size = target_size
		self.graph = tf.get_default_graph()

	def classify(self, img_path, top=5):
	    """Classify image and return top matches.
	    :param img_path: input file path of image.
		:param top: number of top results to return.
		:returns: predictions about detected classes in image.
		:rtype: list[list[tuple(str: class_id, str: class_name, float: score)]]
	    """
	    # Open image
	    img = Image.open(img_path)

	    # Image resizing and preparation for keras.
	    if img.size != self.target_size:
	        img = img.resize(self.target_size)

	    x = image.img_to_array(img)
	    x = np.expand_dims(x, axis=0)
	    x = inception_v3.preprocess_input(x)

	    # Predictions
	    preds = []
	    with self.graph.as_default():
		    preds = self.inception_model.predict(x)

	    # Decode predictions
	    return inception_v3.decode_predictions(preds, top=top)