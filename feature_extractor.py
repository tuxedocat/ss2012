# coding: utf-8
import nltk

class FeatureExtractor(object):
    def __init__(self, postagged_sent, ppindex, *ARGS):
        self.sents = postagged_sent
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
