import glob
import os.path
import sys

from PIL import Image
from tqdm import tqdm


def crop_image(input_path, output_path):
    img = Image.open(input_path)
    imin = 1e10
    imax = -1e10
    jmin = 1e10
    jmax = -1e10
    flag = False
    for i in range(0, img.width):
        for j in range(0, img.height):
            col = img.getpixel((i, j))
            if len(col) == 4:
                if col == (0, 0, 0, 0):
                    continue
                imin = min(imin, i)
                imax = max(imax, i)
                jmin = min(jmin, j)
                jmax = max(jmax, j)
                flag = True
            else:
                print('aaaa')
    if not flag:
        return
    imin = max(0, imin - 10)
    imax = min(img.width, imax + 10)
    jmin = max(0, jmin - 10)
    jmax = min(img.height, jmax + 10)
    print(input_path, file=sys.stderr)
    print(imin, imax, jmin, jmax, file=sys.stderr)

    crop_img = img.crop((imin, jmin, imax, jmax))
    fill_col = (255, 255, 255, 255)
    for i in range(0, crop_img.width):
        for j in range(0, crop_img.height):
            col = crop_img.getpixel((i, j))
            if len(col) == 4 and col != (0, 0, 0, 0):
                fill_col = col
                break
    print(fill_col, file=sys.stderr)

    for i in range(0, crop_img.width):
        for j in range(0, crop_img.height):
            col = crop_img.getpixel((i, j))
            if len(col) == 4 and col == (0, 0, 0, 0):
                crop_img.putpixel((i, j), fill_col)

    crop_img.save(output_path)


out_dir = 'output_dir'
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

imgs_paths = glob.glob('/Users/andrey.matveev/aspire/IMGS/TO_RM_BG/*.png')
for img_path in tqdm(imgs_paths):
    basename = os.path.basename(img_path)
    output_path = os.path.join(out_dir, basename)
    crop_image(img_path, output_path)

