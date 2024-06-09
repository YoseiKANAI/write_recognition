# -*- coding: utf-8 -*-

#
# データのリストを，学習/開発/評価用のデータセットに分割．
# ここでは，以下のように分割します．
# IDの末尾が0のデータ : 評価データ
#   　　　　  5　　　　　 : 開発データ
# それ以外のデータ    : 学習データ
#

# osモジュールをインポート
import os

#
# メイン関数
#
if __name__ == "__main__":

    # 全データが記述されているリストのパス
    all_dir = '../data/label/all'

    # 評価データが記述されたリストの出力先
    out_eval_dir = '../data/label/test'
    # 開発データが記述されたリストの出力先
    out_dev_dir = '../data/label/dev'
    # 学習データが記述されたリストの出力先
    out_train_dir = '../data/label/train'

    # 各出力ディレクトリが存在しない場合は作成
    for out_dir in [out_eval_dir, out_dev_dir,
                    out_train_dir]:
        os.makedirs(out_dir, exist_ok=True)

    # signal.scp, textにそれぞれに同じ処理を行う
    for filename in ['signal.scp', 'num', 'ele']:
        # 全データを読み込みモードで，/評価/開発/学習データリストを書き込みモードで開く
        with open(os.path.join(all_dir, filename),
                  mode='r') as all_file, \
                  open(os.path.join(out_eval_dir, filename),
                  mode='w') as eval_file, \
                  open(os.path.join(out_dev_dir, filename),
                  mode='w') as dev_file, \
                  open(os.path.join(out_train_dir, filename),
                  mode='w') as train_file:
            # 1行ずつ読み込み，評価/開発/学習データリストに書き込み
            for i, line in enumerate(all_file):
                if ( ((i+1)%10) == 0 ):
                    # IDの末が0のデータ: 評価データリストへ書き込み
                    eval_file.write(line)
                elif ( ((i+1)%5) == 0 ):
                    # IDの末が5のデータ: 開発データリストへ書き込み
                    dev_file.write(line)
                else:
                    # そのほかのデータ: 学習（大）データリストへ書き込み
                    train_file.write(line)
