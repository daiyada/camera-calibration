"""
@file_manager.py
@brief ファイル整理関係

@author Shunsuke Hishida / created on 2021/06/04
"""
import glob
import os

class FilePathGetter(object):

    @property
    def file_list(self): return self.__file_list

    def __init__(self, dir_path, ext_list):
        """
        @param dir_path (str) 取得したいファイルが入ったディレクトリパス
        @param ext_list (list) 取得したいファイルの拡張子を入れたリスト
        """
        self.__file_list = []
        for ext in ext_list:
            file_list = glob.glob(os.path.join(dir_path, "*.{}".format(ext)))
            self.__file_list.extend(file_list)
            
