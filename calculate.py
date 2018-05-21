from png import convertToPNG
from glob import glob

def main():
    filedir = glob("input/*.bmp")
    
    bmp_size, png_size, compress = [], [], []

    for i in range(len(filedir)):
        filename = filedir[i][6:-4]

        bmp_data = open(filedir[i].replace("\\","/"), "rb").read()
        png_data = convertToPNG(bmp_data)

        compress_rate = (len(bmp_data) - len(png_data)) / len(png_data)
        compress_rate = round(compress_rate * 100.0, 2)

        bmp_size.append(len(bmp_data))
        png_size.append(len(png_data))
        compress.append(compress_rate)

        output = open('output/' + filename + '_.png','wb')
        output.write(png_data)  
        output.close()
    
    values = int(len(bmp_size)/2)
    print("··· Imagen Barra ···")
    print("Total:", len(bmp_size[:values]), "imágenes")
    print("BMP:", int(sum(bmp_size[:values])/values), "bytes")
    print("PNG:", int(sum(png_size[:values])/values), "bytes")
    print("Compresión:",round(sum(compress[:values])/values,2), "%")
    print("··· Imagen Pixel ···")
    print("Total:", len(bmp_size[values:]), "imágenes")
    print("BMP:", int(sum(bmp_size[values:])/values), "bytes")
    print("PNG:", int(sum(png_size[values:])/values), "bytes")
    print("Compresión:",round(sum(compress[values:])/values,2), "%")

if __name__ == '__main__':
    main()    