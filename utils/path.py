"""
@file path.py
@brief ファイルパスを生成する

@author Shunsuke Hishida / created 2021/04/16
"""
import os

class ConfigPathMaker(object):

    @property
    def getPath(self): return self.__path

    def __init__(self, file_name, ext):
        dir_path = os.path.join(os.getcwd(), "config")
        os.makedirs(dir_path, exist_ok=True)
        self.__path = os.path.join(dir_path, "{}.{}".format(file_name, ext))