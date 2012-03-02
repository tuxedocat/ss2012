# coding: utf-8
import nltk
import cPickle as pickle
import timeit
import classifier

class PrepChecker(object):
    def __init__(self, path):
        from nltk.tag import pos_tag as tagger
        from nltk import word_tokenize as tokenizer
        self.PREPS = ["in", "for", "at", "on", "of", "about", "with", "from", "by", "as", "into"]
        self.PREPTAGS = ["IN"]
        with open(path, "rb") as pkl:
            self.corpus = pickle.load(pkl)[0:10]
        self.trainingdata = [dic["gold"] for dic in self.corpus]
        self.testdata = [dic["test"] for dic in self.corpus]
        self.correctionpairs = [dic["correction_pair"] for dic in self.corpus]
        self.postagged_testdata = self._postag(tokenizer, tagger, self.testdata)
        self.postagged_trainingdata = self._postag(tokenizer, tagger, self.trainingdata)
        self.features = []
        self.labellist = [dic["correction_pair"][1] for dic in self.corpus]

    def _postag(self, tokenizer, tagger, datalist): 
        return [tagger(tokenizer(sent)) for sent in datalist]


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

