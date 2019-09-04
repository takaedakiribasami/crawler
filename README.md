# crawler
Firefoxで指定されたURLにアクセスし、通信データをキャプチャする．
クローリングしながら通信データをキャプチャすることも可能．

## 動作環境
- Ubuntu18.04LTS
- Mozilla Firefox 68.0.2
- pipenv, version 2018.11.26
- Tshark 2.6

## 導入手順
```
$ git clone https://github.com/takaedakiribasami/crawler.git (インストール先ディレクトリ)
$ cd (インストール先ディレクトリ)
$ pipenv install
```

```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install wireshark
$ sudo usermod -aG wireshark (実行ユーザー)
```

## 使い方
```
$ cd (インストール先ディレクトリ)
$ pipenv shell
$ python main.py (URL) (出力先ディレクトリ)
```
