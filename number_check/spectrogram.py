# -*- coding: utf-8 -*-

#
# スペクトログラムを作成して，周波数ごとに単位を作成する
# 色     :　振幅
# 縦軸   ： 時間方向（フレーム数）
# 横軸   ：　周波数
#

import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def _arange_data_(data, n_prev, n_intvl):
    """
    data should be pd.DataFrame()
    """

# range(a,b,c) aからbまでcごとに増える数字の構造体をつくる
# append(追加要素) 末尾に追加要素を付け加える
# lenに行列を渡すと行数が帰る
    dataX = pd.DataFrame()
    docX  = []# 空のリスト
    ii = 0
    i2 = data.shape[1]#電極のchの数になる
    for i in range(64, len(data), n_intvl):

        # iから128さかのぼった値からiまでのデータを抽出し，そこにハミング窓をかける
        # その後iに50(n_intvl)を足して同じことをする
        # それをiがデータの長さ(len)に到達するまで繰り返す
        # その後そのデータを繰り返しの回数ii個の行列にし，ii×128×8chのデータにする
        dataX = data.iloc[i-n_prev:i]
#        for k in range(i2):
            # 直流成分をカットする
#            dataX.iloc[:,k] = dataX.iloc[:,k] - np.mean(dataX.iloc[:,k])
            # ハミング窓をかける
#            dataX.iloc[:,k] *= np.hamming(n_prev)
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
    # 解析する数字 0~9を選択
    num = 9
    # サンプリング周波数 [Hz]
    sample_frequency = 2500
    # フレーム長
    # フレームサイズ
    frame_length = 64
    # フレームシフト
    frame_shift = 25


    file_name = './num/%d.csv' % (num)
#    file_name = '../data/data/data_0001.csv'
    E = pd.read_csv(file_name, index_col = False)

    # ここでバンドパスを通す　5~500Hzが筋電の有効範囲
    for i in E:
        E[i] = bpf(E[i], sample_frequency, 5, 500, 5)


    """
    # 波形を表示
    title_name = 'number : %d' % (num)

    plt.figure()
    plt.title(title_name)
    plt.plot(E)
    plt.yticks([-1.0, -0.5, 0.0, 0.5, 1.0])

    # プロットを保存する
    out_plot_signal = './plot/%d.png' % (num)
    plt.savefig(out_plot_signal)
    plt.show()
#    """

    # 短時間フーリエ
    # 短時間フーリエ変換用にデータを並べ替える df = frame_len×128×8ch
    df = _arange_data_(E, frame_length, frame_shift)
    FFT = np.fft.fft(df, axis=1)

    fft_size = frame_length
    num_frames = len(FFT)

    # スペクトログラムの行列を用意
    spectrogram = np.zeros((num_frames, int(fft_size/2)+1, 8))
    # 振幅スペクトルを求める  Amp_spectrum = num_frame×75×8
    absolute = np.abs(FFT*2 / FFT.shape[1])
    # 線対象になっているので，右半分を削除
    spectrogram = absolute[:, :int(fft_size/2) + 1, :]
    spectrogram = spectrogram[:, 0:20, :]

    # パワースペクトルを計算する  power_spectrum = 927×75×8
#    power_spectrum = np.abs(FFT) ** 2
#    spectrogram = power_spectrum
#    """
    title_name_s = 'spectrogram  number : %d' % (num)

    plt.figure()
    plt.rcParams["font.size"] = 12
    plt.ylabel('frequency', labelpad=-15)
    plt.xlabel('num_frame : %d' %(num_frames))
    plt.title(title_name_s)
    # 枠線削除
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    # 軸ラベル，補助線削除
    plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False,
                    bottom=False, left=False, right=False, top=False)

    # 8ch分のデータをすべてプロット
    for ch in range(8):
        # スペクトログラムをプロットする
        out = np.zeros((num_frames, int(fft_size/2)+1))
        out = spectrogram[:,-1::-1,ch]
        plt.subplot(8, 1, ch+1)
        # 枠線削除
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        # 軸ラベル，補助線削除
        plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False,
                        bottom=False, left=False, right=False, top=False)

        plt.ylabel('CH%d' % (ch+1), rotation=0,ha='right')
        plt.imshow(out.transpose())


    # プロットを出力するファイル(pngファイル)
    # 論文用にepsに変更
    out_plot_spec = './spectrogram/spectrogram_%d.eps' % (num)
    # プロットを保存する
    plt.savefig(out_plot_spec)
