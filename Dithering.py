


from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
import numpy as np


image_path = "YOUR_IMAGE_HERE!"  # Replace with your image file path
img = Image.open(image_path)
imsize = 4
img = img.resize((img.width // imsize, img.height // imsize))


# Convert the image to a NumPy array (pixel matrix)
# For RGB images (Height x Width x Channels)
# For grayscale images, it will be HxW
picturebad = np.asarray(img)
picture = picturebad[:, :, :3]
#Assuming 'grayscale_values_array' is a 2D NumPy array with grayscale intensity values (e.g., 0-255)
print(picture.shape)
colors = 2
def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    #gray = np.sqrt(r**2 + g**2 + b**2)
    return gray

print('greyshape',rgb2gray(picture).shape)
graypic = rgb2gray(picture)
newpic = np.zeros_like(graypic)
print('greyshape again',graypic.shape)
hight,width = graypic.shape
for y in range(0,hight-4):
    for x in range(0,width-4):
        oldpixle = graypic[y,x]
        #print('shape of grayimg', graypic.shape)
        #DONT USE THE LEVEL BS 
        #level = int(oldpixle / colors) * colors  #  levels: 0, 32, 64, 96, 128, 160, 192, 224
        # newpic[y,x] = level
        if oldpixle <= (255.0/4.0):
            newpic[y,x] = 0
        elif oldpixle<= (255.0/2.0):
            newpic[y,x] = (255.0/3.0)
        elif oldpixle<= (3*(255.0/4.0)):
            newpic[y,x] = (2*255.0/3.0)
        else: 
            newpic[y,x] = 255.0
        quant_error = graypic[y,x] - newpic[y,x]

        #-------------------------
        #Floid-Stienberg-Dithering
        #-------------------------
        #graypic[y,x+1] = graypic[y,x+1] + quant_error*(7/16.0)
        #graypic[y+1,x-1] = graypic[y+1,x-1] + quant_error*(3/16.0)
        #graypic[y+1,x] = graypic[y+1,x] + quant_error*(5/16.0)
        #graypic[y+1,x+1] = graypic[y+1,x+1] + quant_error*(1/16.0)
       
        #-------------------------
        #Bill-Atkinson-Dithering--
        #-------------------------
        graypic[y, x+1] = graypic[y, x+1] + quant_error*(1/8.0)
        graypic[y, x+2] = graypic[y, x+2] + quant_error*(1/8.0)
        graypic[y+1, x-1] = graypic[y+1, x-1] + quant_error*(1/8.0)
        graypic[y+1, x] = graypic[y+1, x] + quant_error*(1/8.0)
        graypic[y+1, x+1] = graypic[y+1, x+1] + quant_error*(1/8.0)
        graypic[y+2, x] = graypic[y+2, x] + quant_error*(1/8.0)

def circle_dith(img, spacing=100, max_r=1):
    h, w = img.shape
    output = Image.new('L', (w, h), 255)
    draw = ImageDraw.Draw(output)

    for y in range(0, h, spacing):
        for x in range(0, w, spacing):
            region = img[y:y + spacing, x:x + spacing]
            darkness = 255 - np.mean(region)
            radius = (darkness * max_r) / 255
            if radius >= 0.85:
                draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=1)

    return output

graypicirlce = circle_dith(newpic,3,4) #CHANGE SPACING AND CIRCLE SIZE HERE 
print('great success')
#print(circletime.shape)



plt.imshow(newpic,cmap = "rainbow")
plt.show()
plt.imshow(graypicirlce, cmap = 'plasma')
plt.show()
