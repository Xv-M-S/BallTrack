# -*- coding:utf-8 -*-
# Author: RubanSeven

import cv2
import imageio
from augment import distort, stretch, perspective
from utils import resize_and_pad

def create_gif(image_list, gif_name, duration=200):
    frames = []
    for image in image_list:
        frames.append(image)
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return

def create_video(image_list, video_name, fps=4):
    # Get the dimensions from the first image
    height, width, _ = image_list[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
    video_writer = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    for image in image_list:
        video_writer.write(image)

    video_writer.release()

if __name__ == '__main__':

    im = resize_and_pad("imgs/1.jpg")
    distort_img_list = list()
    stretch_img_list = list()
    perspective_img_list = list()
    for i in range(48):
        distort_img = distort(im, 3)
        distort_img_list.append(distort_img)

        stretch_img = stretch(im, 3)
        stretch_img_list.append(stretch_img)

        perspective_img = perspective(im)
        perspective_img_list.append(perspective_img)

    create_gif(distort_img_list, r'imgs/distort.gif')
    create_gif(stretch_img_list, r'imgs/stretch.gif')
    create_gif(perspective_img_list, r'imgs/perspective.gif')

    create_video(distort_img_list, r'videos/distort.mp4')
    create_video(stretch_img_list, r'videos/stretch.mp4')
    create_video(perspective_img_list, r'videos/perspective.mp4')