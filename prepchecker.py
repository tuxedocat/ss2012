# coding: utf-8
import nltk
import cPickle as pickle
import time
import classifier
from nltk.tag import pos_tag as tagger
from feature_extractor import FeatureExtractor



class PrepChecker(object):
    def __init__(self, path):
        self.PREPS = ["in", "for", "at", "on", "of", "about", "with", "from", "by", "as", "into"]
        self.PREPTAGS = ["IN"]
        with open(path, "rb") as pkl:
            self.corpus = pickle.load(pkl)
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
        trainset_features = self.makefeatures(self.training_words[:1400])
        trainset_labels = self.labellist[:1400]
        trainset = zip(trainset_features, trainset_labels)
        classifier = nltk.MaxentClassifier.train(trainset, algorithm="IIS", max_iter=20)
        self.classifier = classifier

        pass


    def test(self):
        classifier_outputs = []
        testset_features = self.makefeatures(self.test_words[1400:])
        testset_labels = self.labellist[1400:]
        testset = zip(testset_features, testset_labels)
        classifier = self.classifier
        print "Accuracy on the test set:", nltk.classify.accuracy(classifier, testset)
        for testcase in testset_features:
            classifier_out = classifier.classify(testcase)
            classifier_outputs.append(classifier_out)
        cm = nltk.ConfusionMatrix(testset_labels, classifier_outputs)
        print cm
        pass


    
    def stat(self):
        pass


def main():
    st = time.time()
    print "Started...\nReading corpus..."
    pc = PrepChecker("packedcorpus.pkl")
    print "Training..."
    pc.train()
    print "done!"
    print "Testing..."
    pc.test()
    et = time.time()
    print "Overall...%5.3f [sec.]"%(et-st)




if __name__=="__main__":
    main()

