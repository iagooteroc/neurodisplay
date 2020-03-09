import cv2
import numpy as np
import os
import nibabel as nib
import sys
import argparse

img = None
img_bot = None
lab = None
lab_bot = None
lab_max = None
title_window = None
colormap = None
brain_size = None

# example: 
# python neurodisplay.py -i images/2013_15_1_t1.nii.gz -j images_t1ce/2013_15_1_t1ce.nii.gz -x pred/2013_15_1_t1.nii.gz -y labels/2013_15_1_lab.nii.gz

def display(img_path, img_path2, lab_path, lab_path2):
    global lab, lab_bot, img, img_bot, lab_max, title_window, colormap, brain_size
    img = nib.load(img_path)
    brain_size = img.shape
    title_window = "Top: " + img_path.split("/")[-1]
    if lab_path:
        lab = nib.load(lab_path)
    if img_path2:
        img_bot = nib.load(img_path2)
        title_window += " / Botton: " + img_path2.split("/")[-1]
    if lab_path2:
        lab_bot = nib.load(lab_path2)

    alpha_slider_max = img.shape[2] - 1

    cv2.namedWindow(title_window)
    trackbar_name = 'Cut z'
    # colormap = cv2.COLORMAP_COOL
    colormap = cv2.COLORMAP_BONE
    cv2.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar_bin)
    on_trackbar_bin(0)

    # Wait until user press some key
    cv2.waitKey()
    cv2.destroyAllWindows()

def build_brain(image, val):
    img1 = image.get_fdata()[val,:,:].astype(np.uint8)
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2RGB)
    img2 = image.get_fdata()[:,val,:].astype(np.uint8)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2RGB)
    img3 = image.get_fdata()[:,:,val].astype(np.uint8)
    img3 = cv2.cvtColor(img3,cv2.COLOR_GRAY2RGB)
    img_stack = np.hstack((img1, img2))
    return np.hstack((img_stack, img3))

def build_label(label, val):
    if not label:
        return np.zeros((brain_size[0], brain_size[1]*3, 3)).astype(np.uint8)
    lab1 = ((label.get_fdata()[val,:,:] > 0) * 255).astype(np.uint8)
    lab1 = cv2.applyColorMap(lab1, colormap)
    lab2 = ((label.get_fdata()[:,val,:] > 0) * 255).astype(np.uint8)
    lab2 = cv2.applyColorMap(lab2, colormap)
    lab3 = ((label.get_fdata()[:,:,val] > 0) * 255).astype(np.uint8)
    lab3 = cv2.applyColorMap(lab3, colormap)
    img_stack2 = np.hstack((lab1, lab2))
    return np.hstack((img_stack2, lab3))

def on_trackbar_bin(val):
    img_stack = build_brain(img, val)
    if img_bot:
        img_bot_stack = build_brain(img_bot, val)
    elif lab_bot:
        img_bot_stack = img_stack.copy()
    else: # if there is no second brain nor label image, display one row only
        lab_stack = build_label(lab, val)
        dst = cv2.addWeighted(img_stack, 0.5, lab_stack, 0.5, 0.0)
        cv2.imshow(title_window, dst)
        return
    img_brain_stack = np.vstack((img_stack, img_bot_stack))
    lab_stack = build_label(lab, val)
    lab_bot_stack = build_label(lab_bot, val)
    lab_total_stack = np.vstack((lab_stack, lab_bot_stack))
    dst = cv2.addWeighted(img_brain_stack, 0.5, lab_total_stack, 0.5, 0.0)
    cv2.imshow(title_window, dst)

if __name__ == '__main__':
    img_path = None
    img_path2 = None
    lab_path = None
    lab_path2 = None
    parser = argparse.ArgumentParser(description='Display neuroimages with binary labels. At least one brain image (-i) is required')
    parser.add_argument('-i', type=str, help='path to the top brain image (required)', required=True)
    parser.add_argument('-j', type=str, help='path to the bottom brain image')
    parser.add_argument('-x', type=str, help='path to the top label image')
    parser.add_argument('-y', type=str, help='path to the bottom label image')

    args = parser.parse_args()

    display(args.i, args.j, args.x, args.y)
