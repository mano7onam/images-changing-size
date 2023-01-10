import glob
import os.path

from PIL import Image
from rembg import remove
from tqdm import tqdm

out_dir = 'output_dir_rm_bg'
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)


def remove_bg(img_path, output_path):
    input = Image.open(img_path)
    output = remove(input)
    output.save(output_path)


imgs_paths = glob.glob('output_dir/*.png')
for img_path in tqdm(imgs_paths):
    basename = os.path.basename(img_path)
    output_path = os.path.join(out_dir, basename)
    remove_bg(img_path, output_path)
