# write_recognition

文字を書いた時の筋電信号を計測し．その信号から書いた文字を認識する  
今回は数字（0~9）を使用  
過去は一文字までしか使用できなかったが，CTC（音声認識アルゴリズム）を用いることによって複数桁に応用が可能となった  

### アイデア
過去までの数字記述時動作推定は一文字単位でしか推定を行えていないという背景があった．  
それには数字と数字の間に準備動作が含まれていることが理由としてあった．  
そこで似た課題を抱えていた音声認識問題で課題解消に用いられた，「CTC」と呼ばれるアルゴリズムを筋電信号に応用した  
それでも以前よりは課題が解消されたが，計測結果の安定性が欠けるという問題があった．  
そこで文字書く際の動作を「要素動作」に分割し，要素動作を１単位として推定を行うことで安定性と精度の両面で効果がみられた．  
  
要素動作例  
7 ：　左上に縦棒を書く　→　次の動作開始位置まで移動　→　横棒を書く　→　左下に斜め棒を書く

筋電信号は8chで計測  
指先で複数桁の数字を区切りなしで中空に記述し，その時の筋電信号を計測（0~9999まででランダム生成）  
実行は数字の順番

## 1_prepare
データを整形して学習用のデータセットを作成

## 2_compute_features
短時間フーリエ変換を用いて，時系列情報を内包した周波数特性を求める

## 3_ctc_earlyfusion
ctcを用いて学習を行う
一動作を要素動作ごとに推定する手法と数字ごとに推定する手法両方について学習を行うことができる

## number_check
各数字の周波数特性をプロットすることができる  
要素動作分割の際に，各数字がどのような周波数特性を持っているかを確認するために使用した  

＜参考＞  
高島遼一，Pythonで学ぶ音声認識　機械学習実践シリーズ，株式会社インプレス，2021
