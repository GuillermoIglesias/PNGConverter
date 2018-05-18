# PNG Compressor
import zlib
import binascii

# Abrir archivo imagen source
bitmap = open("test.bmp","rb").read()

# Datos imagen
raw_data = bitmap[sum(bitmap[10:13]):]

# Anchura y altura (pixel)
x = sum(bitmap[18:21])
y = sum(bitmap[22:25])

compressed_data = zlib.compress(raw_data, zlib.Z_BEST_COMPRESSION)

compress_ratio = (float(len(raw_data)) - float(len(compressed_data))) / float(len(raw_data))

print (binascii.hexlify(raw_data))
print (binascii.hexlify(compressed_data))
print ('Compressed: %d%%' % (100.0 * compress_ratio))  

# f = open('output.bmp','wb')
# f.write(compressed_data)  
# f.close()