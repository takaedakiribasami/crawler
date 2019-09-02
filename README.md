# crawler

## 動作環境
- Ubuntu18.04LTS
- Mozilla Firefox 68.0.2
- pipenv, version 2018.11.26
- Tshark 2.6

## 導入手順
```
$ git clone https://github.com/takaedakiribasami/crawler.git crawler
$ cd crawler
$ pipenv install
```

```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install wireshark
$ sudo usermod -aG wireshark (your_user_name)
```

## 使い方
```
$ pipenv shell
$ python main.py (URL) (output_directory)
```
