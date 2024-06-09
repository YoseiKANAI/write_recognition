# -*- coding: utf-8 -*-

#
# wrsmで得たlabelのtxtファイルを一つにまとめて
# yamlファイルを作成する
#　

import yaml
import json
import os

#
# メイン関数
#
if __name__ == "__main__":

    # 総被験者数(セット数)
    sub_num = 20

    # アテンプト数
    attempt = 20
    j = 0

    # yamlファイル用の空の辞書
    yml = {}
    # 保存先のyamlファイル
    yaml_label = \
      '../data/data/label.yaml'

    # ラベルのリストを格納する場所
    out_label_dir = '../data/data'


    for i in range(sub_num):
        original_label = '../data/data/label_%02d.txt' % (i+1)
        # txtファイルを開き，yamlという辞書型オブジェクトにデータを格納していく
        with open(original_label, mode='r') as txt_file:
            for line in txt_file:
                j+=1
                data_ID = 'data_%04d' % (j)
                num = ''.join(line.split("\n"))

                # 要素を作成する
                ele = num.replace('1', 'd-a-')
                ele = ele.replace('2', 'b-g-a-')
                ele = ele.replace('3', 'e-f-a-g-')
                ele = ele.replace('4', 'h-b-f-a-')
                ele = ele.replace('5', 'i-a-c-b-')
                ele = ele.replace('6', 'a-j-')
                ele = ele.replace('7', 'b-f-i-a-')
                ele = ele.replace('8', 'f-b-c-g-f-')
                ele = ele.replace('9', 'c-k-l-a-')
                ele = ele.replace('0', 'a-c-')

                #　最後の-を削除
                ele = ele[:-1]

                # numが数字, unitは単位(後で書き込む)
                yml[data_ID] = {'ele':ele, 'num':num}

    # yamlに書き込んだデータをlabel.yamlに書き込む
    with open(yaml_label, mode='w') as yaml_file:
        yaml.dump(yml, yaml_file)
