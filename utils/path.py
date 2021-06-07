"""
@file path.py
@brief ファイルパスを生成する

@author Shunsuke Hishida / created 2021/04/16
"""
import os

class ConfigPathMaker(object):

    @property
    def getPath(self): return self.__path

    def __init__(self, path):
        file_name, ext = os.path.splitext(os.path.basename(path))
        dir_path = os.path.join(os.getcwd(), "config")
        os.makedirs(dir_path, exist_ok=True)
        self.__path = os.path.join(dir_path, "{}{}".format(file_name, ext))

class CalibedPathMaker(object):

    @property
    def getExt(self): return self.__ext

    @property
    def getPath(self): return self.__path

    def __init__(self, path, initial="calibrated"):
        file_name, self.__ext = os.path.splitext(os.path.basename(path))
        dir_path = os.path.join(os.getcwd(), "after")
        os.makedirs(dir_path, exist_ok=True)
        self.__path = os.path.join(dir_path, "{}_{}{}".format(initial, file_name, self.__ext))