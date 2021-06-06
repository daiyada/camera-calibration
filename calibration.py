"""
@file calibration.py
@brief 特定のデータに対してcalibrationを実施する

@author Shunsuke Hishida / created 2021/06/04
"""
import os

import cv2
from tqdm import tqdm

from config.cfg_manager import ReadCalibration
from config.cfg_manager import ReadCalibrationParam
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
        file_name, ext = os.path.splitext(os.path.basename(file_path))
        cpm = CalibedPathMaker(file_name, ext)
        save_path = cpm.getPath
        if ext == ".avi" or ext == ".mp4" or ext == ".wmv":
            # データが動画のとき
            calibrateMovie(calib, file_path, save_path)
            print("動画の保存完了")
        elif ext == ".jpg" or ext == ".JPG" or ext == ".png":
            # データが画像のとき
            img = cv2.imread(file_path)
            calib.execute(img)
            calibrated_img = calib.getCalibratedImg
            cv2.imwrite(save_path, calibrated_img)
            print("画像の保存完了")
        else:
            print("[calibration.py][ERROR]calibrationできるファイルではない")
            raise Exception

if __name__ == "__main__":
    main()