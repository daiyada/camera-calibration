"""
@file movie2img.py
@brief 動画からキャリブレーションに回すための画像を切り出す

@author Shunsuke Hishida / created on 2021/05/26
"""
import os

import cv2
from tqdm import tqdm

from config.cfg_manager import ReadMovie2Img
from utils.path import ImgForCalibPathMaker


def cutIntervally(cap, start_time, end_time, output_number, ext):
    """
    @brief 一定間隔に切り出す
    """
    if not start_time < end_time:
        print("[ERROR]切り出し開始時間と切り出し終了時間の大小関係")
        raise Exception
    final_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    start_frame = start_time * fps
    end_frame = end_time * fps
    # 切り出し最終フレームの見直し
    if end_frame > final_frame:
        end_frame = final_frame
    # step: 切り出すフレーム間隔
    step = int((end_frame - start_frame) / output_number)
    for index, frame_num in enumerate(range(start_frame, end_frame, step), start=1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, img = cap.read()   # img: (numpy.ndarray)
        if ret:
            path_maker = ImgForCalibPathMaker(index, ext)
            save_path = path_maker.getPath
            cv2.imwrite(save_path, img)
        else:
            break
    cap.release()

def cutAll(cap, ext):
    """
    @brief 全フレーム切り出す
    """
    index = 1
    while True:
        ret, img = cap.read()
        if ret:
            path_maker = ImgForCalibPathMaker(index, ext)
            save_path = path_maker.getPath
            cv2.imwrite(save_path, img)
            index += 1
        else:
            break
    cap.release()

def cutImg():
    """
    @param movie_path (str) 動画ファイルのパス
    @param config (class) 出力する画像に関するオプション
    """
    config = ReadMovie2Img(ReadMovie2Img.getYamlPath())
    cap = cv2.VideoCapture(config.getInputPath)
    if not cap.isOpened():
        return
    """
    FIXME: 本当は総フレーム数を取得して、endtime(フレーム番号)が総フレーム数より
    大きい場合は、end_time = fps * 総フレーム数に書き換える処理を入れたいが、なぜか
    raspiカメラで撮影したデータは cap.get(cv2.CAP_PROP_FRAME_COUNT)で総フレーム数を取得できない
    よって現状はこの処理を省いている
    """
    # os.makedirs(output_dir, exist_ok=True)
    if config.getCutFlag:
        cutAll(cap, config.getExtension)
    else:
        cutIntervally(
                    cap,
                    config.getStartTime,
                    config.getEndTime,
                    config.getOutputNumber,
                    config.getExtension
                    )
    print("DONE")

if __name__ == "__main__":
    cutImg()
