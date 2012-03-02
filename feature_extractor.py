# coding: utf-8
import nltk

class FeatureExtractor(object):
    def __init__(self, postagged_sent):
        self.sents = postagged_sent
        self.PREPS = ["in", "for", "at", "on", "of", "about", "with", "from", "by", "as", "into"]
        self.PPTAG = ["IN"]
        self.ppindex = self.ppfinder(postagged_sent)


    def ppfinder(self, sent):
        index = 0
        for i, tup in enumerate(sent):
            if tup[0] in self.PREPS and tup[1] in self.PPTAG:
                index = i
                break
        if index == 0:
            return None
        else:
            return index


    def ngramfeature(self):
        return {"ngram":1}
        pass


    def posfeature(self):
        return {"pos":1}
        pass


def fext(ARG, postagged_sent):
    fe = FeatureExtractor(postagged_sent)
    if ARG == "ngram":
        return {"ngram": 1}
    elif ARG == "pos":
        return {"pos":1, "pos2":1}

    





if __name__=="__main__":
    main()
