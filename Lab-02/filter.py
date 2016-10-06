from ast import literal_eval as make_tuple
import numpy as np
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes
from pyspark import SparkConf
from pyspark import SparkContext
from nltk.tokenize import RegexpTokenizer
import sys

train_size = 1000

def read_input():
    #f = open('part-00000', 'r')
    f = open('training_set.dat', 'r')
    data_input = []
    test_input = []

    for line in f:
        post = list(make_tuple(line))
        label = float(post[-1:][0])
        if label == 0.0 or label == 1.0:
            data_input.append(post)
        elif label == 2.0:
            test_input.append(post)
    return (data_input, test_input)

def comments2string(comments):
    for i in range(0,len(comments)):
        comments[i] = ' '.join(comments[i])
    return ' '.join(comments)


def create_vocabulary(string):
    #print('CREAT VOC START')
    #tokenizer = RegexpTokenizer(r'\w+')
    #tolkens = tokenizer.tokenize(string)

    dict1 = {}
    dict2 = {}
    index = 0
    tolkens = string.split(' ')
    for tk in tolkens:
        try:
            #dict[tk]
            dict1[tk] += 1
        except KeyError:
            #dict[tk] = index
            #index += 1
            dict1[tk] = 0

    index = 0
    print('First size = ' + str(len(dict1)))
    mean = sum(dict1[k] for k in dict1) / len(dict1)
    print("Mean = " + str(mean))
    print("Max = " + str(max(dict1[k] for k in dict1)))
    for k in dict1:
        if dict1[k] < 3 * mean and dict1[k] > 2 * mean:
            dict2[k] = index
            index += 1
    print("Size = " + str(len(dict2)))
    return dict2

def string2feature(string, vocabulary):
    #tokenizer = RegexpTokenizer(r'\w+')
    #tolkens = tokenizer.tokenize(string)
    feature = [0.0] * len(vocabulary)
    tolkens = string.split(' ')

    for tk in tolkens:
        try:
            index = vocabulary[tk]
            feature[index] += 1.0
        except KeyError:
            continue
    return feature

def features_transform(trainset, testset):
    print('FTR2TRNSF START')
    dataset = [row[1:-1] for row in trainset]
    tdataset = [row[1:-1] for row in testset]
    strs = ""

    for row in dataset:
        strs += row[0] + ' '
        # transform list of comments into a big string
        row[-1] = comments2string(comments=row[-1])
        strs = strs + row[-1] + ' '
    vcb = create_vocabulary(string=strs)

    print('DATASET')
    for i in range(0, len(dataset)):
        row = dataset[i]
        row[0] = string2feature(string=row[0], vocabulary=vcb)
        row[-1] = string2feature(string=row[-1], vocabulary=vcb)
        dataset[i] = row[0] + [row[1]] + row[2] + row[3]

    print("END DATASET")
    print("TDATASET")
    for i in range(0,len(tdataset)):
        row = tdataset[i]
        print('Kupo2')
        row[0] = string2feature(string=row[0], vocabulary=vcb)
        row[-1] = comments2string(row[-1])
        row[-1] = string2feature(string=row[-1], vocabulary=vcb)
        tdataset[i] = row[0] + [row[1]] + row[2] + row[3]
    print('FTR2TRNSF END')
    return (dataset, tdataset)

def get_labeled_points(labels, features):
    print('GET LBLPTS START')
    lpts = []

    for i in range(0,len(labels)):
        lpts.append(LabeledPoint(labels[i], features[i]))
    print('GET LBLPTS START')
    return lpts

# Main code
print('PROCESSING')
conf = SparkConf().setAppName('test').setMaster('local[4]')
sc = SparkContext(conf=conf)
(data_train, data_test) = read_input()
(trainset, testset) = features_transform(data_train, data_test)
trainset = sc.parallelize(get_labeled_points([row[-1] for row in data_train], trainset))
print('TRAINING')
model = NaiveBayes.train(trainset, 1.0)
print('PREDICTING')
index = [i for i in range(0, len(testset)) if model.predict(testset[i]) == 1.0]
result = np.array([row[0] for row in data_test])
result = result[index]
result = map((lambda x : "http://9gag.com/gag/{}".format(x)), result)
print('\n'.join(result))
