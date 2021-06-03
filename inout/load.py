"""
@file save.py
@brief ファイルのloadを行う

@author Shunsuke Hishida / created 2021/04/16
"""
import os

import cv2
import yaml

class Loader(object):

    def __init__(self, path):
        """Contructor"""
        self.__path = path

    def loadYaml(self):
        """
        @return cfg_data (dict) configファイル内のデータを格納したdictionary
        """
        try:
            with open(self.__path, mode="r", encoding="utf-8") as f:
                cfg_data = yaml.load(f)
        except Exception as e:
            print("[load_yaml]yamlファイルのロードができませんでした")
            print(e)
        return cfg_data