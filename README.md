# ss2012: Python/NLTKでつくる英語前置詞誤り訂正器

## Requirements
* **Python 2.7.x**
    * 2.6.xではfeature_extractor.py中のdict comprehensionが機能しません
    * 3.x にはNLTKおよびNumpyが対応しておりません
* **NLTK 2.0.1 or above**
* **Numpy 1.6 or above**
    * Scipyは要りません (MaxEntClassifierでBFGS等のアルゴリズムを使うなら必要ですが)


## タスク：「検出済みチェックポイントの訂正」
* 前置詞誤りは検出済みとする
* 対象とする前置詞:
    * "in", "for", "at", "on", "of", "about", "with", "from", "by", "as", "into"
    * "to"はTreebankのPOSタグに不定詞なども含まれているため, 今のところ除外.
* 複合誤りや上記以外の前置詞を含む文を除くと, 全部で1582文となった.


##中身
###ss2012_slide
* 説明用スライド(途中)
* pptx形式が最新版です

<!--
###wdiff_prep
* CLC-FCEデータセットから得た訂正情報をwdiffの形式で付与したもの．
* 1パラグラフ1行．
* 今回は前置詞誤り以外の部分は正しい候補を入れてある．

>@keiskSさんありがとうございました!!!!

-->

###preprocessor.py
* 中身は見ないでください．
* `wdiff_prep`をdict型のリストへ落とし込むスクリプト．

###prepchecker.py
* 本体  
* nltk.MaxentClassifier を用いた多クラス分類問題として,最尤の訂正候補を選ぶ

###feature_extractor.py
* class FeatureExtractor
* nltk.word_tokenize によって単語単位のリスト化された文に対して素性抽出をおこない，素性集合(dict)を返す．

####素性
* ngram: 前後数単語の表層形(lemmatizeなし)
* posngram: それらの品詞(nltk.pos_tagによる,TreeBank形式のタグセット)

##Usage

    $git clone git://github.com/tuxedocat/ss2012.git
    $cd ss2012
    $python preprocessor.py
    $python prepchecker.py

###出力
* 評価はaccuracy
    * 前置詞誤り箇所は特定済みであるとしているから
* nltk.ConfusionMatrixによる混同行列(行:正解ラベル, 列:分類器出力ラベル)

##TODO
1. デバッグ用出力をつける
1. マシな素性のサンプルコードをつける

