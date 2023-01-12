import glob
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

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
                res_all_prompts.append(line)
    return res_all_prompts


def process_request(prompt, negative_prompt):
    print(prompt)
    print(negative_prompt)
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": 20,
        "seed": -1,
        "width": 512,
        "height": 512,
        "cfg_scale": 7,
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
        image.save('generated.png', pnginfo=pnginfo)


def start():
    with open("config.json") as f:
        obj = json.load(f)
        all_models = obj['models']
        all_prompts = process_files_get_prompts(obj['files_with_prompts'])
        all_negative_prompts = process_files_get_prompts(obj['negative_prompts'])
        print(all_models)
        print(all_prompts)
        print(all_negative_prompts)

    for model in all_models:
        print(model)
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
                print(all_negative_prompts)
                process_request(prompt, negative_prompt)


start()
