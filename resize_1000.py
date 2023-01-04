import os
import glob

from PIL import Image
Image.MAX_IMAGE_PIXELS = 933120000

DIR_WITH_IMAGES = '/Users/andrey.matveev/aspire/MIDJORNEY_IMAGES'
OUTPUT_DIR = os.path.join(os.getcwd(), "output")

INPUT_FORMAT = '.png'
OUTPUT_FORMAT = '.png'


def process_image(image_path):
    img = Image.open(image_path)
    res_image = img.resize((1000, 1000))
    img_name = os.path.basename(image_path).split(INPUT_FORMAT)[0]
    res_name = f'1000x1000_{img_name}{OUTPUT_FORMAT}'
    res_path = os.path.join(OUTPUT_DIR, res_name)
    res_image.save(res_path)


for image_path in glob.glob(f'{DIR_WITH_IMAGES}/*{INPUT_FORMAT}'):
    process_image(image_path)