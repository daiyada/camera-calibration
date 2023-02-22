"""
@file cfg_manager.py
@brief yamlファイルからparamを読み取るファイル

@author Shunsuke Hishida / created on 2021/05/26
"""
from enum import IntEnum
import os

import numpy as np

from inout.load import Loader

class GridPattern(IntEnum):
    CHECKER_BOARD = 0
    SYMMETRIC_CIRCLES_GRID = 1
    ASYMMETRIC_CIRCLES_GRID = 2


class Movie2ImgParameters(object):
    PATH = os.path.join(os.getcwd(), "config", "movie2img.yaml")

    @classmethod
    def get_yaml_path(cls):
        return cls.PATH

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def output_number(self):
        return self.__output_number

    @property
    def cut_flag(self):
        return self.__cut_flag

    @property
    def extension(self):
        return self.__extension

    @property
    def input_path(self):
        return self.__input_path

    def __init__(self, path):
        """constructor"""
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        """yamlファイルからparamを読み取る"""
        self.__start_time = int(self.__yaml_data["time"]["start_time"])
        self.__end_time = int(self.__yaml_data["time"]["end_time"]) - 1
        self.__output_number = int(self.__yaml_data["number"]["output_sheets"])
        self.__cut_flag = bool(int(self.__yaml_data["cut_flag"]))
        self.__extension = str(self.__yaml_data["extension"])
        self.__input_path = str(self.__yaml_data["input_path"])


class CalculationParameters(object):
    PATH = os.path.join(os.getcwd(), "config", "calc_camera_param.yaml")

    @classmethod
    def get_yaml_path(cls):
        return cls.PATH

    @property
    def grid_interval(self):
        return self.__grid_interval

    @property
    def grid_num_tuple(self):
        """self.__grid_num_tuple = (vertical_num., horizontal_nnum)"""
        return self.__grid_num_tuple

    @property
    def horizontal_grid_num(self):
        return int(self.__yaml_data["grid_num"]["horizontal"])

    @property
    def vertical_grid_num(self):
        return int(self.__yaml_data["grid_num"]["vertical"])

    @property
    def img_dir(self):
        return self.__img_dir

    @property
    def img_extention(self):
        return self.__img_ext

    @property
    def file_name(self):
        return self.__file_name

    @property
    def circle_radius(self):
        return float(self.__yaml_data["circle_radius"])

    def __init__(self, path):
        """Constructor"""
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        """yamlファイルからparamを読み取る"""
        self.__grid_interval = int(self.__yaml_data["grid_interval"])
        self.__grid_num_tuple = (
            int(self.__yaml_data["grid_num"]["vertical"]),
            int(self.__yaml_data["grid_num"]["horizontal"]),
        )
        self.__img_dir = str(self.__yaml_data["img"]["input_dir"])
        self.__img_ext = str(self.__yaml_data["img"]["extension"])
        self.__file_name = str(self.__yaml_data["output"]["file_name"])


class CalibrationParameters(object):
    PATH = os.path.join(os.getcwd(), "config", "calibration.yaml")

    @classmethod
    def get_yaml_path(cls):
        return cls.PATH

    @property
    def input_dir(self):
        return self.__input_dir

    @property
    def extension(self):
        return self.__ext

    @property
    def movie_mode(self):
        return self.__movie_mode

    @property
    def right_title(self):
        return self.__right_title

    @property
    def left_title(self):
        return self.__left_title

    def __init__(self, path):
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        self.__input_dir = str(self.__yaml_data["before_calib"]["input_dir"])
        self.__ext = self.__yaml_data["before_calib"]["ext"]
        self.__movie_mode = bool(int(self.__yaml_data["after_calib"]["movie_mode"]))
        self.__left_title = str(self.__yaml_data["after_calib"]["title_left"])
        self.__right_title = str(self.__yaml_data["after_calib"]["title_right"])


class CalibrationMatrix(object):
    PATH = os.path.join(os.getcwd(), "config", "calibration_param.npz")

    @classmethod
    def get_npz_path(cls):
        return cls.PATH

    @property
    def camera_matrix(self):
        return self.__camera_matrix

    @property
    def distortion(self):
        return self.__distortion

    def __init__(self, path):
        """Constructor"""
        calib_param = np.load(path)
        self.__deserialize(calib_param)

    def __deserialize(self, calib_param):
        self.__camera_matrix = calib_param["camera_matrix"]
        self.__distortion = calib_param["distortion"]


class MovieCutterParameters(object):
    PATH = os.path.join(os.getcwd(), "config", "movie_cutter.yaml")

    @classmethod
    def get_yaml_path(cls):
        return cls.PATH

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def input_path(self):
        return self.__input_path

    @property
    def output_dir(self):
        return self.__output_dir

    def __init__(self, path):
        """Constructor"""
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        self.__start_time = int(self.__yaml_data["start_time"])
        self.__end_time = int(self.__yaml_data["end_time"]) - 1
        self.__input_path = str(self.__yaml_data["input_path"])
        self.__output_dir = str(self.__yaml_data["output_dir"])


class MovieConcatenaterParameters(object):
    PATH = os.path.join(os.getcwd(), "config", "movie_concatenater.yaml")

    @classmethod
    def get_yaml_path(cls):
        return cls.PATH

    @property
    def concate_type(self):
        return self.__concate_type

    @property
    def arrangement(self):
        return self.__arrangement

    @property
    def input_path1(self):
        return self.__input_path_1

    @property
    def input_path2(self):
        return self.__input_path_2

    @property
    def input_path3(self):
        return self.__input_path_3

    @property
    def input_path4(self):
        return self.__input_path_4

    @property
    def output_path(self):
        return self.__output_path

    @property
    def file_name(self):
        return self.__file_name

    @property
    def extension(self):
        return self.__extension

    @property
    def title1(self):
        return self.__title_1

    @property
    def title2(self):
        return self.__title_2

    @property
    def title3(self):
        return self.__title_3

    @property
    def title4(self):
        return self.__title_4

    def __init__(self, path):
        """Constructor"""
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __check_path(self):
        if not bool(self.__input_path_1) or not bool(self.__input_path_2):
            print("[ERROR]画像パス1, 2が未入力")
            raise Exception
        if self.__concate_type:  # 4動画合体の場合は3,4のパスが入力されていないとエラーをはく
            if not bool(self.__input_path_3) or bool(not self.__input_path_4):
                print("[ERROR]画像パス1, 2が未入力")
                raise Exception

    def __deserialize(self):
        self.__concate_type = bool(self.__yaml_data["concate_type"])
        self.__arrangement = bool(self.__yaml_data["arrangement"])
        self.__input_path_1 = self.__yaml_data["input"]["path_1"]
        self.__input_path_2 = self.__yaml_data["input"]["path_2"]
        self.__input_path_3 = self.__yaml_data["input"]["path_3"]
        self.__input_path_4 = self.__yaml_data["input"]["path_4"]
        self.__output_path = self.__yaml_data["output"]["path"]
        self.__file_name = self.__yaml_data["output"]["file_name"]
        self.__extension = self.__yaml_data["output"]["ext"]
        self.__title_1 = self.__yaml_data["output"]["title_1"]
        self.__title_2 = self.__yaml_data["output"]["title_2"]
        self.__title_3 = self.__yaml_data["output"]["title_3"]
        self.__title_4 = self.__yaml_data["output"]["title_4"]
        self.__check_path()
