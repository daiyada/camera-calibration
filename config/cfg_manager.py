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
    def getYamlPath(cls): return cls.PATH

    @property
    def getStartTime(self): return self.__start_time

    @property
    def getEndTime(self): return self.__end_time

    @property
    def getOutputNumber(self): return self.__output_number

    @property
    def getCutFlag(self): return self.__cut_flag

    @property
    def getExtension(self): return self.__extension

    def __init__(self, path):
        """constructor"""
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        """yamlファイルからparamを読み取る"""
        self.__start_time = int(self.__yaml_data["time"]["start_time"])
        self.__end_time = int(self.__yaml_data["time"]["end_time"])
        self.__output_number = int(self.__yaml_data["number"]["output_sheets"])
        self.__cut_flag = bool(int(self.__yaml_data["cut_flag"]))
        self.__extension = str(self.__yaml_data["extension"])

class ReadCalculation(object):
    PATH = os.path.join(os.getcwd(), "config", "calc_camera_param.yaml")

    @classmethod
    def getYamlPath(cls): return cls.PATH

    @property
    def getSquareSize(self): return self.__square_size

    @property
    def getCrossPoint(self): return self.__cross_point

    @property
    def getImgDir(self): return self.__img_dir

    @property
    def getImgExt(self): return self.__img_ext

    @property
    def getFileName(self): return self.__file_name

    def __init__(self, path):
        """Constructor"""
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        """yamlファイルからparamを読み取る"""
        self.__square_size = int(self.__yaml_data["square_size"])
        self.__cross_point = (int(self.__yaml_data["cross_point"]["vertical"]), int(self.__yaml_data["cross_point"]["horizontal"]))
        self.__img_dir = str(self.__yaml_data["img"]["input_dir"])
        self.__img_ext = str(self.__yaml_data["img"]["extension"])
        self.__file_name = str(self.__yaml_data["output"]["file_name"])

class ReadCalibration(object):
    PATH = os.path.join(os.getcwd(), "config", "calibration.yaml")

    @classmethod
    def getYamlPath(cls): return cls.PATH

    @property
    def getInputDir(self): return self.__input_dir

    @property
    def getExtension(self): return self.__ext

    @property
    def getOutputDir(self): return self.__output_dir

    @property
    def getMovieMode(self): return self.__movie_mode

    def __init__(self, path):
        self.__load = Loader(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        self.__input_dir = str(self.__yaml_data["before_calib"]["input_dir"])
        self.__ext = self.__yaml_data["before_calib"]["input_dir"]
        self.__output_dir = str(self.__yaml_data["after_calib"]["output_dir"])
        self.__movie_mode = bool(int(self.__yaml_data["after_calib"]["movie_mode"]))

class ReadCalibrationParam(object):
    PATH = os.path.join(os.getcwd(), "config", "calibration_param.npz")

    @classmethod
    def getNpzPath(cls): return cls.PATH

    @property
    def getCameraMatrix(self): return self.__camera_matrix

    @property
    def getDistortion(self): return self.__distortion

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
    def getYamlPath(cls): return cls.PATH

    @property
    def getStartTime(self): return self.__start_time

    @property
    def getEndTime(self): return self.__end_time

    @property
    def getInputPath(self): return self.__input_path

    @property
    def getOutputDir(self): return self.__output_dir

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