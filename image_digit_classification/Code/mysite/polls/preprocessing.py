from PIL import Image, ImageFilter
import numpy as np

def imageprepare(path):
    im = Image.open(path).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    print(width, height)
    newImage = Image.new('L', (28, 28), (255)) # Creating white canvas of 28*28 pixels - mnist format
    if (width > height):
        # Checking if the dimensions are not correct
        nheight = int(round(20.0/width * height)) # Resetting height according to ratio width
        if nheight == 0:
           nheight = 1

        # Sharpening the image
        img = im.resize((20, nheight), Image.LANCZOS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight)/2), 0)) # calculating horizontal position
        newImage.paste(img, (4, wtop))

    else:
        # height is bigger, resize it
        nwidth = int(round(20.0 / height*width))
        if nwidth == 0:
            nwidth = 1

        # Sharpening the image
        img = im.resize((nwidth, 20), Image.LANCZOS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - width)/2), 0)) # Calculating vertical position
        newImage.paste(img, (wleft, 4))

    tv = list(newImage.getdata()) # get pixel values
    tva = [(255 - x)*1.0 / 255.0 for x in tv]
    var = np.array(tva).reshape(1, 784)
    return var