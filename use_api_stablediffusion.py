import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "http://127.0.0.1:7860"

payload = {
    "prompt": "beautiful, slim body, red lips, naked blonde girl, stockings, ((RAW, analog style)), {wide angle, extremely detailed photo of a *subject*}, ((film grain, skin details, high detailed skin texture, 8k hdr, dslr))",
    "negative_prompt": "((((realistic, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime)))), cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck",
    "steps": 20,
    "seed": -1,
    "width": 512,
    "height": 768,
    "cfg_scale": 7,
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save('generated.png', pnginfo=pnginfo)