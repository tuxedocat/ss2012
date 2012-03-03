# coding: utf-8
import nltk
import cPickle as pickle
import timeit
import classifier

class PrepChecker(object):
    def __init__(self, path):
        from nltk.tag import pos_tag as tagger
        self.PREPS = ["in", "for", "at", "on", "of", "about", "with", "from", "by", "as", "into"]
        self.PREPTAGS = ["IN"]
        with open(path, "rb") as pkl:
            self.corpus = pickle.load(pkl)[0:10]
        self.training_words = [dic["gold_words"] for dic in self.corpus]
        self.test_words = [dic["test_words"] for dic in self.corpus]
        self.correctionpairs = [dic["correction_pair"] for dic in self.corpus]
        self.postagged_testdata = self._postag(tagger, self.test_words)
        self.postagged_trainingdata = self._postag(tagger, self.training_words)
        self.features = []
        self.labellist = [dic["correction_pair"][1] for dic in self.corpus]

    def _postag(self, tagger, datalist): 
        return [tagger(sent) for sent in datalist]


    def featureextractor(self, postagged_sents):
        from feature_extractor import fext
        for sent in postagged_sents:
            self.features.append(fext("pos", sent))


    def train(self):

        pass


    def test(self):
        pass

    
    def stat(self):
        pass


def main():
    pc = PrepChecker("packedcorpus.pkl")
    pc.featureextractor(pc.postagged_trainingdata)
    print pc.features
    print pc.labellist


if __name__=="__main__":
    main()

