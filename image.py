# Image Structure

# PNG
file = open("test.png","rb")
data = file.read()
for i in range(len(data)):
    print (str(i) + ": " + str(data[i]) )

# # BMP
# file = open("test.bmp","rb")
# data = file.read()
# for i in range(len(data)):
#     if i == 0:
#         print("Tipo de fichero")
#     if i == 2:
#         print("Tamaño del archivo")
#     if i == 6:
#         print("Reservado")
#     if i == 8:
#         print("Reservado")
#     if i == 10:
#         print("Inicio de los datos de la imagen")
#     if i == 14:
#         print("Tamaño de la cabecera del bitmap")
#     if i == 18:
#         print("Anchura (píxels)")
#     if i == 22:
#         print("Altura (píxels)")
#     if i == 26:
#         print("Número de planos")
#     if i == 28:
#         print("Tamaño de cada punto")
#     if i == 30:
#         print("Compresión (0=no comprimido)")
#     if i == 34:
#         print("Tamaño de la imagen")
#     if i == 38:
#         print("Resolución horizontal")
#     if i == 42:
#         print("Resolución vertical")
#     if i == 46:
#         print("Tamaño de la tabla de color")
#     if i == 50:
#         print("Contador de colores importantes")
#     if i == 54:
#         print("DATA")

#     print (str(i) + ": " + str(data[i]))