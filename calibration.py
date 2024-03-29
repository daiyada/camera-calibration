"""
@file calibration.py
@brief 特定のデータに対してcalibrationを実施する

@author Shunsuke Hishida / created 2021/06/04
"""
import os

import cv2
from tqdm import tqdm

from utils.cfg_manager import CalibrationParameters, CalibrationMatrix
from utils.path import CalibedPathMaker
from utils.file_manager import FilePathGetter
from movie_cutter import setOutputFormat

class Calibration(object):

    @property
    def calibrated_img(self): return self.__calibrated_img

    def __init__(self):
        """Constructor"""
        self.__calib_param = CalibrationMatrix(CalibrationMatrix.get_npz_path())

    def execute(self, img):
        """
        @brief キャリブレーションを実行する
        @param img (numpy.ndarray) calibrationする画像
        """
        h, w, _ = img.shape
        dst = cv2.undistort(
                            img,
                            self.__calib_param.camera_matrix,
                            self.__calib_param.distortion,
                            None)
        self.__calibrated_img = dst

def set_format(movie, img, save_path):
    fourcc = int(movie.get(cv2.CAP_PROP_FOURCC))
    fps = int(movie.get(cv2.CAP_PROP_FPS))
    height, width, _ = img.shape
    new_movie = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
    return new_movie

def concatatenate_movie(movie1_path, movie2_path, save_path, left_title, right_title, color=(255,0,0)):
    """
    @param left_title (str) concatenateした際の左側動画タイトル
    @param right_title (str) concatenateした際の右側動画タイトル
    """
    movie1 = cv2.VideoCapture(movie1_path)
    movie2 = cv2.VideoCapture(movie2_path)
    format_flag = False
    while True:
        ret1, img1 = movie1.read()
        ret2, img2 = movie2.read()
        ret = ret1 and ret2
        if ret:
            cv2.putText(img1, left_title, (10, 30),
               cv2.FONT_HERSHEY_PLAIN, 1.5,
               color, 2, cv2.LINE_AA)
            cv2.putText(img2, right_title, (10, 30),
               cv2.FONT_HERSHEY_PLAIN, 1.5,
               color, 2, cv2.LINE_AA)
            img = cv2.hconcat([img1, img2])
            if not format_flag:
                concatanated_movie = set_format(movie1, img, save_path)
                format_flag = True
            concatanated_movie.write(img)
        else:
            break
    concatanated_movie.release()
    movie1.release()
    movie2.release()

def calibrate_movie(calib, path, save_path):
    """
    動画データをキャリブレーション
    """
    movie = cv2.VideoCapture(path)
    new_movie = setOutputFormat(movie, save_path)
    while True:
        ret, img = movie.read()
        if ret:
            calib.execute(img)
            calibrated_img = calib.calibrated_img
            new_movie.write(calibrated_img)
        else:
            break
    movie.release()
    new_movie.release()

def main():
    """メイン関数"""
    config = CalibrationParameters(CalibrationParameters.get_yaml_path())
    calib = Calibration()
    fpg = FilePathGetter(config.input_dir, config.extension)
    file_list = fpg.file_list
    for file_path in tqdm(file_list):
        cpm = CalibedPathMaker(file_path, initial="calibrated")
        save_path = cpm.path
        ext = cpm.extention
        # HACK: この拡張子の分岐きれいではない。良い方法ないか？？
        if ext == ".avi" or ext == ".mp4" or ext == ".wmv":
            # データが動画のとき
            calibrate_movie(calib, file_path, save_path)
            print("動画の保存完了")
            # 以下、movie_mode = Trueならばcalib前後の動画をconcatenateする
            if config.movie_mode:
                print("元動画との連結開始")
                cpm = CalibedPathMaker(file_path, initial="concatenated")
                concatatenate_movie(file_path, save_path, cpm.path, config.left_title, config.right_title)
        elif ext == ".jpg" or ext == ".JPG" or ext == ".png":
            # データが画像のとき
            img = cv2.imread(file_path)
            calib.execute(img)
            calibrated_img = calib.calibrated_img
            cv2.imwrite(save_path, calibrated_img)
            print("画像の保存完了")
        else:
            print("[calibration.py][ERROR]calibrationできないファイル")
            raise Exception

if __name__ == "__main__":
    main()