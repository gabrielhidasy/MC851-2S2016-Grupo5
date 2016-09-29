from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.regression import LabeledPoint
import numpy as np

def Preprocessing(data):

    num_features = len(data) - 2
    trainingset = np.empty((0, num_features))
    traininigset_label = np.empty((0, num_features))

    for element in data:
        post = list(element)
        last = len(post) - 1
        label = post[last]
        np.append(traininigset_label, label, axis=0)
    return
