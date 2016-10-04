from ast import literal_eval as make_tuple
import numpy as np
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes
from pyspark import SparkConf
from pyspark import SparkContext
from nltk.tokenize import RegexpTokenizer

def read_input():
    f = open('part-00000', 'r')
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

def comments2list(comments):
    list = []
    for (user, cmt) in comments:
        #print(tpl)
        # = make_tuple(tpl)
        list.append(user)
        list.append(cmt)
    return list

def create_vocabulary(data_vector):
    dict = {}
    for string in data_vector:
        tolkens = string.split(' ')
        for tk in tolkens:
            try:
                dict[tk]
            except KeyError:
                dict[tk] = 1

    return sorted(list(dict.keys()))

def string2feature(string, vocabulary):
    tokenizer = RegexpTokenizer(r'\w+')
    tolkens = tokenizer.tokenize(string)
    hash = {}
    feature = []
    for tk in tolkens:
        try:
            hash[tk] += 1
        except KeyError:
            hash[tk] = 1

    for word in vocabulary:
        try:
            feature.append(float(hash[word]))
        except Exception as e:
            feature.append(0.0)

    return feature

def features_transform(trainset, testset):
    dataset = [row[1:-1] for row in trainset]
    tdataset = [row[1:-1] for row in testset]
    strs = []
    trainfeatures = []
    testfeatures = []

    for row in dataset:
        strs.append(row[0])
        # transform list of comments into a big string
        row[-1] = comments2list(row[-1])
        strs = strs + row[-1]

    vocabulary = create_vocabulary(strs)

    for row in dataset:
        row[0] = string2feature(row[0], vocabulary)
        row[-1] = string2feature(' '.join(row[-1]), vocabulary)
        trainfeatures.append(row[0] + [row[1]] + row[2] + row[3])

    for row in tdataset:
        row[0] = string2feature(row[0], vocabulary)
        row[-1] = comments2list(row[-1])
        row[-1] = string2feature(' '.join(row[-1]), vocabulary)
        testfeatures.append(row[0] + [row[1]] + row[2] + row[3])

    return (trainfeatures, testfeatures)

def get_labeled_points(labels, features):
    lpts = []

    for i in range(0,len(labels)):
        lpts.append(LabeledPoint(labels[i], features[i]))

    return lpts


conf = SparkConf().setAppName('test').setMaster('local')
sc = SparkContext(conf=conf)
(data_train, data_test) = read_input()
(trainset, testset) = features_transform(data_train, data_test)
trainset = sc.parallelize(get_labeled_points([row[-1] for row in data_train], trainset))
model = NaiveBayes.train(trainset, 1.0)

index = [i for i in range(0, len(testset)) if model.predict(testset[i]) == 1.0]
result = np.array([row[0] for row in data_test])
result = result[index]
result = map((lambda x : "http://9gag.com/gag/{}".format(x)), result)
print('\n'.join(result))
