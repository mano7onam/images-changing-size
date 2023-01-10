from PIL import Image

input_path = '/Users/andrey.matveev/Downloads/IMG_0572.png'
img = Image.open(input_path)
WHITE = (255, 255, 255)

imin = 1e10
imax = -1e10
jmin = 1e10
jmax = -1e10
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
        else:
            print('aaaa')
imin = max(0, imin - 10)
imax = min(img.width, imax + 10)
jmin = max(0, jmin - 10)
jmax = min(img.height, jmax + 10)

crop_img = img.crop((imin, jmin, imax, jmax))
fill_col = (255, 255, 255, 255)
for i in range(0, crop_img.width):
    for j in range(0, crop_img.height):
        col = crop_img.getpixel((i, j))
        if len(col) == 4 and col != (0, 0, 0, 0):
            fill_col = col
            break
print(fill_col)

for i in range(0, crop_img.width):
    for j in range(0, crop_img.height):
        col = crop_img.getpixel((i, j))
        if len(col) == 4 and col == (0, 0, 0, 0):
            crop_img.putpixel((i, j), fill_col)

crop_img.save('crop.png')