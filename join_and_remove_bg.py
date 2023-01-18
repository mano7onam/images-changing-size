import glob
import json
import os.path

from tqdm import tqdm

from helpers import get_model_dir_name
from remove_bg_images import remove_bg

RES_DIR = 'joined_removed_bg'
if not os.path.isdir(RES_DIR):
    os.makedirs(RES_DIR)


def start():
    with open("config.json") as f:
        obj = json.load(f)
        all_models = obj['models']

    all_files = []
    for model in all_models:
        model_dir_name = get_model_dir_name(model)
        print(model_dir_name)
        if not os.path.isdir(model_dir_name):
            continue
        abs_path = os.path.abspath(model_dir_name)
        png_names = list(filter(lambda x: x.endswith('.png'), os.listdir(abs_path)))
        png_names = list(map(lambda x: os.path.join(abs_path, x), png_names))
        all_files.extend(png_names)
    print(all_files)

    for img_file in tqdm(all_files):
        base_path = os.path.basename(img_file)
        model_dir_name = os.path.basename(os.path.dirname(img_file))
        remove_bg(img_file, os.path.join(RES_DIR, f'{model_dir_name}_{base_path}'))


# print(glob.glob('/Users/andrey.matveev/PycharmProjects/ImgCenterPaste/*.png'))
start()
