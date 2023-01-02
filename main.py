import os
import glob
from PIL import Image

DIR_WITH_IMAGES = '/Users/andrey.matveev/aspire/MIDJORNEY_IMAGES'
DPI = (50, 50)

print('Named explicitly:')
for image_path in glob.glob(f'{DIR_WITH_IMAGES}/*.png'):
    img = Image.open(image_path)
    print(img.width)
    print(img.height)
    img_name = os.path.basename(image_path).split('.png')[0]
    print(img_name)
    img.save(f'res{DPI}_{img_name}.jpg', dpi=DPI)

