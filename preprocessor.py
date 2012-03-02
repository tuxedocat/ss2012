# coding: utf-8

import nltk
from nltk.tag import pos_tag as tagger
from nltk.classify import maxent
import re
import timeit
import random
import cPickle as pickle


def read_corpus(path):
    """
    CLCのデータ(wdiff)を読み込み，学習データとテストデータを辞書のリストで返す関数．
    
    ARGS:
        path : path to wdiff file of CLC corpus, string
    RETURNS:
        annotatedcorpus : a list of dictionaries which contains infomation of each sentences
    """
    with open(path, 'r') as wdiff_file:
        rawtext = wdiff_file.read().strip("\n")
    all_sents = nltk.sent_tokenize(rawtext)
    
    # 今回は前置詞誤りの検出は行わず、すべての前置詞を対象にする．
    # つまり訂正対象は前置詞誤りを含む文のみであるため、それらを抽出する．

    filtered_sents = [s for s in all_sents if ("[-" and "{+" in s)]
    annotatedcorpus = [add_annotation(s) for s in filtered_sents if add_annotation(s)]
    return annotatedcorpus

    

def add_annotation(sentence):
    """
    wdiff形式のアノテーションから, 訂正情報,テスト文,トレーニング文を抽出する.

    ARGS:
        sentence    : wdiffを含む文
    RETURNS:
        sent_dict   : sent_dict.keys = [rawtext(wdiff文, str), test(テストデータ, str)
                      gold(トレーニングデータ, str), correction_pair(訂正前後の前置詞ペア, tuple)
    """
    # 対象とする前置詞のリスト
    PREPS = ["in", "for", "at", "on", "of", "about", "with", "from", "by", "as", "into"]

    sent_dict = {}
    pattern = re.compile(r'(\[-(?P<i>.+)-\])\s*((\{\+(?P<c>.+)\+\}))?')
    correction_pairs = [m.groupdict() for m in pattern.finditer(sentence)]
    if correction_pairs:
        try:
            sent_dict["rawtext"] = sentence
            for n, dic in enumerate(correction_pairs):
                i = dic["i"]
                c = dic["c"]
                if not "correction_pair" in sent_dict and (i in PREPS and c in PREPS):
                    sent_dict["correction_pair"] = (dic["i"],dic["c"]) 
                else:
                    raise TypeError
            incorrectsent, goldsent = remove_tags(sentence, correction_pairs)
            sent_dict["test"] = incorrectsent
            sent_dict["gold"] = goldsent
            return sent_dict
        except TypeError:
            pass 
    else:
        pass


def remove_tags(sentence, correction_pairs):
    """
    wdiff形式のアノテーションを削除して, 学習者文(incorrectsent)と全訂正済みの文(goldsent)を返す.

    ARGS:
        sentence : 文字列, 一文単位
        correction_pairs : 訂正情報を含む辞書
    RETURNS:
        incorrectsent   : 学習者の前置詞誤りを含む文, テストデータ用
        goldsent        : すべての誤りが訂正されている文, 学習データ用
    """
    incorrectsent = sentence
    goldsent = sentence
    try:
        for dic in correction_pairs:
            i = dic["i"]
            c = dic["c"]
            incorrectsent = incorrectsent.replace("[-%s-]"%i, i, 1).replace("{+%s+} "%c, "", 1)
            goldsent = goldsent.replace("[-%s-]"%i, c, 1).replace("{+%s+} "%c, "", 1)
    except:
       raise TypeError 
    return incorrectsent, goldsent

        
def main():
    path = "wdiff_prep"
    corpus = read_corpus(path)
    for item in corpus:
        print item
    print "Num. of sentences:", len(corpus)
    with open("packedcorpus.pkl", "wb") as pkl_s:
        pickle.dump(corpus, pkl_s)
    with open("packedcorpus.pkl", "rb") as pkl_l:
        dbg = pickle.load(pkl_l)
    print len(dbg)

if __name__=="__main__":
    main()

