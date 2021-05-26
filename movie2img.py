"""
@file movie2img.py
@brief 動画からキャリブレーションに回すための画像を切り出す

@author Shunsuke Hishida / created on 2021/05/26
@copyright (c) 2021 Global Walkers,inc All rights reserved.
"""
import os

import cv2

def cutImg(movie_path):
    cap = cv2.VideoCapture(movie_path)
    print("cap: ", cap)
    print("cap: ", type(cap))
    if not cap.isOpened():
        return



if __name__ == "__main__":
    file_name = "video_20210525_11.avi"
    movie_path = os.path.join(os.getcwd(), "movie", file_name)
    output_path = os.path.join(os.getcwd(), "calibration_img", file_name)
    cutImg(movie_path)
