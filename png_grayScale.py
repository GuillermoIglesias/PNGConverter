import zlib
import struct
import sys

def convertToPNG(data, height=None, width=None):
    def B1(value):
        return struct.pack("!B", value & (2**8-1))
    def B4(value):
        return struct.pack("!I", value & (2**32-1))

    if height is None:
        height = len(data)
    if width is None:
        width = 0
        for row in data:
            if width < len(row):
                width = len(row)    

    # Firma Header PNG
    png = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')

    # Chunk: IHDR
    colortype = 0 # Escala de grises
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
    for y in range(height):
        raw += b"\0" # Sin filtro
        for x in range(width):
            c = b"\0" # Pixel negro por defecto
            if y < len(data) and x < len(data[y]):
                c = B1(data[y][x])
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

def imageSource(source):
    data = open(source,"rb").read()

    x = sum(data[18:22])
    y = sum(data[22:26])
    d = sum(data[10:14])
    raw = data[d:] 

    image = [[] for i in range(y)] 
    pad = 0
    if (x * 3 % 4 != 0): 
        pad = 4 - (x * 3 % 4)

    for i in range(y):
        pos = i * (x * 3 + pad)
        for j in range(0, x * 3, 3):
            R = raw[pos + j]
            G = raw[pos + j + 1]
            B = raw[pos + j + 2]
            rgbToGray = (0.2125 * R) + (0.7154 * G) + (0.0721 * B)
            image[i].append(int(rgbToGray))
    
    return image[::-1]

def main():
    if (len(sys.argv) == 1):
        return print('Error: python png.py <archivo.bmp>')

    bitmap_data = imageSource(sys.argv[1])
    png_data = convertToPNG(bitmap_data)

    output = open('output.png','wb')
    output.write(png_data)  
    output.close()

if __name__ == '__main__':
    main()