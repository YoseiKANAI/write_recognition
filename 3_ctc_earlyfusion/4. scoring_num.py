# -*- coding: utf-8 -*-

#
# 認識結果と正解文を参照して，認識エラー率を計算
# num単位での結果
#

# 認識エラー率を計算するモジュールをインポート
import levenshtein


import os
import sys


if __name__ == "__main__":

    # トークンの単位
    # 数字　: num
    # 要素　：　ele
    unit = 'ele'

    # 実験ディレクトリ
    exp_dir = './exp_train'

    # デコード結果が格納されているディレクトリ
    decoded_dir = os.path.join(exp_dir,
                               unit+'_model_ctc',
                               'decode_test')

    # 認識結果が記述されたファイル
    hypothesis_file = os.path.join(decoded_dir, 'hypothesis.txt')

    # 正解文が記述されたファイル
    reference_file = os.path.join(decoded_dir, 'reference.txt')

    # エラー率算出結果を出力するディレクトリ
    out_dir = decoded_dir

    # エラー率算出結果の出力ファイル
    result_file = os.path.join(out_dir, 'result_num.txt')

    # 出力ディレクトリが存在しない場合は作成する
    os.makedirs(out_dir, exist_ok=True)

    # 各誤りの総数(エラー率算出時の分子)
    total_err = 0
    total_sub = 0
    total_del = 0
    total_ins = 0
    # 正解文の総文字数(エラー率算出時の分母)
    total_length = 0

    # 各ファイルをオープン
    with open(hypothesis_file, mode='r') as hyp_file, \
         open(reference_file, mode='r') as ref_file, \
         open(result_file, mode='w') as out_file:
        # 認識結果ファイル正解文ファイルを一行ずつ読み込む
        for line_hyp, line_ref in zip(hyp_file, ref_file):
            # 読み込んだ行をスペースで区切り，リスト型の変数にする
            parts_hyp = line_hyp.split()
            parts_ref = line_ref.split()

            # 発話ID(partsの0番目の要素)が一致しているか確認
            if parts_hyp[0] != parts_ref[0]:
                sys.stderr.write('Utterance ids of '\
                    'hypothesis and reference do not match.')
                exit(1)

            hypothesis = []
            reference  = []

            str_hyp = "".join(parts_hyp[1:])
            str_ref = "".join(parts_ref[1:])

            # 要素を数字に変換する（出力）
            str_hyp = str_hyp.replace('fbcgf','8')
            str_hyp = str_hyp.replace('iacb','5')
            str_hyp = str_hyp.replace('hbfa','4')
            str_hyp = str_hyp.replace('ckla','9')
            str_hyp = str_hyp.replace('efag','3')
            str_hyp = str_hyp.replace('bfia','7')
            str_hyp = str_hyp.replace('bga','2')
            str_hyp = str_hyp.replace('da','1')
            str_hyp = str_hyp.replace('ac','0')
            str_hyp = str_hyp.replace('aj','6')

            str_hyp = str_hyp.replace('a','-').replace('b','-').replace('c','-').replace('d','-').replace('e','-').replace('f','-').replace('g','-').replace('h','-').replace('i','-').replace('j','-').replace('k','-').replace('l','-')
            # 一つ前フレームの文字番号
            prev_token = -1
            # フレーム毎の出力文字系列を前から順番にチェックしていく
            for n in str_hyp:
                if n != prev_token:
                    # 1. 前フレームと同じトークン
                    if n != '-':
                        # 2. かつ，blank(番号=0)ではない
                        # --> token_listから対応する文字を抽出し，
                        #     出力文字列に加える
                        hypothesis.append(n)
                    # 前フレームのトークンを更新
                    prev_token = n

            # 要素を数字に変換する（正解データ）
            str_ref = str_ref.replace('fbcgf','8')
            str_ref = str_ref.replace('iacb','5')
            str_ref = str_ref.replace('hbfa','4')
            str_ref = str_ref.replace('ckla','9')
            str_ref = str_ref.replace('efag','3')
            str_ref = str_ref.replace('bfia','7')
            str_ref = str_ref.replace('bga','2')
            str_ref = str_ref.replace('da','1')
            str_ref = str_ref.replace('ac','0')
            str_ref = str_ref.replace('aj','6')
            str_ref = str_ref.replace('a','-').replace('b','-').replace('c','-').replace('d','-').replace('e','-').replace('f','-').replace('g','-').replace('h','-').replace('i','-').replace('j','-').replace('k','-').replace('l','-')
            # 一つ前フレームの文字番号
            prev_token = -1
            # フレーム毎の出力文字系列を前から順番にチェックしていく
            for n in str_ref:
                if n != prev_token:
                    # 1. 前フレームと同じトークン
                    if n != '-':
                        # 2. かつ，blank(番号=0)ではない
                        # --> token_listから対応する文字を抽出し，
                        #     出力文字列に加える
                        reference.append(n)
                    # 前フレームのトークンを更新
                    prev_token = n


            # 誤り数を計算する
            (error, substitute, delete, insert, ref_length) \
                = levenshtein.calculate_error(hypothesis,
                                              reference)

            # 総誤り数を累積する
            total_err += error
            total_sub += substitute
            total_del += delete
            total_ins += insert
            total_length += ref_length

            # 各発話の結果を出力する
            out_file.write('ID: %s\n' % (parts_hyp[0]))
            out_file.write('#ERROR (#SUB #DEL #INS): '\
                '%d (%d %d %d)\n' \
                % (error, substitute, delete, insert))
            out_file.write('REF: %s\n' % (' '.join(reference)))
            out_file.write('HYP: %s\n' % (' '.join(hypothesis)))
            out_file.write('\n')

        # 総エラー数を，正解文の総文字数で割り，エラー率を算出する
        err_rate = 100.0 * total_err / total_length
        sub_rate = 100.0 * total_sub / total_length
        del_rate = 100.0 * total_del / total_length
        ins_rate = 100.0 * total_ins / total_length

        # 最終結果を出力する
        out_file.write('------------------------------'\
            '-----------------------------------------------\n')
        out_file.write('#TOKEN: %d, #ERROR: %d '\
            '(#SUB: %d, #DEL: %d, #INS: %d)\n' \
            % (total_length, total_err,
               total_sub, total_del, total_ins))
        out_file.write('TER: %.2f%% (SUB: %.2f, '\
            'DEL: %.2f, INS: %.2f)\n' \
            % (err_rate, sub_rate, del_rate, ins_rate))
        print('TER: %.2f%% (SUB: %.2f, DEL: %.2f, INS: %.2f)' \
            % (err_rate, sub_rate, del_rate, ins_rate))
        out_file.write('------------------------------'\
            '-----------------------------------------------\n')
