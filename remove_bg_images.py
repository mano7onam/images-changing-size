from rembg import remove
from PIL import Image

input_path = 'crop.png'
# input_path = 'output.png'
output_path = 'output42.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)