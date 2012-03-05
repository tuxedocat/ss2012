# ss2012: Python/NLTKでつくる英語前置詞誤り訂正器
##中身
###ss2012_slide
* 説明用スライド(途中)
* pptx形式が最新版です

###wdiff_prep
CLC-FCEデータセットから得た訂正情報をwdiffの形式で付与したもの．
1パラグラフ1行．
今回は前置詞誤り以外の部分は正しい候補を入れてある．

>@keiskSさんありがとうございました!!!!

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

