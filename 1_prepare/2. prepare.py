# -*- coding: utf-8 -*-

# signal.scpファイルの作成
# 信号データのファイルとそのパスを記載したファイル

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

    # csvファイルが展開されたディレクトリ
    original_csv_dir = '../data/data'

    # csvデータのリストを格納するディレクトリ
    out_scp_dir = '../data/label/all'

    # 出力ディレクトリが存在しない場合は作成する
    os.makedirs(out_scp_dir, exist_ok=True)

    # csvデータのリストファイルを書き込みモードで開き，以降の処理を実施する
    with open(os.path.join(out_scp_dir, 'signal.scp'), mode='w') as scp_file:
        # testのdata_01~10 に対して処理を繰り返し実行
        for i in range(data_num):
            filename = 'data_%04d' % (i+1)
            # オリジナルデータ(csv)のファイル名
            csv_path = os.path.join(original_csv_dir, filename+'.csv')

            print(csv_path)
            # ファイルが存在しない場合はエラー
            if not os.path.exists(csv_path):
                print('Error: Not found %s' % (csv_path))
                exit()

            # csvファイルのリストを書き込む
            scp_file.write('%s %s\n' %
                           (filename, os.path.abspath(csv_path)))
