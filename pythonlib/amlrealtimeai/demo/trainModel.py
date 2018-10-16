import os
import sys
import tensorflow as tf
import numpy as np
import amlrealtimeai
from amlrealtimeai import resnet50

import glob
import imghdr

datadir = os.path.expanduser("~/images")

cat_files = glob.glob(os.path.join(datadir, 'PetImages', 'Cat', '*.jpg'))
dog_files = glob.glob(os.path.join(datadir, 'PetImages', 'Dog', '*.jpg'))

# Limit the data set to make the notebook execute quickly.
cat_files = cat_files[:64]
dog_files = dog_files[:64]

# The data set has a few images that are not jpeg. Remove them.
cat_files = [f for f in cat_files if imghdr.what(f) == 'jpeg']
dog_files = [f for f in dog_files if imghdr.what(f) == 'jpeg']

if(not len(cat_files) or not len(dog_files)):
    print("Please download the Kaggle Cats and Dogs dataset form https://www.microsoft.com/en-us/download/details.aspx?id=54765 and extract the zip to " + datadir)
    raise ValueError("Data not found")
else:
    print(cat_files[0])
    print(dog_files[0])

# constructing a numpy array as labels
image_paths = cat_files + dog_files
total_files = len(cat_files) + len(dog_files)
labels = np.zeros(total_files)
labels[len(cat_files):] = 1

import amlrealtimeai.resnet50.utils
in_images = tf.placeholder(tf.string)
image_tensors = resnet50.utils.preprocess_array(in_images)
print(image_tensors.shape)
