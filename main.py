import os
import glob
from PIL import Image

DIR_WITH_IMAGES = '/Users/andrey.matveev/aspire/MIDJORNEY_IMAGES'
DPI = (50, 50)
SIZES = ((8, 10), (11, 14), (16, 20), (83, 117))


def get_color_value(color):
    return color[0] + color[1] * 256 + color[2] * 256 * 256


def continue_background(img):
    REPEAT_PIXELS = 30

    w = img.width
    h = img.height
    j_start = (h - w) // 2 - 1
    for dj in range(0, j_start + 1):
        for i in range(0, w):
            img.putpixel((i, j_start - dj), img.getpixel((i, j_start + dj + 1)))

    j_start = (h - w) // 2 + w
    for dj in range(0, (h - w) // 2):
        for i in range(0, w):
            img.putpixel((i, j_start + dj), img.getpixel((i, j_start - dj - 1)))


def calculate_stat(img):
    mm = {}
    for i in range(0, 100):
        for j in range(0, 100):
            vcol = get_color_value(img.getpixel((i, j)))
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    ci = i + di
                    cj = j + dj
                    if ci < 0 or ci >= img.width or cj < 0 or cj >= img.height:
                        continue
                    ccol = img.getpixel((ci, cj))
                    if vcol not in mm:
                        mm[vcol] = set()
                    mm[vcol].add(get_color_value(ccol))
    return mm


def process_image(image_path):
    img = Image.open(image_path)
    mm = calculate_stat(img)
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
        res_image.paste(resized_image, (0, (h - w) // 2))
        continue_background(res_image, mm)
        res_name = f'{ww}_{hh}_{w}_{h}_{dpi}_{img_name}.jpg'
        print(res_name)
        res_image.save(res_name, dpi=(dpi, dpi))


print('Named explicitly:')
for image_path in glob.glob(f'{DIR_WITH_IMAGES}/*.png'):
    process_image(image_path)


