from PIL import Image, ImageDraw
from random import randint

def main():
    # Cantidad y tamaño
    nImages = 30
    width = 20
    height = 20

    # Barras verticales
    for i in range(nImages):
        filename = "bar" + str(i + 1) + ".bmp" 
        barImage(filename, width, height)

    # Pixeles de color
    for i in range(nImages):
        filename = "pixel" + str(i + 1) + ".bmp" 
        pixelImage(filename, width, height)

def barImage(filename, width, height):
    img = Image.new('RGB', (width, height), color="white")
    for i in range(width):
        red, green, blue = randint(0,255), randint(0,255), randint(0,255)
        draw = ImageDraw.Draw(img)
        draw.line((i, img.height, i, 0), fill=(red, green, blue))
        del draw
    img.save("input/" + filename)

def pixelImage(filename, width, height):
    img = Image.new('RGB', (width, height), color="white")
    for i in range(width):
        for j in range(height):
            red, green, blue = randint(0,255), randint(0,255), randint(0,255)
            draw = ImageDraw.Draw(img)
            draw.point((i,j), fill=(red, green, blue))
            del draw
    img.save("input/" + filename)

if __name__ == '__main__':
    main()