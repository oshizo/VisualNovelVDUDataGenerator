# VisualNovelVDUDataGenerator

日本語ビジュアルノベルゲーム画像の合成データジェネレータ

## 目的
OCRなどVisual document understanding (VDU)の学習用テキスト画像サンプルの生成。
日本語のみを対象にしています。

## 使用方法

### Google Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/oshizo/VisualNovelVDUDataGenerator/blob/main/example_colab.ipynb)

### ローカル

```
git clone https://github.com/oshizo/VisualNovelVDUDataGenerator.git
pip install -r requirements.txt
pip install jupyter
```

環境構築後、`example.ipynb`を実行してください。

モデルのトレーニングループの中で動的にデータを生成することを目的として実装したため、バッチ生成するためのCLIは用意していません。

## 仕組み
コア部分は[Belval/TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator)を参考に実装しています。
PIL.ImageDrawを使って動的に画像を生成します。

表示するテキストやキャラクターの名前は、`texts/message_samples.csv`と`texts/name_samples.csv`から取得しています。

このファイルに追記するか、example.ipynbのファイル読み込み部分を好きな方法に変更してください。

背景画像やキャラクター画像、フォントファイル（.ttfまたは.otf）を複数用意することでより多様な画像を生成できます。


## 生成可能なバリエーションと生成画像のサンプル

現在のバージョンでは、キャラクターの名前を0～1つ、メッセージを0～1つ、選択肢を0～N個持つ画像を生成できます。

また、テキストにはルビを表示することができます。
ルビをレンダリングするためのフォーマットは以下のようなHTMLタグの形式です。

```ルビを表示したいときの<ruby>例<rt>れい</rt></ruby>です。```

ただし、`<ruby>`タグの中に複数の`<rt>`タグを含む形式はサポートしていないため、以下のように`<ruby>`タグを複数回使用する必要があります。

```<ruby>複数<rt>ふくすう</rt></ruby>の箇所にルビを表示したいときの<ruby>例<rt>れい<rt><ruby>です。```


## ライセンス

ソースコードのライセンスはMITですが、`fonts/BIZUDGothic-Bold.ttf`はSIL OPEN FONT LICENSEに従います。

このことを明示するため、[googlefonts/morisawa-biz-ud-gothic](https://github.com/googlefonts/morisawa-biz-ud-gothic)の`OFL.txt`を`fonts/OFL.txt`にコピーしています。


### 生成画像の例
![sample_01](https://raw.githubusercontent.com/oshizo/VisualNovelVDUDataGenerator/main/sample_outputs/sample_01.png)
![sample_02](https://raw.githubusercontent.com/oshizo/VisualNovelVDUDataGenerator/main/sample_outputs/sample_02.png)
![sample_03](https://raw.githubusercontent.com/oshizo/VisualNovelVDUDataGenerator/main/sample_outputs/sample_03.png)

