"""
@file movie_cutter.py
@brief 秒数を指定して画像を切り出す

@author Shunsuke Hishida / created on 2021/06/04
"""
import os

import cv2

from config.cfg_manager import ReadMovieCutter

def setOutputFormat(movie, save_path):
    """
    @param movie (cv2.VideoCapture)
    """
    fourcc = int(movie.get(cv2.CAP_PROP_FOURCC))
    fps = int(movie.get(cv2.CAP_PROP_FPS))
    width = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
    new_movie = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
    return new_movie

def setRange(movie, start_time, end_time):
    """
    切り出し範囲を決める
    """
    fps = int(movie.get(cv2.CAP_PROP_FPS))
    all_frames = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))
    start_frame = start_time * fps
    end_frame = end_time * fps
    if end_frame > all_frames:
        end_frame = all_frames
    return start_frame, end_frame

def cutMovie(data_path, start_time, end_time, save_path):
    """
    @brief 指定の時間で動画を切り出す
    """
    if not start_time < end_time:
        print("[ERROR]切り出し開始時間と切り出し終了時間の大小関係")
        raise Exception
    movie = cv2.VideoCapture(data_path)
    new_movie = setOutputFormat(movie, save_path)
    start_frame, end_frame = setRange(movie, start_time, end_time)
    for frame_num in range(start_frame, end_frame, 1):
        movie.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = movie.read()
        if ret:
            new_movie.write(frame)
        else:
            break
    movie.release()
    new_movie.release()

def main():
    """メイン関数"""
    rmc = ReadMovieCutter(ReadMovieCutter.getYamlPath())
    save_path = os.path.join(rmc.getOutputDir, "cut_{}".format(os.path.basename(rmc.getInputPath)))
    cutMovie(rmc.getInputPath, rmc.getStartTime, rmc.getEndTime, save_path)

if __name__ == "__main__":
    main()