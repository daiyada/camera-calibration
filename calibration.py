"""
@file calibration.py
@brief 特定のデータに対してcalibrationを実施する

@author Shunsuke Hishida / created 2021/06/04
"""
import os

import cv2
from tqdm import tqdm

from config.cfg_manager import ReadCalibration, ReadCalibrationParam
from utils.path import CalibedPathMaker
from utils.file_manager import FilePathGetter
from movie_cutter import setOutputFormat

class Calibration(object):

    @property
    def getCalibratedImg(self): return self.__calibrated_img

    def __init__(self):
        """Constructor"""
        self.__calib_param = ReadCalibrationParam(ReadCalibrationParam.getNpzPath())

    def execute(self, img):
        """
        @brief キャリブレーションを実行する
        @param img (numpy.ndarray) calibrationする画像
        """
        h, w, _ = img.shape
        dst = cv2.undistort(
                            img,
                            self.__calib_param.getCameraMatrix,
                            self.__calib_param.getDistortion,
                            None)
        self.__calibrated_img = dst

def setFormat(movie, img, save_path):
    fourcc = int(movie.get(cv2.CAP_PROP_FOURCC))
    fps = int(movie.get(cv2.CAP_PROP_FPS))
    height, width, _ = img.shape
    new_movie = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
    return new_movie

def concatatenateMovie(movie1_path, movie2_path, save_path):
    movie1 = cv2.VideoCapture(movie1_path)
    movie2 = cv2.VideoCapture(movie2_path)
    format_flag = False
    while True:
        ret1, img1 = movie1.read()
        ret2, img2 = movie2.read()
        ret = ret1 and ret2
        if ret:
            img = cv2.hconcat([img1, img2])
            if not format_flag:
                concatanated_movie = setFormat(movie1, img, save_path)
                format_flag = True
            # print("img: ", img.shape)
            # cv2.imwrite("/home/hishida/Desktop/test.png", img)
            # input(0)
            concatanated_movie.write(img)
        else:
            break
    concatanated_movie.release()
    movie1.release()
    movie2.release()

def calibrateMovie(calib, path, save_path):
    """
    動画データをキャリブレーション
    """
    movie = cv2.VideoCapture(path)
    new_movie = setOutputFormat(movie, save_path)
    while True:
        ret, img = movie.read()
        if ret:
            calib.execute(img)
            calibrated_img = calib.getCalibratedImg
            new_movie.write(calibrated_img)
        else:
            break
    movie.release()
    new_movie.release()

def main():
    """メイン関数"""
    config = ReadCalibration(ReadCalibration.getYamlPath())
    calib = Calibration()
    fpg = FilePathGetter(config.getInputDir, config.getExtension)
    file_list = fpg.getFileList
    for file_path in tqdm(file_list):
        cpm = CalibedPathMaker(file_path, initial="calibrated")
        save_path = cpm.getPath
        ext = cpm.getExt
        if ext == ".avi" or ext == ".mp4" or ext == ".wmv":
            # データが動画のとき
            calibrateMovie(calib, file_path, save_path)
            print("動画の保存完了")
            # 以下、movie_mode = Trueならばcalib前後の動画をconcatenateする
            if config.getMovieMode:
                print("元動画との連結開始")
                cpm = CalibedPathMaker(file_path, initial="concatenated")
                con_save_path = cpm.getPath
                concatatenateMovie(file_path, save_path, con_save_path)
        elif ext == ".jpg" or ext == ".JPG" or ext == ".png":
            # データが画像のとき
            img = cv2.imread(file_path)
            calib.execute(img)
            calibrated_img = calib.getCalibratedImg
            cv2.imwrite(save_path, calibrated_img)
            print("画像の保存完了")
        else:
            print("[calibration.py][ERROR]calibrationできないファイル")
            raise Exception

if __name__ == "__main__":
    main()