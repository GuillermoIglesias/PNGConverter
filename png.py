import zlib
import struct
import sys

def main():
    if (len(sys.argv) == 1):
        return print('Error: python png.py <archivo.bmp>')

    input_name = (sys.argv[1][:-4])

    bmp_data = open(sys.argv[1], "rb").read()

    png_data = convertToPNG(bmp_data)

    output = open(input_name + '_.png','wb')
    output.write(png_data)  
    output.close()

def convertToPNG(source):
    # Extraer data desde fuente
    data, width, height = imageSource(source)

    def B1(value):
        return struct.pack("!B", value & (2**8-1))
    def B4(value):
        return struct.pack("!I", value & (2**32-1))

    # Firma Header PNG
    png = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')

    # Chunk: IHDR
    colortype = 2 # RGB 
    bitdepth = 8 # Un byte por pixel (0-255)
    compression = 0 # Función zlib (default)
    filtertype = 0 # Adaptivo 
    interlaced = 0 # No
    IHDR = B4(width) + B4(height) + B1(bitdepth)
    IHDR += B1(colortype) + B1(compression)
    IHDR += B1(filtertype) + B1(interlaced)
    block = "IHDR".encode('ascii') + IHDR
    png += B4(len(IHDR)) + block + B4(zlib.crc32(block))

    # Chunk: IDAT
    raw = b""
    for i in range(height):
        raw += b"\0" # Sin filtro
        for j in range(width*3):
            c = b"\0" # Pixel negro por defecto
            if i < len(data) and j < len(data[i]):
                c = B1(data[i][j])
            raw += c
    compressor = zlib.compressobj()
    compressed = compressor.compress(raw)
    compressed += compressor.flush() 
    block = "IDAT".encode('ascii') + compressed
    png += B4(len(compressed)) + block + B4(zlib.crc32(block))

    # Chunk: IEND
    block = "IEND".encode('ascii')
    png += B4(0) + block + B4(zlib.crc32(block))

    return png

def imageSource(raw):

    x = sum(raw[18:22])
    y = sum(raw[22:26])
    d = sum(raw[10:14])
    data = raw[d:] 

    image = [[] for i in range(y)] 
    pad = 0
    if (x * 3 % 4 != 0): 
        pad = 4 - (x * 3 % 4)

    for i in range(y):
        pos = i * (x * 3 + pad)
        for j in range(0, x * 3, 3):
            image[i].append(data[pos + j + 2]) # B
            image[i].append(data[pos + j + 1]) # G
            image[i].append(data[pos + j]) # R
            
    return image[::-1], x , y

if __name__ == '__main__':
    main()