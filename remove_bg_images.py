from rembg import remove
from PIL import Image

input_path = '/Users/andrey.matveev/Downloads/IMG_0572.png'
# input_path = 'output.png'
# output_path = 'output1.png'

input = Image.open(input_path)
input.save('output2.png')
# output = remove(input)
# output.save(output_path)