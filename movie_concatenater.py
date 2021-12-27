"""
@file movie_concatenater.py
@brief 複数の動画を組み合わせて同時再生できるようにする

@author Shunsuke Hishida / created on 2021/07/19
@copyright (c) 2021 Global Walkers,inc All rights are reserved.
"""
import os

import cv2
from config.cfg_manager import ReadMovieConcatenater


class MovieConcatenater(object):
    def __init__(self, concate_type, arrangement, save_path, **kwargs):
        """
        Constructor

        @param concate_type (bool)  True -> 4動画合体、False -> 2動画合体
        @param arrangement (bool)  True -> 横方向合体、False -> 縦方向合体
        @param kwargs (dictionary) ファイルパスと、そのデータのタイトルを格納
                                   path_1 ~ path_4、title_1 ~ title_4のkeyにそれぞれ
                                   が格納されていることを前提とする
        """
        self.__arangement = arrangement
        self.__save_path = save_path
        self.__path_1 = kwargs["path_1"]
        self.__path_2 = kwargs["path_2"]
        self.__title_1 = kwargs["title_1"]
        self.__title_2 = kwargs["title_2"]
        if concate_type:
            self.__path_3 = kwargs["path_3"]
            self.__path_4 = kwargs["path_4"]
            self.__title_3 = kwargs["title_3"]
            self.__title_4 = kwargs["title_4"]
            self.__concate4Video()
        else:
            self.__concate2Video()

    def __setFormat(self, movie, img, save_path):
        fourcc = int(movie.get(cv2.CAP_PROP_FOURCC))
        fps = int(movie.get(cv2.CAP_PROP_FPS))
        height, width, _ = img.shape
        new_movie = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
        return new_movie

    def __concate2Video(self, color=(255, 0, 0)):
        format_flag = False
        movie1 = cv2.VideoCapture(self.__path_1)
        movie2 = cv2.VideoCapture(self.__path_2)
        while True:
            ret1, img1 = movie1.read()
            ret2, img2 = movie2.read()
            ret = ret1 and ret2
            if ret:
                cv2.putText(
                    img1,
                    self.__title_1,
                    (10, 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    color,
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    img2,
                    self.__title_2,
                    (10, 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    color,
                    2,
                    cv2.LINE_AA,
                )
                if self.__arangement:
                    img = cv2.hconcat([img1, img2])
                else:
                    img = cv2.vconcat([img2, img2])
                if not format_flag:
                    concatenated_2movie = self.__setFormat(
                        movie1, img, self.__save_path
                    )
                    format_flag = True
                concatenated_2movie.write(img)
            else:
                break
        concatenated_2movie.release()
        movie1.release()
        movie2.release()

    def __concate4Video(self, color=(255, 0, 0)):
        format_flag = False
        movie1 = cv2.VideoCapture(self.__path_1)
        movie2 = cv2.VideoCapture(self.__path_2)
        movie3 = cv2.VideoCapture(self.__path_3)
        movie4 = cv2.VideoCapture(self.__path_4)
        while True:
            ret1, img1 = movie1.read()
            ret2, img2 = movie2.read()
            ret3, img3 = movie3.read()
            ret4, img4 = movie4.read()
            ret = ret1 and ret2 and ret3 and ret4
            if ret:
                cv2.putText(
                    img1,
                    self.__title_1,
                    (10, 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    color,
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    img2,
                    self.__title_2,
                    (10, 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    color,
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    img3,
                    self.__title_3,
                    (10, 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    color,
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    img4,
                    self.__title_4,
                    (10, 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.5,
                    color,
                    2,
                    cv2.LINE_AA,
                )
                if self.__arangement:
                    img_h1 = cv2.hconcat([img1, img2])
                    img_h2 = cv2.hconcat([img3, img4])
                    img = cv2.vconcat([img_h1, img_h2])
                else:
                    img_v1 = cv2.vconcat([img1, img2])
                    img_v2 = cv2.vconcat([img3, img4])
                    img = cv2.hconcat([img_v1, img_v2])
                if not format_flag:
                    concatenated_4movie = self.__setFormat(
                        movie1, img, self.__save_path
                    )
                    format_flag = True
                concatenated_4movie.write(img)
            else:
                break
        concatenated_4movie.release()
        movie1.release()
        movie2.release()
        movie3.release()
        movie4.release()


def main():
    """メイン関数"""
    config = ReadMovieConcatenater(ReadMovieConcatenater.getYamlPath())
    save_path = os.path.join(
        config.getOnputPath, "{}.{}".format(config.getFileName, config.getExtension)
    )
    MovieConcatenater(
        config.getConcateType,
        config.getArrangement,
        save_path,
        path_1=config.getInputPath1,
        path_2=config.getInputPath2,
        path_3=config.getInputPath3,
        path_4=config.getInputPath4,
        title_1=config.getTitle1,
        title_2=config.getTitle2,
        title_3=config.getTitle3,
        title_4=config.getTitle4,
    )


if __name__ == "__main__":
    main()
