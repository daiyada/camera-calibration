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
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
                                    self.__calib_param.getCameraMatrix,
                                    self.__calib_param.getDistortion,
                                    (w, h),
                                    1,
                                    (w, h))
        dst = cv2.undistort(img,
                            self.__calib_param.get.getCameraMatrix,
                            self.__calib_param.getDistortion,
                            None,
                            new_camera_matrix)
        x, y, w, h = roi
        self.__calibrated_img = dst[y:y+h, x:x+w]

def main():
    """メイン関数"""
    config = ReadCalibration(ReadCalibration.getYamlPath())
    calib = Calibration()
    fpg = FilePathGetter(config.getInputDir, config.getExtension)
    file_list = fpg.getFileList
    for file_path in tadm(file_list):
        file_name, ext = os.path.splitext(os.path.basename(file_path))
        save_path = CalibedPathMaker(file_name, ext)
        if ext == "avi" or ext == "mp4" or ext == "wmv":
            
        elif ext == "jpg" or ext == "JPG" or ext == "png":
            img = cv2.imread(file_path)
            calib.execute(img)
            calibrated_img = calib.getCalibratedImg
            cv2.imwrite(save_path, calibrated_img)
            print("画像の保存完了")
        else:
            print("[calibration.py][ERROR]calibrationtaionできるファイルではない")
            raise Exception

if __name__ == "__main__":
    main()