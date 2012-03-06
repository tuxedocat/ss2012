# coding: utf-8
import nltk
import cPickle as pickle
import time
import random
from feature_extractor import FeatureExtractor


class PrepChecker(object):
    """
    前置詞誤り訂正器本体
    
    VARIABLES
        gold_words  : dict型のコーパスの"gold"キーの値をリスト化したもの(要素は単語分割された文のリスト)
        test_words      : "test_words"の値をリスト化したもの(上記と同様)
        correction_pairs: "correction_pairs"の値をリスト化したもの(要素はtuple)
        labellist       : correction_pairから得た正解ラベルのリスト
        ppindexlist     : 単語分割されたリスト中での前置詞誤り箇所のリスト(誤りは特定済みだという問題設定のため)
        packeddata      : 文順序をシャッフルしても良いようにとtuple に詰めたもの (現在未使用)
    METHODS
        __init__(path)      : path = カレントディレクトリの"packedcorpus.pkl"
        makefeature(sent)   : FeatureExtractorクラスで素性抽出する
                              sent は単語分割された文のリスト
        train()             : nltk.MaxentClassifierを学習させる
        test()              : テストセットに対して評価(accuracy)を行い正解ラベルとの混同行列を出力する

    TODO
        * train(), test() should handle various amount of training and test dataset
        * make classifier work with scipy's faster MaxEnt implementation

    """

    def __init__(self, path):
        with open(path, "rb") as pkl:
            self.corpus = pickle.load(pkl)
        gold_words = [dic["gold_words"] for dic in self.corpus]
        test_words = [dic["test_words"] for dic in self.corpus]
        corr_pairs = [dic["correctionpair"] for dic in self.corpus]
        labellist = [dic["correctionpair"][1] for dic in self.corpus]
        ppindexlist = [dic["ppindex"] for dic in self.corpus]
        rawsents = [dic["rawtext"] for dic in self.corpus]
        self.packeddata = zip(gold_words, test_words, ppindexlist, labellist, corr_pairs, rawsents)
        random.shuffle(self.packeddata)
        self.gold_words = [t[0] for t in self.packeddata]
        self.test_words = [t[1] for t in self.packeddata]
        self.ppindexlist = [t[2] for t in self.packeddata]
        self.labellist = [t[3] for t in self.packeddata]
        self.rawsentences = [t[5] for t in self.packeddata]


    def makefeatures(self, sents_list):
        """
        ARGS
            sent_list: [[s1word1,s1word2,...], [s2word1,s2word2,...],...]
        RETURNS
            _features: a list of feature set (dict)
        """
        _features = []
        for sent, ppindex in zip(sents_list, self.ppindexlist):
            fe = FeatureExtractor(sent, ppindex, "pos", "ngram")
            _features.append(fe.features())
        return _features


    def train(self, numexamples = 1400, numiter = 20):
        trainset_features = self.makefeatures(self.gold_words[:numexamples])
        trainset_labels = self.labellist[:numexamples]
        trainset = zip(trainset_features, trainset_labels)
        classifier = nltk.MaxentClassifier.train(trainset, algorithm="IIS", max_iter=numiter)
        self.classifier = classifier
        self.numexamples = numexamples


    def test(self):
        """
        TODO
            output logfile and confusion matrix for debugging
        """
        classifier_outputs = []
        ns = self.numexamples
        testset_features = self.makefeatures(self.test_words[ns:])
        testset_labels = self.labellist[ns:]
        testset_rawsents = self.rawsentences[ns:]
        testset = zip(testset_features, testset_labels)
        print "Accuracy on the test set:", nltk.classify.accuracy(self.classifier, testset)
        print "Most informative features:\n", self.classifier.show_most_informative_features(n=10)
        classifier_outputs = [self.classifier.classify(test) for test in testset_features]
        self.failedcases = [testset_rawsents[i] for i,w 
                            in enumerate(zip(testset_labels, classifier_outputs))
                            if w[0] != w[1] ]
        self.cm = nltk.ConfusionMatrix(testset_labels, classifier_outputs)
        print self.cm



    def log(self, filename):
        with open(filename, "w") as logfile:
            logfile.write("FAILED CASES:\n")
            for item in self.failedcases:
                logfile.write(item+"\n")

def main():
    st = time.time()
    print "Started...\nReading corpus..."
    pc = PrepChecker("packedcorpus.pkl")
    print "Training..."
    trnum = len(pc.labellist)-100
    pc.train(numexamples=trnum, numiter=20)
    print "done!"
    print "Testing..."
    pc.test()
    et = time.time()
    print "Overall...%5.3f [sec.]"%(et-st)
    pc.log("log.txt")




if __name__=="__main__":
    main()

