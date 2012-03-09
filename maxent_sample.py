#!/usr/bin/env python
#encoding: utf-8

#import library
import nltk
from nltk.classify import MaxentClassifier


#feature vector/set for training
training =[
        (dict(x1=1,x3=1,x8=1), 'N'),
        (dict(x4=1,x6=1,x8=1), 'N'),
        (dict(x4=1,x6=1,x8=1), 'L'),
        (dict(x1=1,x5=1,x9=1), 'L'),
        (dict(x1=1,x2=1,x6=1), 'P'),
        (dict(x3=1,x4=1,x8=1), 'P')
        ]


#featre vector/set for test
test = [
        (dict(x1=1, x6=1, x8=1))
        ]


#training classifier (example)
me_classifier =  MaxentClassifier.train(training, algorithm='iis', trace=0, max_iter=1, min_lldelta=0.5)


#classify the test using the classifier above (example)
pdist = me_classifier.prob_classify(test[0])


#print results
print 'probability of N'
print pdist.prob('N')
print 'probability of L'
print pdist.prob('L')
print 'probability of P'
print pdist.prob('P')

