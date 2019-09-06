# チェキ印刷バッチ処理システム

## How to Use

- Wi-Fi: INSTAX-XXXXXX に接続する
    - テプラで個体番号が書いてある
- files フォルダに画像を入れる
- 以下を叩く

```
python cheki_printer.py
```

## install in Mac

### Homebrew を入れる

https://brew.sh/index_ja を参考に以下を叩く

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### pipenv を入れる

Python バージョン管理等は pipenv が主流
https://qiita.com/propella/items/247beb6be15bdef66ecc
https://github.com/pypa/pipenv

```
brew install pipenv
```

`.bashrc` に以下を追加

```
eval "$(pipenv --completion)"
```

### Python 3.7 を入れる

```
pipenv --python 3.7
```

### 環境の中に入る

```
pipenv shell
```

### instax-api を入れる

```
pip3 install instax-api
```


# 仕様

## 要求

- フォルダの中の画像ファイルをすべて印刷する
- 用紙切れ対応もしたい

## 使い方

files フォルダ直下のすべての画像を印刷

```
python cheki_printer.py
```

## 処理

files フォルダに `printout.log` を保存
ファイル名, ファイルハッシュを CSV 形式で記録
