#coding: utf-8

# ADRSIR用ライブラリ
#  Copyright 2018 tokieng
#  MIT License
#
# 準備: sudo apt-get install python3-smbus

## 参考文献
# http://bit-trade-one.co.jp/blog/2017121302/
# ビット・トレード・ワン社提供のラズベリー・パイ専用 学習リモコン基板(型番：ADRSIR)用のツール
#　著作権者:(C) 2015 ビット・トレード・ワン社
#　ライセンス: ADL(Assembly Desk License)


import smbus

# ADRSIRのI2Cアドレス
ADDR = 0x52

# コマンド群
R1_memo_no_write  = 0x15
R2_data_num_read  = 0x25
R3_data_read      = 0x35
W2_data_num_write = 0x29
W3_data_write     = 0x39
T1_trans_start    = 0x59

bus = smbus.SMBus(1)

def get(no):
	### ●赤外線データ長読み出し手順
	senddata = [no]
	bus.write_i2c_block_data(ADDR, R1_memo_no_write, senddata)
	data = bus.read_i2c_block_data(ADDR, R2_data_num_read, 3)  # data = [0, データ長H, データ長L]
	read_length = (data[1] << 8) + data[2]  # データのバイト数は、 read_length * 4 になる

	if read_length == 0xffff:
		return []

	### ●赤外線データ読み出し手順
	# 1バイト目は常に0が得られるっぽいから、読んで捨てる
	data = bus.read_i2c_block_data(ADDR, R3_data_read, 1)

	# read_length分繰り返す。
	ir_data = []
	for i in range(read_length):
		data = bus.read_i2c_block_data(ADDR, R3_data_read, 4) # 4バイトずつ読むらしい
		ir_data.extend(data)

	ir_str_data = ''
	for i in ir_data:
		ir_str_data += "{:02x}".format(i)
	return ir_str_data


def send(ir_str_data):

	ir_data = [int(ir_str_data[i:i+2],16) for i in range(0,len(ir_str_data),2)]

	# ●赤外線データ長書き込み手順
	data_length = len(ir_data)
	senddata = [data_length >> 8, data_length & 0xff]
	bus.write_i2c_block_data(ADDR, W2_data_num_write, senddata)

	# read_length分繰り返す。
	for i in range(0, data_length, 4):
		bus.write_i2c_block_data(ADDR, W3_data_write, ir_data[i:i+4]) # 4バイトずつ

	bus.write_i2c_block_data(ADDR, T1_trans_start, [0] )   #= 

#####

if __name__ == '__main__':
	str = get(0)
	print(str)
	send(str)
