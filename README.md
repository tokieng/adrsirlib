# adrsirlib
ビットトレードワン製 ADRSIR 用をPythonから簡単に使うためのライブラリです。   

## ADRSIRとは
　Raspberry Piに取り付けて、Raspberry Piを学習リモコンにするという、ビットトレードワンの製品です。   
　http://bit-trade-one.co.jp/product/module/adrsir/

## ファイルについて
  * adrsirlib.py : ライブラリ本体
  * ircontrol    : ライブラリの使用例。コマンドライン上で簡単な操作を行えます。

## ライブラリの説明
2つの関数があるだけです。
  * get(no)
  指定した番号(0～19)のボタンでADRSIRが記憶している、赤外線データを取り込みます。   
  結果は16進数の文字列に変換して返します。
  * send(ir_str_data)
  get()で取得した赤外線データの文字列を、ADRSIRに赤外線送信させます。

## ライブラリの簡単な使い方
```python
import adrsirlib as ir
str = ir.get(0)  # ボタン0のデータを取り込む
ir.send(str)     # そのデータを赤外線送信する
```

## ircontrolの使い方
`./ircontrol <コマンド> [<オプション>...]`
* storeコマンド
ADRSIRから赤外線データを取り込み、ファイルに保存します。   
オプションに、ボタン番号とファイル名を、0:filename のようにコロンで区切って指定します。複数指定できます。   
例: `./ircontrol store 0:power 1:volume_up 2:volume_down`
* sendコマンド
保存した赤外線データを、ADRSIRに送信させます。   
オプションには、保存したファイル名を指定します。1つだけ指定します。   
例: `./ircontrol send power`
* listコマンド
保存した赤外線データの一覧を表示します。   
例: `./ircontrol list`

## もしかしたら
Raspberry Pi 1では、adrsirlib.pyを書き換えないと動かないかも？
```
bus = smbus.SMBus(1)
↓
bus = smbus.SMBus(0)
```

## 参考文献
ビットトレードワンによる以下のブログ記事を参考にしました。   
http://bit-trade-one.co.jp/blog/2017121302/

## ライセンス
切ったり貼ったり、お好きに使ってください。
いちおうMITライセンスってしておきますが、著作権表記等も一切不要です。
