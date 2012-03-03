# coding: utf-8
import nltk
from nltk import pos_tag

class FeatureExtractor(object):
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


        def _ngramfeature(n = 2):
            ngrams = [(index - self.ppindex, word) for index, word in enumerate(self.sent) 
            for i, word in ngrams:

            _feature = {}
            posngrams = [(index - self.ppindex, t[1]) for index, t in enumerate(taggedsent) 
                        if index != self.ppindex and index >= self.ppindex - n]
            for i, word in posngrams:
            return _feature

            if "pos" in self.ARGS:
            if "ngram" in self.ARGS:

            return self.featuredict
>>>>>>> test
