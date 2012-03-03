# coding: utf-8
import nltk
import cPickle as pickle
import timeit
import classifier
from nltk.tag import pos_tag as tagger
from feature_extractor import FeatureExtractor



class PrepChecker(object):
    def __init__(self, path):
        self.PREPS = ["in", "for", "at", "on", "of", "about", "with", "from", "by", "as", "into"]
        self.PREPTAGS = ["IN"]
        with open(path, "rb") as pkl:
            self.corpus = pickle.load(pkl)[:20]
        self.training_words = [dic["gold_words"] for dic in self.corpus]
        self.test_words = [dic["test_words"] for dic in self.corpus]
        self.correction_pairs = [dic["correction_pair"] for dic in self.corpus]
        self.labellist = [dic["correction_pair"][1] for dic in self.corpus]
        self.ppindexlist = [dic["ppindex"] for dic in self.corpus]
        self.packeddata = zip(self.training_words, self.test_words,
                              self.ppindexlist, self.labellist, self.correction_pairs)


    def makefeatures(self, sents_list): 
        _features = []
        for sent, ppindex in zip(sents_list, self.ppindexlist):
            fe = FeatureExtractor(sent, ppindex, "pos", "ngram")
            _features.append(fe.features())
        return _features


    def train(self):
        trainset_features = self.makefeatures(self.training_words[:10])
        trainset_labels = self.labellist[:10]
        trainset = zip(trainset_features, trainset_labels)
        classifier = nltk.MaxentClassifier.train(trainset, max_iter=3)
        self.classifier = classifier

        pass


    def test(self):
        testset_features = self.makefeatures(self.test_words[:10])
        testset_labels = self.labellist[:10]
        testset = zip(testset_features, testset_labels)
        classifier = self.classifier
        print nltk.classify.accuracy(classifier, testset)
        pass

    
    def stat(self):
        pass


def main():
    pc = PrepChecker("packedcorpus.pkl")
    pc.train()
    pc.test() 




if __name__=="__main__":
    main()

