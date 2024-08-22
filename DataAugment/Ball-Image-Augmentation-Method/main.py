# -*- coding:utf-8 -*-
# Author: RubanSeven

import cv2
import imageio
from augment import distort, stretch, perspective
from utils import resize_and_pad

def create_gif(image_list, gif_name, duration=0.1):
    frames = []
    for image in image_list:
        frames.append(image)
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return


if __name__ == '__main__':

    im = resize_and_pad("imgs/1.jpg")
    distort_img_list = list()
    stretch_img_list = list()
    perspective_img_list = list()
    for i in range(24):
        distort_img = distort(im, 3)
        distort_img_list.append(distort_img)

        stretch_img = stretch(im, 3)
        stretch_img_list.append(stretch_img)

        perspective_img = perspective(im)
        perspective_img_list.append(perspective_img)

    create_gif(distort_img_list, r'imgs/distort.gif')
    create_gif(stretch_img_list, r'imgs/stretch.gif')
    create_gif(perspective_img_list, r'imgs/perspective.gif')