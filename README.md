# 勾配ブースティングを利用した、KPIに聞く特徴量のレコメンド

## 意思決定をサポートする機械学習の必要性

## ワトソンの料理の新しいレシピのレコメンドと基本は一緒

## 【実験】　jin115.comのコメント数をどんな単語で記述したら数が増えるか予想する
[jin115.comのデータセットをzip圧縮で17GByteもダウンロード](https://storage.googleapis.com/nardtree/jin115-20171125)してしまったので、何か有効活用できないかと考えていたのですが、難しく、なんともKPIという軸で定量化できないので、
ある記事に対してつく、コメント数を増やすには、どんな単語選択が適切かという軸に切り替えて、分析してみました。  

jin115.comでは、2chまとめが流行った時に大量のアクセスを受けていたという背景があり、近年では常には同じぐらいのユーザ数がいるわけではありません。  
(あとでここはフィルする)

## 前処理

**データセットダウンロード**  

[Google Cloud Strageに大容量のスクレイピング済みのデータセットをzip圧縮したもの](https://storage.googleapis.com/nardtree/jin115-20171125/jin115-20171125.zip)がありので、追試等が必要な方は参照してください。
```console
$ wget https://storage.googleapis.com/nardtree/jin115-20171125/jin115-20171125.zip
```

**htmlコンテンツから必要なarticle, commentの数, 日時, タイトルのパース**  

ダウンロード済みのhtmlコンテンツから予想の元となる説明変数（article, title, date）と、目的変数であるcomment数をパースします　　

この捜査自体が極めて重いので、[Google Data Strageからもダウンロード]()できます　　

```console
$ python3 parser.py --map1
```

**パースしたデータを分かち書きします**  

分かち書きして、形態素解析して、BoWとしてベクトル表現にできる状態にします  

```console
$ python3 wakati.py --all
```

**LightGBM, XGBoostで機械学習可能なデータセット(train, test)を作成します**  

まず最初に、予想するとしたKPIであるコメント数を予想するもモデルを構築することを目的とします　　

そのために、トレインとテストのデータセットを分割して、作成します
```console
$ python3 make_sparse.py --terms # uniq単語をカウント
$ 
```

**LightGBMで学習して、モデルを作成します**  
一般的に、言語のBoWは単語数に応じたベクトル時原まで拡大されますので、numpyなどで密行列で表現することには向いていません  
そのため、デフォルトでスパースマトリックスを扱え、CUI経由で学習できるLightGBMのバイナリを直接実行してモデルを作成します  
```console
$ lightgbm config=train.conf
```
(LightGBMのインストールは、[Github](https://github.com/Microsoft/LightGBM)からcloneして、cmake, make & sudo make installでシステムパスに追加しておくと便利です)

**特徴量重要度を確認する**  
Gradient Boosting Machine系の特徴量重要度は、必ずしも、事象を説明する特徴量が支配的に記述されるわけではないのですが、どんな特徴量が効いているのか参考適度になります。  
また、今回、どんな単語をアーティクルやタイトルに記述されていれば、KPIが向上するのかの選択候補を与えるために、これらの特徴量重要度が高い候補のものから与えます

## 特定の記事から、KPIを増加させるために、なんの単語群を選択すればいいのか

