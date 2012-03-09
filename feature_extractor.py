# coding: utf-8
import nltk
from nltk import pos_tag


class FeatureExtractor(object):
    """
    素性抽出関数

    nltk.pos_tagをngram pos featureで使用
    
    TODO
        implement more sophisticated features
    """
    def __init__(self, sent, ppindex, *ARGS):
        self.sent = sent
        self.PREPS = ["in", "for", "at", "on", "of", "about", "with", "from", "by", "as", "into"]
        self.PPTAG = ["IN"]
        self.ppindex = ppindex
        self.ARGS = ARGS
        self.featuredict = {}
        self.n = 2 
        self.tagger = nltk.pos_tag


    def features(self):
        def _ngramfeature(n = 2):
            _feature = {}
            ngrams = [(index - self.ppindex, word) for index, word in enumerate(self.sent) 
                        if index != self.ppindex and index >= self.ppindex - n]
            for i, word in ngrams:
                _feature.update({"%d-gram(%d)_%s"%(n*2+1, i, word): 1})
            return _feature

        def _ngramposfeature(n = 2):
            _feature = {}
            taggedsent = self.tagger(self.sent)
            posngrams = [(index - self.ppindex, t[1]) for index, t in enumerate(taggedsent) 
                        if index != self.ppindex and index >= self.ppindex - n]
            for i, word in posngrams:
                _feature.update({"POS_%d-gram(%d)_%s"%(n*2+1, i, word): 1})
            return _feature

        def _succ():
            _succfeature = {}
            _succfeature.update({"succ_%s"%(self.sent[self.ppindex + 1]) : 1})
            return _succfeature

        try:
            if "pos" in self.ARGS:
                self.featuredict.update(_ngramposfeature(self.n))
            if "ngram" in self.ARGS:
                self.featuredict.update(_ngramfeature(self.n))
            if "succ" in self.ARGS:
                self.featuredict.update(_succ())

        finally:
            return self.featuredict


