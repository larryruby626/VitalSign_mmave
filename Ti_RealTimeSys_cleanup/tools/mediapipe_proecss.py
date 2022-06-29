import cv2
import keyboard
import numpy as np
import mediapipe as mp
from collections import deque
import argparse
import math
from typing import List, Tuple, Union
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.mplot3d import Axes3D

def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    # TODO: Draw coordinates even if it's outside of the image bounds.
    # print("TODO: Draw coordinates even if it's outside of the image bounds.")
    return None,None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px

PRESENCE_THRESHOLD = 0.5
RGB_CHANNELS = 3
RED_COLOR = (0, 0, 255)
VISIBILITY_THRESHOLD = 0.5

def larry_draw(image,landmark_list,connections):
    x=[]
    y=[]
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    if not landmark_list:
        return
    if image.shape[2] != RGB_CHANNELS:
        raise ValueError('Input image must contain three channel rgb data.')
    image_rows, image_cols, _ = image.shape
    # print(image.shape)
    idx_to_coordinates = {}
    for idx, landmark in enumerate(landmark_list.landmark):
        if ((landmark.HasField('visibility') and
             landmark.visibility < VISIBILITY_THRESHOLD) or
                (landmark.HasField('presence') and
                 landmark.presence < PRESENCE_THRESHOLD)):
            continue
        tmpx,tmpy = _normalized_to_pixel_coordinates(landmark.x, landmark.y,
                                                           image_cols, image_rows)
        x.append(tmpx)
        y.append(tmpy)
    # ax.scatter(x,y,cmap='Greens')
    # plt.show()
    return x,y

def plot_hand(fig,elev,azim,x1,x2,y2,px,py,pz,mode):
    fig.clf()
    mark = "."
    ax = fig.gca(projection='3d')
    ax.set_xlim(0, 640)  # X軸，橫向向右方向
    ax.set_ylim(0, 480)  # Y軸,左向與X,Z軸互為垂直
    ax.set_zlim(0, 640)  # 豎向為Z軸
    ax.plot3D(x1[1:5],x2[1:5],y2[1:5] ,marker=mark,color="gray" )
    ax.plot3D(x1[5:9],x2[5:9],y2[5:9] ,marker=mark,color="gray" )
    ax.plot3D(x1[9:13],x2[9:13],y2[9:13] ,marker=mark, color="gray")
    ax.plot3D(x1[13:17],x2[13:17],y2[13:17] ,marker=mark, color="gray")
    ax.plot3D(x1[17:],x2[17:],y2[17:] ,marker=mark,color="gray" )
    ax.scatter(0,0,0,marker="o")
    ax.view_init(elev=elev,azim=azim)
    ax.set_xlabel("x axis")
    ax.set_ylabel("y axis")
    ax.set_zlabel("z axis")
    # palm = []
    palmx =[x1[0],x1[5],x1[9],x1[13],x1[17],x1[0],x1[1]]
    palmy =[x2[0],x2[5],x2[9],x2[13],x2[17],x2[0],x2[1]]
    palmz =[y2[0],y2[5],y2[9],y2[13],y2[17],y2[0],y2[1]]
    ax.plot3D(palmx,palmy,palmz ,marker=mark,color = "gray")
    # ax.plot3D(x1[4], x2[4], y2[4], marker="8", color="Red")
    ax.scatter(x1[8], x2[8], y2[8], marker=mark, color="Red")
    ax.plot3D(px,py,pz,color="Red")
    plt.draw()
    if mode == "avg":
        return x1[8],x2[8],y2[8]