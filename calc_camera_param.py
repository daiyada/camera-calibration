"""
@file calc_camera_param.py
@brief カメラのキャリブレーションに必要なパラメータを算出する

@author Shunsuke Hishida / created on 2021/05/30
"""
import glob
import os

import cv2
import numpy as np
from tqdm import tqdm

from config.cfg_manager import ReadCalculation
from inout.save import Saver
from utils.path import ConfigPathMaker

class CalcCameraParam(object):
    def __init__(self):
        """Constructor"""
        self.__param = ReadCalculation(ReadCalculation.getYamlPath())

        # チェッカーボードの角の座標の算出
        self.__checker_coords = np.zeros((np.prod(self.__param.getCrossPoint), 3), np.float32)
        self.__checker_coords[:,:2] = np.indices(self.__param.getCrossPoint).T.reshape(-1, 2)
        self.__checker_coords *= self.__param.getSquareSize

    def __calcParam(self, img_list):
        """
        @brief キャリブレーションに必要なパラメータ４つ（戻り値）を算出
        @param parameterを算出するのに用いる画像群（チェッカーボード）
        @return camera_matrix (numpy.ndarray) カメラ行列
        @return dist (list) レンズ歪みパラメータ
        @return rot_vecs (list) 回転ベクトル
        @return trans_vecs (numpy.ndarray) 並進ベクトル
        """
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        obj_coords = []     # 3d point in real world space
        img_coords = []     # 2d point in image space
        for img_path in tqdm(img_list):
            img = cv2.imread(img_path)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(gray_img, self.__param.getCrossPoint)
            if ret:
                obj_coords.append(self.__checker_coords)
                #  cornersより高い精度での座標の算出
                sophiscated_corners = cv2.cornerSubPix(gray_img, corners, (11, 11), (-1, -1), criteria)
                img_coords.append(sophiscated_corners)

                #　制御点を描画した画像を確認したい場合は以下２行のコメントアウトを解除
                # img = cv2.drawChessboardCorners(img, self.__param.getCrossPoint, sophiscated_corners, ret)
                # cv2.imwrite(os.path.join(os.getcwd(), "test.jpg"), img)

        _, camera_matrix, dist, rot_vecs, trans_vecs = cv2.calibrateCamera(obj_coords, img_coords, gray_img.shape[::-1], None, None)
        return camera_matrix, dist, rot_vecs, trans_vecs

    def execute(self):
        """メイン関数"""
        img_list = glob.glob(os.path.join(self.__param.getImgDir, "*.{}".format(self.__param.getImgExt)))
        camera_matrix, distortion, _, _ = self.__calcParam(img_list)
        cpm = ConfigPathMaker(self.__param.getFileName, ext="npz")
        # 計算したparameterをnpzファイルに保存
        save = Saver(cpm.getPath, camera_matrix=camera_matrix, distortion=distortion)
        save.saveNpz()
        print("Done!!")

if __name__ == "__main__":
    ccp = CalcCameraParam()
    ccp.execute()