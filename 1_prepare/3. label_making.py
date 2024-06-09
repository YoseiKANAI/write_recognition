# -*- coding: utf-8 -*-

#
# ダウンロードしたラベルデータを読み込み，
# textファイルの作成
#　データのIDとラベルを記載したラベルファイル

import yaml
import os
from sys import exit
#
# メイン関数
#
if __name__ == "__main__":

    # 総被験者数
    sub_num = 20
    # アテンプト数
    attempt = 20
    # 総データ数
    data_num = sub_num * attempt

    # ダウンロードしたラベルデータ(yaml形式)
    original_label = \
      '../data/data/label.yaml'

    # ラベルのリストを格納する場所
    out_label_dir = '../data/label/all'

    # 出力ディレクトリが存在しない場合は作成する
    os.makedirs(out_label_dir, exist_ok=True)

    # ラベルデータを読み込む
    # mode = 'r'　・・・　読み込みで開く
    # yaml.safe_load() ・・・　yamlファイルを辞書型ファイルとして読み込む
    with open(original_label, mode='r') as yamlfile:
        label_info = yaml.safe_load(yamlfile)

    # ラベルファイルを書き込みモードで開く
    with open(os.path.join(out_label_dir, 'num'), mode='w') as label_num,\
        open(os.path.join(out_label_dir, 'ele'), mode='w') as label_ele:

        # 総データ数だけ処理を繰り返し実行
        for i in range(data_num):
            # 発話ID
            filename = 'data_%04d' % (i+1)

            # 発話ID が label_info に含まれない場合はエラー
            if not filename in label_info:
                print('Error: %s is not in %s' % (filename, original_label))
                exit()

            # ラベル情報を取得
            num = label_info[filename]['num']
            ele = label_info[filename]['ele']


            # ラベルファイルへ，1文字ずつスペース区切りで書き込む
            # (' '.join(list) は，リストの各要素にスペースを挟んで，1文にする)
            label_num.write('%s %s\n' % (filename, ' '.join(num)))
            # 要素ラベルは，'-'をスペースに置換して書き込む
            label_ele.write('%s %s\n' % (filename, ele.replace('-',' ')))
