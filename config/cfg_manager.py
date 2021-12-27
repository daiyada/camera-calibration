"""
@file cfg_manager.py
@brief yamlファイルからparamを読み取るファイル

@author Shunsuke Hishida / created on 2021/05/26
"""
import os

import numpy as np

from inout.load import Loader


class ReadMovie2Img(object):
    PATH = os.path.join(os.getcwd(), "config", "movie2img.yaml")

    @classmethod
    def getYamlPath(cls):
        return cls.PATH

    @property
    def getStartTime(self):
        return self.__start_time

    @property
    def getEndTime(self):
        return self.__end_time

    @property
    def getOutputNumber(self):
        return self.__output_number

    @property
    def getCutFlag(self):
        return self.__cut_flag

    @property
    def getExtension(self):
        return self.__extension

    @property
    def getInputPath(self):
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


class ReadCalculation(object):
    PATH = os.path.join(os.getcwd(), "config", "calc_camera_param.yaml")

    @classmethod
    def getYamlPath(cls):
        return cls.PATH

    @property
    def getSquareSize(self):
        return self.__square_size

    @property
    def getCrossPoint(self):
        return self.__cross_point

    @property
    def getImgDir(self):
        return self.__img_dir

    @property
    def getImgExt(self):
        return self.__img_ext

    @property
    def getFileName(self):
        return self.__file_name

    def __init__(self, path):
        """Constructor"""
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        """yamlファイルからparamを読み取る"""
        self.__square_size = int(self.__yaml_data["square_size"])
        self.__cross_point = (
            int(self.__yaml_data["cross_point"]["vertical"]),
            int(self.__yaml_data["cross_point"]["horizontal"]),
        )
        self.__img_dir = str(self.__yaml_data["img"]["input_dir"])
        self.__img_ext = str(self.__yaml_data["img"]["extension"])
        self.__file_name = str(self.__yaml_data["output"]["file_name"])


class ReadCalibration(object):
    PATH = os.path.join(os.getcwd(), "config", "calibration.yaml")

    @classmethod
    def getYamlPath(cls):
        return cls.PATH

    @property
    def getInputDir(self):
        return self.__input_dir

    @property
    def getExtension(self):
        return self.__ext

    @property
    def getMovieMode(self):
        return self.__movie_mode

    @property
    def getRightTitle(self):
        return self.__right_title

    @property
    def getLeftTitle(self):
        return self.__left_title

    def __init__(self, path):
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        self.__input_dir = str(self.__yaml_data["before_calib"]["input_dir"])
        self.__ext = self.__yaml_data["before_calib"]["ext"]
        self.__movie_mode = bool(int(self.__yaml_data["after_calib"]["movie_mode"]))
        self.__left_title = bool(int(self.__yaml_data["after_calib"]["left_title"]))
        self.__right_title = bool(int(self.__yaml_data["after_calib"]["right_title"]))


class ReadCalibrationParam(object):
    PATH = os.path.join(os.getcwd(), "config", "calibration_param.npz")

    @classmethod
    def getNpzPath(cls):
        return cls.PATH

    @property
    def getCameraMatrix(self):
        return self.__camera_matrix

    @property
    def getDistortion(self):
        return self.__distortion

    def __init__(self, path):
        """Constructor"""
        calib_param = np.load(path)
        self.__deserialize(calib_param)

    def __deserialize(self, calib_param):
        self.__camera_matrix = calib_param["camera_matrix"]
        self.__distortion = calib_param["distortion"]


class ReadMovieCutter(object):
    PATH = os.path.join(os.getcwd(), "config", "movie_cutter.yaml")

    @classmethod
    def getYamlPath(cls):
        return cls.PATH

    @property
    def getStartTime(self):
        return self.__start_time

    @property
    def getEndTime(self):
        return self.__end_time

    @property
    def getInputPath(self):
        return self.__input_path

    @property
    def getOutputDir(self):
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


class ReadMovieConcatenater(object):
    PATH = os.path.join(os.getcwd(), "config", "movie_concatenater.yaml")

    @classmethod
    def getYamlPath(cls):
        return cls.PATH

    @property
    def getConcateType(self):
        return self.__concate_type

    @property
    def getArrangement(self):
        return self.__arrangement

    @property
    def getInputPath1(self):
        return self.__input_path_1

    @property
    def getInputPath2(self):
        return self.__input_path_2

    @property
    def getInputPath3(self):
        return self.__input_path_3

    @property
    def getInputPath4(self):
        return self.__input_path_4

    @property
    def getOnputPath(self):
        return self.__output_path

    @property
    def getFileName(self):
        return self.__file_name

    @property
    def getExtension(self):
        return self.__extension

    @property
    def getTitle1(self):
        return self.__title_1

    @property
    def getTitle2(self):
        return self.__title_2

    @property
    def getTitle3(self):
        return self.__title_3

    @property
    def getTitle4(self):
        return self.__title_4

    def __init__(self, path):
        """Constructor"""
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __checkPath(self):
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
        self.__checkPath()
