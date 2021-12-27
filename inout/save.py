"""
@file save.py
@brief ファイルのsave行う

@author Shunsuke Hishida / created 2021/04/09
"""

import numpy as np

class Saver(object):
    def __init__(self, path, **kwargs):
        """Constructor"""
        self.__path = path
        self.__data = kwargs

    def saveNpz(self):
        np.savez(
            self.__path,
            camera_matrix=self.__data["camera_matrix"],
            distortion=self.__data["distortion"],
            )