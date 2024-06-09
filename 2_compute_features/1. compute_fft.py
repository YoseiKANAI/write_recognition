# -*- coding: utf-8 -*-

#
# 特徴量をFFTを用いて計算する
#

import numpy as np
import pandas as pd
import os
import sys
from scipy import signal

#　データを２次元のデータから３次元のデータ（短時間FFT用）に変換する
def _arange_data_(data, n_prev, n_intvl):
    """
    data should be pd.DataFrame()
    """
    dataX = pd.DataFrame()
    docX  = []
    ii = 0
    i2 = data.shape[1]#電極のchの数になる
    for i in range(64, len(data), n_intvl):

        # iから64さかのぼった値からiまでのデータを抽出し，そこにハミング窓をかける
        # その後iに25(n_intvl)を足して同じことをする
        # それをiがデータの長さ(len)に到達するまで繰り返す
        # その後そのデータを繰り返しの回数ii個の行列にし，ii×64×8chのデータにする
        dataX = data.iloc[i-n_prev:i]
        for k in range(i2):
            # 直流成分をカットする
            dataX.iloc[:,k] = dataX.iloc[:,k] - np.mean(dataX.iloc[:,k])
            # ハミング窓をかける
            dataX.iloc[:,k] *= np.hamming(n_prev)
        # dataXをdocXに結合する
        docX.append(dataX.values)
        # 繰り返しの階数をカウント（０軸の大きさになる）
        ii+=1
    alsX = np.array(docX).reshape(ii, n_prev, i2)
    return alsX

# バンドパスフィルタ　（信号，サンプリング周波数，下限，上限，次数）
def bpf(wave, fs, fe1, fe2, n):
    nyq = fs / 2.0
    b, a = signal.butter(1, [fe1/nyq, fe2/nyq], btype='band')
    for i in range(0, n):
        wave = signal.filtfilt(b, a, wave)
    return wave

#
# メイン関数
#
if __name__ == "__main__":

    # ファイルの設定を行う
    train_csv_scp = '../data/label/train/signal.scp'
    train_out_dir = './fft/train'
    dev_csv_scp = '../data/label/dev/signal.scp'
    dev_out_dir = './fft/dev'
    test_csv_scp = '../data/label/test/signal.scp'
    test_out_dir = './fft/test'

    # ch数
    ch = 8
    # サンプリング周波数 [Hz]
    sample_frequency = 2500
    # フレーム長
    # FFT用フレームサイズ
    frame_length = 64
    # フレームシフト
    frame_shift = 25

    # csvファイルリストと出力先をリストにする
    csv_scp_list = [train_csv_scp,
                    dev_csv_scp,
                    test_csv_scp]
    out_dir_list = [train_out_dir,
                    dev_out_dir,
                    test_out_dir]

    # 各セットについて処理を実行する
    for (csv_scp, out_dir) in zip(csv_scp_list, out_dir_list):
        print('Input signal_scp: %s' % (csv_scp))
        print('Output directory: %s' % (out_dir))

        # 特徴量ファイルのパス，フレーム数，
        # 次元数を記したリスト
        feat_scp = os.path.join(out_dir, 'feats.scp')

        # 出力ディレクトリが存在しない場合は作成する
        os.makedirs(out_dir, exist_ok=True)

        # signal.scpを読み込みモード、
        # 特徴量リストを書き込みモードで開く
        with open(csv_scp, mode='r') as file_csv, \
                open(feat_scp, mode='w') as file_feat:
            # csvリストを1行ずつ読み込む
            for line in file_csv:
                # 各行には，発話IDとcsvファイルのパスが
                # スペース区切りで記載されているので，
                # split関数を使ってスペース区切りの行を
                # リスト型の変数に変換する
                parts = line.split()
                # 0番目が発話ID
                utterance_id = parts[0]
                # 1番目がcsvファイルのパス
                csv_path = parts[1]

                # 与えられたパスに存在するcsvファイルを読み込み，特徴量を計算する
                csv = pd.read_csv(csv_path, index_col = False)
# 8chを7chに縮小
#                csv.loc[:,['CH1','CH2','CH3','CH4','CH6','CH7','CH8']]

                # ここでバンドパスを通す　5~500Hzが筋電の有効範囲
                for i in csv:
                    csv[i] = bpf(csv[i], sample_frequency, 5, 500, 5)

                # 短時間フーリエ変換用にデータを並べ替える df = frame_len×128×8ch
                df = _arange_data_(csv, frame_length, frame_shift)
                #　fftを行う  FFT = 927×128×8
                FFT = np.fft.fft(df, axis=1)
                # もしデータをearly fusionするならこうする？
                # だけど標準偏差もまとめて計算されてしまう可能性あり
                # ここは別々にしておいたほうが良い？

                # 振幅スペクトルを求める  Amp_spectrum = num_frame×75×8
                Amp_spectrum = np.abs(FFT*2 / FFT.shape[1])

                # パワースペクトルを計算する  power_spectrum = 927×75×8
#                power_spectrum = np.abs(FFT) ** 2
                # 線対象になっているので，右半分を削除
                # 要素数を必要範囲に絞る
                spectrogram = Amp_spectrum[:, 0:20, :]

                # 特徴量のフレーム数と次元数を取得
                # 次元数は8ch分なので8をかけておく？
                num_frames = len(FFT)
                num_dims   = spectrogram.shape[1]

                # 特徴量ファイルの名前(splitextで拡張子を取り除いている)
                out_file = os.path.splitext(os.path.basename(csv_path))[0]
                out_file = os.path.join(os.path.abspath(out_dir),
                                        out_file + '.npy')

                # データをfloat32形式に変換
                spectrogram = spectrogram.astype(np.float32)

                # データをファイルに出力
                # 配列の内容をout_file(binファイルに書き出している)
#                spectrogram.tofile(out_file)
                # np.saveを使うときは，上の'bin'を'npy'にしておく必要あり
                np.save(out_file, spectrogram)
                # 発話ID，特徴量ファイルのパス，フレーム数，
                # 次元数を特徴量リストに書き込む
                file_feat.write("%s %s %d %d\n" %
                    (utterance_id, out_file, num_frames, num_dims))
