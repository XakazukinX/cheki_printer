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

### ~~instax-api を入れる~~
```
~~pip3 install instax-api~~
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

## License
### instax_api
MIT License

Copyright (c) 2016 James Sutton

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.