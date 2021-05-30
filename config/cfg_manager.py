"""
@file cfg_manager.py
@param yamlファイルからparamを読み取るファイル

@author Shunsuke Hishida / created on 2021/05/26
@copyright (c) 2021 Global Walkers,inc All rights reserved.
"""
import os

from inout.load import Load

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

    def __init__(self, path):
        """constructor"""
        self.__load = Load(path)
        self.__yaml_data = self.__load.loadYaml()
        self.__deserialize()

    def __deserialize(self):
        """yamlファイルからparamを読み取る"""
        self.__start_time = int(self.__yaml_data["time"]["start_time"])
        self.__end_time = int(self.__yaml_data["time"]["end_time"])
        self.__output_number = int(self.__yaml_data["number"]["output_sheets"])
        self.__cut_flag = bool(int(self.__yaml_data["type"]["cut_flag"]))

