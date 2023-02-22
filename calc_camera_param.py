"""
@file calc_camera_param.py
@brief カメラのキャリブレーションに必要なパラメータを算出する

@author Shunsuke Hishida / created on 2021/05/30
"""
from abc import ABCMeta, abstractmethod
import argparse
import glob
import math
import os

import cv2
import numpy as np
from tqdm import tqdm

from utils.cfg_manager import CalculationParameters, GridPattern
from inout.save import Saver
from utils.path import ConfigPathMaker

class CameraParamCalculator(metaclass=ABCMeta):
    def __init__(self, params: CalculationParameters):
        """Constructor"""
        self._params = params

    @abstractmethod
    def calculate(self):
        """
        @brief キャリブレーションに必要なパラメータ４つ（戻り値）を算出
        """
        pass

    @abstractmethod
    def _make_board(self):
        """実空間上でのcalibration用ボードを作成"""
        pass

    def _write_point(self, corners, img, gray_img, criteria, ret, index):
        """画像内のcalibrationボードに制御点を描画"""
        img = cv2.drawChessboardCorners(img, self._params.grid_num_tuple, corners, ret)
        save_dir = "./draw_corner"
        os.makedirs(save_dir, exist_ok=True)
        cv2.imwrite(os.path.join(save_dir, f"test_{index}.jpg"), img)

    def _make_blob_detector(self):
        """
        BLOB: Binary Large OBject
        """
        blob_area = math.pi * (self._params.circle_radius)**2
        blob_params = cv2.SimpleBlobDetector_Params()
        blob_params.filterByArea = True
        blob_params.minArea = 0.80 * blob_area
        blob_params.maxArea = 1.20 * blob_area
        self._blob_detector = cv2.SimpleBlobDetector_create(blob_params)


class CheckerBoard(CameraParamCalculator):
    def __init__(self, params: CalculationParameters):
        """Constructor"""
        super().__init__(params)
        self.__make_board()

    def __make_board(self):
        """実空間上でのチェッカーボードの座標情報を算出"""
        self.__checker_coords = np.zeros((np.prod(self._params.grid_num_tuple), 3), np.float32)
        self.__checker_coords[:,:2] = np.indices(self._params.grid_num_tuple).T.reshape(-1, 2)
        self.__checker_coords *= self._params.grid_interval


    def calculate(self, img_list, save_result: bool = True):
        """
        @brief キャリブレーションに必要なパラメータ４つ（戻り値）を算出
        @param img_list (list) parameterを算出するのに用いる画像群（チェッカーボード）
        @param save_result (bool) 制御点を描画した画像を保存するか管理するフラグ default:True
        @return camera_matrix (numpy.ndarray) カメラ行列
        @return dist (list) レンズ歪みパラメータ
        @return rot_vecs (list) 回転ベクトル
        @return trans_vecs (numpy.ndarray) 並進ベクトル
        """
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        obj_coords = []     # 3d point in real world space
        img_coords = []     # 2d point in image space
        for i, img_path in enumerate(tqdm(img_list)):
            img = cv2.imread(img_path)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(gray_img, self._params.grid_num_tuple)
            if ret:
                obj_coords.append(self.__checker_coords)
                #  cornersより高い精度での座標の算出
                sophiscated_corners = cv2.cornerSubPix(gray_img, corners, (11, 11), (-1, -1), criteria)
                img_coords.append(sophiscated_corners)

                #　制御点を描画した画像を確認したい場合は以下２行のコメントアウトを解除
                if save_result:
                    self._write_point(sophiscated_corners, img, gray_img, criteria, ret, i)

        _, camera_matrix, dist, rot_vecs, trans_vecs = cv2.calibrateCamera(obj_coords, img_coords, gray_img.shape[::-1], None, None)
        return camera_matrix, dist, rot_vecs, trans_vecs


class SymmetricCirclesGrid(CameraParamCalculator):

    def __init__(self, params: CalculationParameters):
        """Constructor"""
        super().__init__(params)
        self._make_blob_detector()
        self._make_board()

    def _make_board(self):
        """
        EX) grid_num = (horizontal_grid_num, vertical_grid_num) = (10, 7) の場合
        =====
            　　０ １ ２ ３ ４ ５ ６ ７ ８ ９  <- horizontal_index
            　┌ー ー ー ー ー ー ー ー ー ー
            ０｜● ● ● ● ● ● ● ● ● ●
            １｜● ● ● ● ● ● ● ● ● ●
            ２｜● ● ● ● ● ● ● ● ● ●
            ３｜● ● ● ● ● ● ● ● ● ●
            ４｜● ● ● ● ● ● ● ● ● ●
            ５｜● ● ● ● ● ● ● ● ● ●
            ６｜● ● ● ● ● ● ● ● ● ●

            ↑
            vertical_index
        =====
        iの対応関係; cv2.findCirclesGridの戻り値 corners と index をリンクさせる
            　　０ １ ２ ３ ４ ５ ６ ７ ８ ９  <- horizontal_index
            　┌ー ー ー ー ー ー ー ー ー ー
            ０｜６ 13 20 27 34 41 48 55 62 69
            １｜５ 12 18 26 33 40 47 54 61 68
            ２｜４ 11 17 25 32 39 46 53 60 67
            ３｜３ 10 17 24 31 38 45 52 59 66
            ４｜２ ９ 16 23 30 37 44 51 58 65
            ５｜１ ８ 15 22 29 36 43 50 57 64
            ６｜０ ７ 14 21 28 35 42 49 56 63

            ↑
            vertical_index
        """
        self.__checker_coords = np.zeros((np.prod(self._params.grid_num_tuple), 3), np.float32)
        horizontal_index = 0
        vertical_index = 0
        for i in range(np.prod(self._params.grid_num_tuple)):
            if (i % self._params.vertical_grid_num == 0) and (i != 0):
                horizontal_index += 1
                vertical_index = self._params.vertical_grid_num * 2 - 1
            self.__checker_coords[i][:2] = (
                self._params.grid_interval * horizontal_index,
                self._params.grid_interval * vertical_index
                )
            # 垂直方向に隣り合う i は vertical_index を -2 する必要あり
            vertical_index -= 2

    def calculate(self, img_list: list, save_result: bool = True):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        obj_coords = []     # 3d point in real world space
        img_coords = []     # 2d point in image space
        for i, img_path in enumerate(tqdm(img_list)):
            img = cv2.imread(img_path)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            key_points = self._blob_detector.detect(gray_img)

            img_with_keypoints = cv2.drawKeypoints(img, key_points, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            img_with_keypoints_gray = cv2.cvtColor(img_with_keypoints, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findCirclesGrid(img_with_keypoints, self._params.grid_num_tuple, None, flags = cv2.CALIB_CB_SYMMETRIC_GRID)

            if ret:
                obj_coords.append(self.__checker_coords)
                img_coords.append(corners)

                #　制御点を描画した画像を確認したい場合は以下２行のコメントアウトを解除
                if save_result:
                    self._write_point(corners, img, img_with_keypoints_gray, criteria, ret, i)

        _, camera_matrix, dist, rot_vecs, trans_vecs = cv2.calibrateCamera(obj_coords, img_coords, gray_img.shape[::-1], None, None)
        return camera_matrix, dist, rot_vecs, trans_vecs


class AsymmetricCirclesGrid(CameraParamCalculator):
    
    def __init__(self, params: CalculationParameters):
        """Constructor"""
        super().__init__(params)
        self._make_blob_detector()
        self._make_board()

    def _make_board(self):
        """
        EX) grid_num = (horizontal_grid_num, vertical_grid_num) = (11, 4) の場合
        =====
            　　０１２３４５６７８９10  <- horizontal_index
            　┌ーーーーーーーーーーー
            ０｜　●  ●  ●  ●  ●  
            １｜●　●　●　●　●　●　
            ２｜　●　●　●　●　●　
            ３｜●　●　●　●　●　●　
            ４｜　●　●　●　●　●　
            ５｜●　●　●　●　●　●　
            ６｜　●　●　●　●　●　
            ７｜●　●　●　●　●　●　
            ↑
            vertical_index
        =====
        iの対応関係; cv2.findCirclesGridの戻り値 corners と index をリンクさせる
            　　０１２３４５６７８９10  <- horizontal_index
            　┌ーーーーーーーーーー
            ０｜　７　15　23　31　39　
            １｜３　11　19　27　35　43
            ２｜　６　14　22　30　38　
            ３｜２　10　18　26　34　42
            ４｜　５　13　21　29　37　
            ５｜１　９　17　25　33　41
            ６｜　４　12　20　28　36　
            ７｜０　８　16　24　32　40
            ↑
            vertical_index
        """
        self.__checker_coords = np.zeros((np.prod(self._params.grid_num_tuple), 3), np.float32)
        horizontal_index = 0
        vertical_index = self._params.vertical_grid_num * 2 - 1
        for i in range(np.prod(self._params.grid_num_tuple)):
            if (i % self._params.vertical_grid_num == 0) and (i != 0):
                horizontal_index += 1
                if horizontal_index % 2 == 0:
                    vertical_index = self._params.vertical_grid_num * 2 - 1
                else:
                    vertical_index = self._params.vertical_grid_num * 2 - 2
            self.__checker_coords[i][:2] = (
                self._params.grid_interval/2 * horizontal_index,
                self._params.grid_interval/2 * vertical_index
                )
            # 垂直方向に隣り合う i は vertical_index を +2 する必要あり
            vertical_index -= 2

    def calculate(self, img_list: list, save_result: bool = True):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        obj_coords = []     # 3d point in real world space
        img_coords = []     # 2d point in image space
        for i, img_path in enumerate(tqdm(img_list)):
            img = cv2.imread(img_path)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            key_points = self._blob_detector.detect(gray_img)

            img_with_keypoints = cv2.drawKeypoints(img, key_points, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            img_with_keypoints_gray = cv2.cvtColor(img_with_keypoints, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findCirclesGrid(img_with_keypoints, self._params.grid_num_tuple, None, flags = cv2.CALIB_CB_ASYMMETRIC_GRID)
            if ret:
                obj_coords.append(self.__checker_coords)
                img_coords.append(corners)

                #　制御点を描画した画像を確認したい場合は以下２行のコメントアウトを解除
                if save_result:
                    self._write_point(corners, img, img_with_keypoints_gray, criteria, ret, i)

        _, camera_matrix, dist, rot_vecs, trans_vecs = cv2.calibrateCamera(obj_coords, img_coords, gray_img.shape[::-1], None, None)
        return camera_matrix, dist, rot_vecs, trans_vecs


if __name__ == "__main__":
    params = CalculationParameters(CalculationParameters.get_yaml_path())
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", type=int,
                        help="Write calibration pattern, \
                            0: Checkerboard,\
                            1: Symmetric Circles Grid,\
                            2: Asymmetric Circles Grid")
    args = parser.parse_args()

    if args.pattern == GridPattern.CHECKER_BOARD:
        calc = CheckerBoard(params)
    elif args.pattern == GridPattern.SYMMETRIC_CIRCLES_GRID:
        calc = SymmetricCirclesGrid(params)
    elif args.pattern == GridPattern.ASYMMETRIC_CIRCLES_GRID:
        calc = AsymmetricCirclesGrid(params)
    else:
        raise Exception("Calibration Pattern は 0,1,2 のうちから選択してください")

    img_list = glob.glob(os.path.join(params.img_dir, f"*.{params.img_extention}"))
    camera_matrix, distortion, _, _  = calc.calculate(img_list, save_result=True)
    cpm = ConfigPathMaker(params.file_name, ext="npz")
    save = Saver(cpm.path, camera_matrix=camera_matrix, distortion=distortion)
    save.save_npz()
