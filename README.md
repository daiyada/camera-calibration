# Camera-Calibration
カメラキャリブレーションに必要な画像群の切り出し、キャリブレーション用のパラメータの算出、動画や画像への適用を行う

## 使用方法
### 1. 環境構築  
```
$ pip install -r requirements.txt
```
### 2. 以下スクリプトを順に実行  
【注意】以下スクリプトと同名のyamlファイルが ***config/*** に格納されているため、**実行前に値を設定**する
- movie2img.py / 【設定ファイル】： config/movie2img.yaml  
カメラキャリブレーションのparamを算出するのに用いる画像（チェッカーボード）を切り出す。/***imgs_for_calc_param/*** に切り出した画像が出力される

- calc_camera_param.py / 【設定ファイル】： config/calc_camera_param.yaml  
paramを算出するのに用いる画像（チェッカーボード）からparamを算出する。算出したparamは***config/calibration_param.npz***に保存される

- calibration.py / 【設定ファイル】： config/calibration.yaml  
特定の画像、動画に対して***config/calibration_param.npz***に格納したparamをもとにcalibrationを行う。出力データは　***after/***に格納される

### 3. サブスクリプト
- movie_cutter / 【設定ファイル】： config/movie_cutter_.yaml  
指定の範囲の動画を切り出す

## Calibration後出力イメージ
- 動画／calibration前後の動画をconcatenateしたもの
<video width="1280" height="480" controls>
  <source src="sample/concatenated_video_20210525_11.avi" type="video/avi">
</video>