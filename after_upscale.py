import os
import glob
import random
from collections import Counter

from PIL import Image
DIR_WITH_IMAGES = '/Users/andrey.matveev/aspire/MIDJORNEY_IMAGES'
SIZES = ((8, 10), (11, 14), (16, 20), (83, 117))

def process_image(image_path):
    img = Image.open(image_path)
    img_name = os.path.basename(image_path).split('.png')[0]

    for size in SIZES:
        x = img.width
        ww = size[0]
        hh = size[1]
        w = x - x % ww
        h = (w // ww) * hh
        dpi = w // ww
        if ww == 83:
            dpi *= 10
        bg_color = img.getpixel((0, 0))
        print(bg_color)
        res_image = Image.new("RGB", (w, h), bg_color)
        resized_image = img.resize((w, w))
        # mm, mmm = calculate_stat(resized_image)
        res_image.paste(resized_image, (0, (h - w) // 2))
        # continue_background(res_image, mm, mmm)
        # continue_background_reverse(res_image)
        res_name = f'{ww}_{hh}_{w}_{h}_{dpi}_{img_name}.jpg'
        print(res_name)
        res_image.save(res_name, dpi=(dpi, dpi))


for image_path in glob.glob(f'{DIR_WITH_IMAGES}/*.png'):
    process_image(image_path)
