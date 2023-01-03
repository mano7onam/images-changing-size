import glob
import os
import shutil

from PIL import Image

DIR_WITH_IMAGES = '/Users/andrey.matveev/aspire/MIDJORNEY_IMAGES'
DIR_WITH_IMAGES = os.path.join(os.getcwd(), "output")
OUTPUT_DIR = os.path.join(os.getcwd(), "output_new")
INPUT_FORMAT = '.png'
OUTPUT_FORMAT = '.jpg'

SIZES = ((8, 10), (11, 14), (16, 20), (83, 117))

def process_image(image_path):
    img = Image.open(image_path)
    img_name = os.path.basename(image_path).split(INPUT_FORMAT)[0]

    for size in SIZES:
        w = img.width
        h = img.height
        ww = size[0]
        hh = size[1]
        if w % ww != 0 or h % hh != 0:
            continue
        dpi = w // ww
        if ww == 83:
            dpi *= 10
        res_name = f'{w}_{h}_{dpi}_{img_name}{OUTPUT_FORMAT}'
        res_dir_name = f'{ww}x{hh}'
        res_dir_path = os.path.join(OUTPUT_DIR, res_dir_name)
        if not os.path.isdir(res_dir_path):
            os.makedirs(res_dir_path)
        img.save(os.path.join(res_dir_path, res_name), dpi=(dpi, dpi))


def zip_directories():
    for size in SIZES:
        ww = size[0]
        hh = size[1]
        res_dir_name = f'{ww}x{hh}'
        res_dir_path = os.path.join(OUTPUT_DIR, res_dir_name)
        zip_path = os.path.join(OUTPUT_DIR, res_dir_name)
        shutil.make_archive(zip_path, 'zip', res_dir_path)


for image_path in glob.glob(f'{DIR_WITH_IMAGES}/*{INPUT_FORMAT}'):
    print(image_path)
    process_image(image_path)

zip_directories()
