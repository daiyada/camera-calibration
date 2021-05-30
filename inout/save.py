"""
@file save.py
@brief ファイルのsave行う

@author Shunsuke Hishida / created 2021/04/09
"""
import os
import shutil
import zipfile

from tqdm import tqdm

class Saver(object):
    """
    @brief ファイルのsaveを行うクラス
    """
    def __init__(self, rgb_dir, depthraw_dir):
        """
        @brief コンストラクター
        """
        if not os.path.isdir(rgb_dir):
            print("{}: 指定のディレクトリはありません".format(rgb_dir))
            raise FileNotFoundError
        if not os.path.isdir(depthraw_dir):
            print("{}: 指定のディレクトリはありません".format(depthraw_dir))
            raise FileNotFoundError
        self.__rgb_dir = rgb_dir
        self.__depthraw_dir = depthraw_dir

    def from_zip(self, zip_path, file_list, key=""):
        """
        @brief zipから抽出して保存
        @param output_dir (str) 抽出したあと解凍するパス
        @param zip_path (str) 抽出するzipのパス
        @param file_list (list) 抽出するfile名が格納されたリスト
        @param key (str) "RGB"か"DepthRaw"
        """
        if key == "":
            print("[from_zip]keyを入力してください")
            raise Exception
        for file_name in tqdm(file_list):
            self.do_unzip(zip_path, file_name, key)

    def do_unzip(self, zip_path, file_name, key):
        """
        @brief 1データをunzipする
        @param zip_path (str) 抽出するzipのパス
        @param file_name (str) 抽出するファイル名
        @param key (str) "RGB"か"DepthRaw"
        """
        with zipfile.ZipFile(zip_path) as target_zip:
            if key == "RGB":
                target_zip.extract(file_name, self.__rgb_dir)
            elif key == "DepthRaw":
                target_zip.extract(file_name, self.__depthraw_dir)
            else:
                print("{}: keyの値に問題あり".format(key))
                raise Exception

    def from_dir(self, file_list, key=""):
        """
        @brief 特定のdirectoryからファイルを抽出して保存
        @param file_list (list) コピー元のデータパスを格納したリスト
        @param key (str) "RGB"か"DepthRaw"
        """
        if key == "":
            print("[from_zip]keyを入力してください")
            raise Exception
        for file_path in tqdm(file_list):
            file_name = os.path.basename(file_path)
            if key == "RGB":
                dst_path = os.path.join(self.__rgb_dir, file_name)
            elif key == "DepthRaw":
                dst_path = os.path.join(self.__depthraw_dir, file_name)
            else:
                print("{}: keyの値に問題あり".format(key))
                raise Exception
            shutil.copy(file_path, dst_path)
