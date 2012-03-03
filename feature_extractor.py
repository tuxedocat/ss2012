# coding: utf-8
import nltk
from nltk import pos_tag

class FeatureExtractor(object):
<<<<<<< HEAD
    def __init__(self, postagged_sent, ppindex, *ARGS):
        self.sents = postagged_sent
=======
    def __init__(self, sent, ppindex, *ARGS):
        self.sent = sent
>>>>>>> test
        self.PREPS = ["in", "for", "at", "on", "of", "about", "with", "from", "by", "as", "into"]
        self.PPTAG = ["IN"]
        self.ppindex = ppindex
        self.ARGS = ARGS
        self.featuredict = {}
<<<<<<< HEAD


    def features(self):
        def _ngramfeature():
            return {"ngram":1}

        def _posfeature():
            return {"pos":1}

        try:
            if "pos" in self.ARGS:
                self.featuredict.update(_posfeature())
            if "ngram" in self.ARGS:
                self.featuredict.update(_ngramfeature())
        finally:
            return self.featuredict
=======
        self.n = 2
        self.tagger = nltk.pos_tag


    def features(self):
        def _ngramfeature(n = 2):
            _feature = {}
            ngrams = [(index - self.ppindex, word) for index, word in enumerate(self.sent) 
                        if index != self.ppindex and index >= self.ppindex - n]
            for i, word in ngrams:
                _feature.update({"%d-gram(%d)_%s"%(n, i, word): 1})
            return _feature

        def _ngramposfeature(n = 2):
            _feature = {}
            taggedsent = self.tagger(self.sent)
            posngrams = [(index - self.ppindex, t[1]) for index, t in enumerate(taggedsent) 
                        if index != self.ppindex and index >= self.ppindex - n]
            for i, word in posngrams:
                _feature.update({"POS_%d-gram(%d)_%s"%(n, i, word): 1})
            return _feature

        try:
            if "pos" in self.ARGS:
                self.featuredict.update(_ngramposfeature(self.n))
            if "ngram" in self.ARGS:
                self.featuredict.update(_ngramfeature(self.n))

        finally:
            return self.featuredict

>>>>>>> test
