import os
import glob

from PIL import Image
Image.MAX_IMAGE_PIXELS = 933120000

DESIRED_SIZE_W = 512
DESIRED_SIZE_H = 512

DIR_WITH_IMAGES = '/Users/andrey.matveev/aspire/IMGS/WATERCOLOUR'
OUTPUT_DIR = '/Users/andrey.matveev/aspire/IMGS/WATERCOLOUR_RESIZED_512_JPEG'
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

INPUT_FORMAT = ['.png', '.jpg']
OUTPUT_FORMAT = '.jpeg'


def process_image(image_path, input_format):
    img = Image.open(image_path)
    res_image = img.resize((DESIRED_SIZE_W, DESIRED_SIZE_H))
    img_name = os.path.basename(image_path).split(input_format)[0]
    res_name = f'{DESIRED_SIZE_W}x{DESIRED_SIZE_H}_{img_name}{OUTPUT_FORMAT}'
    res_path = os.path.join(OUTPUT_DIR, res_name)
    res_image.save(res_path)


cnt = 0
for input_format in INPUT_FORMAT:
    for image_path in glob.glob(f'{DIR_WITH_IMAGES}/*{input_format}'):
        cnt += 1
        process_image(image_path, input_format)
print(cnt)
