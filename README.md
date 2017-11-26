# 勾配ブースティングを利用した、KPIに聞く特徴量のレコメンド

## 意思決定をサポートする機械学習の必要性

## ワトソンの料理の新しいレシピのレコメンドからの発送   
もともと、この考えは、シェフ・ワトソン[1]の全く新しい食材の組み合わせで美味しいと言われているレシピをレコメンドするという機能をリバースエンジニアリングして導いたものです  
IBMが長らく研究していたテーマとして、意味情報を演算可能にするというお題があったはずですが、これはちょっと別で、機械学習の最小化のアルゴリズムでいくつかこれとこれが同時に存在して、この量以下ならば、という膨大なルールセットを獲得し、その獲得した条件式が成立していれば、美味しいはずであるという発想に基づいているかと思います  
<p align="center">
  <img width="750px" src="https://user-images.githubusercontent.com/4949982/33238374-c5b682d4-d2cf-11e7-8a1e-b25aca799d3b.png">
</p>
何品か、最初の条件となる、食品を選んで、他の何品かのレシピを自動でレコメンドします。  

## 【実験】　jin115.comのコメント数をどんな単語で記述したら数が増えるか予想する
[jin115.comのデータセットをzip圧縮で17GByteもダウンロード](https://storage.googleapis.com/nardtree/jin115-20171125)してしまったので、何か有効活用できないかと考えていたのですが、難しく、なんともKPIという軸で定量化できないので、
ある記事に対してつく、コメント数を増やすには、どんな単語選択が適切かという軸に切り替えて、分析してみました。  

jin115.comでは、2chまとめが流行った時に大量のアクセスを受けていたという背景があり、近年では常には同じぐらいのユーザ数がいるわけではありません。  
各月のユーザのコメント数を累積していくと、このようなグラフを書くことができました（2006年からやっているんですね。。すごい）
<p align="center">
  <img width="700px" src="https://user-images.githubusercontent.com/4949982/33239233-bc51b78e-d2e0-11e7-9f03-51dc78f02e18.png">
</p>

## 前処理

**データセットダウンロード**  

[Google Cloud Strageに大容量のスクレイピング済みのデータセットをzip圧縮したもの](https://storage.googleapis.com/nardtree/jin115-20171125/jin115-20171125.zip)がありので、追試等が必要な方は参照してください。
```console
$ wget https://storage.googleapis.com/nardtree/jin115-20171125/jin115-20171125.zip
```

**htmlコンテンツから必要なarticle, commentの数, 日時, タイトルのパース**  

ダウンロード済みのhtmlコンテンツから予想の元となる説明変数（article, title, date）と、目的変数であるcomment数をパースします　　

この捜査自体が極めて重いので、[Google Data Strageからもダウンロード](https://storage.googleapis.com/nardtree/jin115-20171125/contents.zip)できます　　

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
ここまでとても長かったのですが、ここからが本番で、クリエイティブを作る人は、書きかけの記事の単語選択や、表現に迷うことがあります。  

一般的に単語や表現は組み合わせで初めて、価値を発揮することが多く、経験則的にはこのようなクリエイティブはKPIが異なるとされています  

```json
[もちもち　した　美肌　！　今なら　、　キャンペーン　で　送料　無料　！] 
```
```json
[もちもち　した　食感　！　北海道産　、　まんじゅう　！　美味しい　！]
```
liblinearや単純な重回帰では、「もちもち」は単独の特徴量として表現されて、「もちもち」＋　「美容」　と「もちもち」＋「食べ物」の組み合わせることで、別の特徴量だと考慮すべき点は見ることができません  

Gradient Boosting MachineやDeep Learningなどは、内部的に組み合わせ表現を多角的に獲得可能なので、「美容」のクリエイティブを作成している時に、「美容」という制約が入った状態で、最適などの単語を使うべきかをレコメンド可能になります  

**元となるテキストをベクトル化する**  
デフォルトでは、学習データセットに用いなかったjin115.comの最新の記事を参照するようにしていますが、適宜必要なデータセットに変えてください
```console
$ python3 make_init.py
```

**モデルで判別するために獲得された単語群を作成する**
この単語があるから、KPIが変わった、という単語の一覧を得て、その単語群を組み合わせることで、よくなるのか、悪くなるか計算することができます  
```console
$ python3 check_importance.py
```

**単語群を利用して、ランダムの組み合わせ表現100,000通りを作成する**  
レコメンドの候補となる単語群の組み合わせ10万通りを計算して、データセットを作成します  
```console
$ python3 calc_combinations.py  > dump.dat
```

**前処理で学習したモデルを利用して、KPI増加量が多い単語の組み合わせ表現を、昇順でランキングします**  
```console
$ python3 upper_calc.py | less
```
(この例では、コメントするユーザのハッシュ値も予想の重要な特徴量になってしまっているので、名詞のみのモデルでランキングしています)

## 参考文献
- [1] [www.ibm.chefwatson.com](https://www.ibmchefwatson.com/tupler#tupler%2F2305-0255-01624-01005%2F%2F%2F%2F%2F%2F0)
