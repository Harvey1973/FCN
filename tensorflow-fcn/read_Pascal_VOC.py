__author__ = 'charlie'
import numpy as np
import os
import random
from six.moves import cPickle as pickle
from tensorflow.python.platform import gfile
import glob

import TensorflowUtils as utils

# DATA_URL = 'http://sceneparsing.csail.mit.edu/data/ADEChallengeData2016.zip'
#DATA_URL = 'http://data.csail.mit.edu/places/ADEchallenge/ADEChallengeData2016.zip'
train_list_dir = 'VOCdevkit/VOC2012/ImageSets/Segmentation/train.txt'
trainval_list_dir = 'VOCdevkit/VOC2012/ImageSets/Segmentation/trainval.txt'
val_list_dir = 'VOCdevkit/VOC2012/ImageSets/Segmentation/val.txt'
image_dir ='VOCdevkit/VOC2012/JPEGImages/'
annotation_dir = 'VOCdevkit/VOC2012/annotations'
test_list_dir = 'VOCdevkit/VOC2012/ImageSets/Segmentation/test.txt'

def read_dataset(data_dir):
    pickle_filename = "Pascal_VOC.pickle"
    pickle_filepath = os.path.join(data_dir, pickle_filename)
    if not os.path.exists(pickle_filepath):
        #utils.maybe_download_and_extract(data_dir, DATA_URL, is_zipfile=True)
        #SceneParsing_folder = os.path.splitext(DATA_URL.split("/")[-1])[0]
        result = create_image_lists(image_dir)  #creates a dict
        print('img_dir is ..' )
        print(image_dir)
        print ("Pickling ...")
        with open(pickle_filepath, 'wb') as f:
            pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)
    else:
        print ("Found pickle file!")

    with open(pickle_filepath, 'rb') as f:
        result = pickle.load(f)
        training_records = result['training']
        validation_records = result['validation']
        test_records = result['test']
        del result

    return training_records, validation_records,test_records


def create_image_lists(image_dir):
    if not gfile.Exists(image_dir):
        print("Image directory '" + image_dir + "' not found.")
        return None
    directories = ['training', 'validation','test']
    image_list = {}

    for directory in directories:
        file_list = []
        image_list[directory] = []
        
        if directory == 'training':
            f_train = open(train_list_dir)
            for line in f_train:
                file_name = line.split('\n')[0]
                #print(file_name)
                file_glob = os.path.join(image_dir, file_name + '.jpg')  #directory for images 
                file_list.extend(glob.glob(file_glob))
            #f_train_more = open(trainval_list_dir)
            #for line in f_train_more:
            #    file_name = line.split('\n')[0]
                #print(file_name)
            #    file_glob = os.path.join(image_dir, file_name + '.jpg')  #directory for images 
            #    file_list.extend(glob.glob(file_glob))
        elif directory=='validation' :
            f_val = open(val_list_dir)
            for line in f_val:
                file_name = line.split('\n')[0]
                #print(file_name)
                file_glob = os.path.join(image_dir, file_name + '.jpg')  #directory for images 
                file_list.extend(glob.glob(file_glob))
        elif directory == 'test':
            f_test = open(test_list_dir)
            for line in f_test:
                file_name = line.split('\n')[0]
                file_glob = os.path.join(image_dir, file_name + '.jpg')  #directory for images 
                file_list.extend(glob.glob(file_glob))
        
        if not file_list:
            print('No files found')
        else:
            for f in file_list:
                filename = os.path.splitext(f.split("/")[-1])[0]   # gets the actual image file name
                annotation_file = os.path.join(annotation_dir, filename + '.png')
                if os.path.exists(annotation_file):
                    record = {'image': f, 'annotation': annotation_file, 'filename': filename}
                    image_list[directory].append(record)
                else:
                    print("Annotation file not found for %s - Skipping" % filename)

        random.shuffle(image_list[directory])
        no_of_images = len(image_list[directory])
        print ('No. of %s files: %d' % (directory, no_of_images))
    #print('what is this')
    #print(file_list[0].split("/"))
    return image_list
#train_reords ,val_recrods = read_dataset('VOCdevkit/VOC2012')
#print(train_reords[0])