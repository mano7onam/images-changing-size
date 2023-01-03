import os
import glob
import random
from collections import Counter

from PIL import Image

DIR_WITH_IMAGES = '/Users/andrey.matveev/aspire/MIDJORNEY_IMAGES'
DPI = (50, 50)
SIZES = ((8, 10), (11, 14), (16, 20), (83, 117))


def get_color_value(color):
    return color[0] + color[1] * 256 + color[2] * 256 * 256


def get_value_color(value):
    r = value % 256
    value //= 256
    g = value % 256
    value //= 256
    b = value % 256
    return (r, g, b)


def continue_background(img, mm, mmm):
    w = img.width
    h = img.height
    j_start = (h - w) // 2 - 1
    RAD = 5
    dds = [(0, 1)]
    for di in range(-RAD, 0):
        dds.append((di, 0))
    for di in range(-RAD, RAD):
        for dj in range(1, RAD):
            if di == 0 and dj == 1:
                continue
            dds.append((di, dj))
    for j in range(j_start, -1, -1):
        print(j)
        for i in range(0, w):
            dind = random.randint(0, len(dds) - 1)
            cur_d = dds[dind]
            ci = i + cur_d[0]
            cj = j + cur_d[1]
            if ci < 0 or ci >= img.width or cj < 0 or cj >= img.height:
                ci = i + dds[0][0]
                cj = j + dds[0][1]
            col = img.getpixel((ci, cj))
            col = get_color_value(col)
            # colors = mm[col]
            # ind = random.randint(0, len(colors) - 1)
            # col = colors[ind]
            col = mmm[col]
            img.putpixel((i, j), get_value_color(col))

    j_start = (h - w) // 2 + w
    for dj in range(0, (h - w) // 2):
        for i in range(0, w):
            img.putpixel((i, j_start + dj), img.getpixel((i, j_start - dj - 1)))


def calculate_stat(img):
    mm = {}
    mmm = {}
    w = img.width
    h = img.height
    for i in range(0, 10):
        for j in range(0, h):
            vcol = get_color_value(img.getpixel((i, j)))
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if di == 0 and dj == 0:
                        continue
                    ci = i + di
                    cj = j + dj
                    if ci < 0 or ci >= img.width or cj < 0 or cj >= img.height:
                        continue
                    ccol = img.getpixel((ci, cj))
                    if vcol not in mm:
                        mm[vcol] = []
                    mm[vcol].append(get_color_value(ccol))
    for j in range(0, 10):
        for i in range(0, w):
            vcol = get_color_value(img.getpixel((i, j)))
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if di == 0 and dj == 0:
                        continue
                    ci = i + di
                    cj = j + dj
                    if ci < 0 or ci >= img.width or cj < 0 or cj >= img.height:
                        continue
                    ccol = img.getpixel((ci, cj))
                    if vcol not in mm:
                        mm[vcol] = []
                    mm[vcol].append(get_color_value(ccol))
    for (key, val) in mm.items():
        newl = []
        for el in val:
            if el in mm:
                newl.append(el)
        counter = Counter(newl)
        mm[key] = newl
        mmm[key] = counter.most_common(1)[0][0]
    return mm, mmm


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
        mm, mmm = calculate_stat(resized_image)
        res_image.paste(resized_image, (0, (h - w) // 2))
        continue_background(res_image, mm, mmm)
        res_name = f'{ww}_{hh}_{w}_{h}_{dpi}_{img_name}.jpg'
        print(res_name)
        res_image.save(res_name, dpi=(dpi, dpi))


print('Named explicitly:')
for image_path in glob.glob(f'{DIR_WITH_IMAGES}/*.png'):
    process_image(image_path)


