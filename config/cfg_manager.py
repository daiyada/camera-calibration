"""
@file cfg_manager.py
@brief yamlファイルからparamを読み取るファイル

@author Shunsuke Hishida / created on 2021/05/26
"""
import os

from inout.load import Loader

class ReadMovie2Img(object):
    PATH = os.path.join(os.getcwd(), "config", "movie2img_param.yaml")

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
    PATH = os.path.join(os.getcwd(), "config", "calculation_param.yaml")

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
