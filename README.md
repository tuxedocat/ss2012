# ss2012: Python/NLTKでつくる英語前置詞誤り訂正器
##wdiff_prep
CLC-FCEデータセットから得た訂正情報をwdiffの形式で付与したもの．
1パラグラフ1行．
今回は前置詞誤り以外の部分は正しい候補を入れてある．

##preprocessor.py
中身は見ないでください．
`wdiff_prep`をdict型のリストへ落とし込むスクリプト．

##prepchecker.py
本体

##feature_extractor.py
POSタグ付けされた1文に対して素性抽出をおこない，dictを返す．

##classifier.py
`nltk.classify.maxent`を扱う．