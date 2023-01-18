import glob
import json
import os

import requests
import io
import base64
from PIL import Image, PngImagePlugin

from helpers import get_model_dir_name

URL = "http://127.0.0.1:7860"


def process_files_get_prompts(files_or_globs):
    all_files = []
    res_all_prompts = []
    for file in files_or_globs:
        if file.startswith('glob::::'):
            glob_str = file.split('::::')[1]
            cur_files = glob.glob(glob_str)
            all_files.extend(cur_files)
        elif file.startswith('prompt::::'):
            cur_prompt = file.split('::::')[1]
            res_all_prompts.append(cur_prompt)
        else:
            all_files.append(file)

    for file in all_files:
        with open(file, 'r') as f:
            for line in f:
                to_add = line
                if line.endswith('\n'):
                    to_add = line[:-1]
                res_all_prompts.append(to_add)
    return res_all_prompts


def process_one_request(iteration, model_dir_name, prompt, negative_prompt, img_width, img_height):
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": 20,
        "seed": -1,
        "width": img_width,
        "height": img_height,
        "cfg_scale": 7
    }

    response = requests.post(url=f'{URL}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{URL}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        start_prompt = prompt[:30]
        hash_prompt = hash(prompt)
        hash_negative_prompt = hash(negative_prompt)
        print(hash_prompt, hash_negative_prompt)
        base_img_path = f'{start_prompt}_{hash_prompt}_{hash_negative_prompt}_{iteration}.png'
        res_img_name = os.path.join(model_dir_name, base_img_path)
        image.save(res_img_name, pnginfo=pnginfo)


def process_requests(model_dir_name, prompt, negative_prompt, repetitions, img_width, img_height):
    for i in range(0, repetitions):
        print(i)
        process_one_request(i, model_dir_name, prompt, negative_prompt, img_width, img_height)


def start():
    with open("config.json") as f:
        obj = json.load(f)
        all_models = obj['models']
        all_prompts = process_files_get_prompts(obj['files_with_prompts'])
        all_negative_prompts = process_files_get_prompts(obj['negative_prompts'])
        img_height = obj['height']
        img_width = obj['width']
        repetitions = obj['repetitions']
        print(all_models)
        print(all_prompts)
        print(all_negative_prompts)

    if len(all_negative_prompts) == 0:
        all_negative_prompts.append('')

    for model in all_models:
        print(model)
        model_dir_name = get_model_dir_name(model)
        if not os.path.isdir(model_dir_name):
            os.makedirs(model_dir_name)
        option_payload = {
            "sd_model_checkpoint": model
        }
        response = requests.post(url=f'{URL}/sdapi/v1/options', json=option_payload)
        print(response.status_code)
        if response.status_code != 200:
            continue
        print(all_prompts)
        for prompt in all_prompts:
            for negative_prompt in all_negative_prompts:
                print(prompt)
                print(negative_prompt)
                process_requests(model_dir_name, prompt, negative_prompt, repetitions, img_width, img_height)


start()
