# PNG Compressor
import zlib

# Calcular CRC en cada chunk
def checksum (tag, data):
    checksum = zlib.crc32(tag)
    checksum = zlib.crc32(data, checksum)
    checksum &= 0xFFFFFFFF
    checksum = checksum.to_bytes(4,byteorder='big')
    return checksum

# Abrir archivo imagen source
bitmap = open("input.bmp","rb").read()

# Datos imagen
raw_data = bitmap[sum(bitmap[10:13]):]

# Anchura y altura (pixel)
x = sum(bitmap[18:21])
y = sum(bitmap[22:25])

compressed_data = zlib.compress(raw_data, zlib.Z_BEST_COMPRESSION)
# compress = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED)  
# compressed_data = compress.compress(raw_data)  
# compressed_data += compress.flush()
# compress_ratio = (float(len(raw_data)) - float(len(compressed_data))) / float(len(raw_data))

# print (raw_data)
# print (compressed_data)
# print ('Compressed: %d%%' % (100.0 * compress_ratio))  

# PNG firma de archivo
bmp_file = bytearray([137,80,78,71,13,10,26,10])

# Chunk: IHDR
bmp_file.extend([0,0,0,13]) # Largo Chunk
tag = bytearray([73,72,68,82]) # IHDR
bmp_file.extend(tag) 
chunk_data = bytearray([0,0,0,x,0,0,0,y,8,6,0,0,0]) # Datos 13 bytes.
bmp_file.extend(chunk_data) 
crc = checksum(bytes(tag),bytes(chunk_data)) # CRC
bmp_file.extend([crc[0],crc[1],crc[2],crc[3]]) 

# Chunk: sRGB
bmp_file.extend([0,0,0,1]) # Largo Chunk
tag = bytearray([115,82,71,66]) # sRGB
bmp_file.extend(tag) 
chunk_data = bytearray([0]) # 0: Perceptual
bmp_file.extend(chunk_data) 
crc = checksum(bytes(tag),bytes(chunk_data)) # CRC
bmp_file.extend([crc[0],crc[1],crc[2],crc[3]]) 

# Chunk: gAMA
bmp_file.extend([0,0,0,4]) # Largo Chunk
tag = bytearray([103,65,77,65]) # gAMA
bmp_file.extend(tag) 
chunk_data = bytearray([0,0,177,143]) # 0: Perceptual
bmp_file.extend(chunk_data) 
crc = checksum(bytes(tag),bytes(chunk_data)) # CRC
bmp_file.extend([crc[0],crc[1],crc[2],crc[3]]) 

# Chunk: pHYs
bmp_file.extend([0,0,0,9]) # Largo Chunk
tag = bytearray([112,72,89,115]) # pHYs
bmp_file.extend(tag) 
chunk_data = bytearray([0,0,14,195,0,0,14,195,1]) # Data chunk
bmp_file.extend(chunk_data) 
crc = checksum(bytes(tag),bytes(chunk_data)) # CRC
bmp_file.extend([crc[0],crc[1],crc[2],crc[3]]) 

# Chunk: IDAT
bmp_file.extend([0,0,0,len(compressed_data)]) # Largo Chunk
tag = bytearray([73,68,65,84]) # IDAT
bmp_file.extend(tag) 
chunk_data = compressed_data # Datos imagen comprimida.
bmp_file.extend(chunk_data) 
crc = checksum(bytes(tag),bytes(chunk_data)) # CRC
bmp_file.extend([crc[0],crc[1],crc[2],crc[3]]) 

# Chunk: IEND
bmp_file.extend([0,0,0,0]) # Largo Chunk
tag = bytearray([73,69,78,68]) # IEND
bmp_file.extend(tag) 
chunk_data = bytearray([]) # No datos
bmp_file.extend(chunk_data) 
crc = checksum(bytes(tag),bytes(chunk_data)) # CRC
bmp_file.extend([crc[0],crc[1],crc[2],crc[3]]) 

bmp_file = bytes(bmp_file)

print (bmp_file)

# for i in range(len(bmp_file)):
#     print (bmp_file[i])

f = open('output.png','wb')
f.write(bmp_file)  
f.close()