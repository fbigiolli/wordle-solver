
#Abrir el archivo con las palabras
original_txt = open('dataset.txt','r')

#Leer el archivo con las palabras
original_txt = original_txt.read()

#Armar la lista con las palabras
list = []
current_word = ''

#Recorrer el txt armando la lista
for letra in original_txt:
    #Si es un espacio lo agrego a la lista y sigo
    if letra == ' ':
        list.append(current_word)
        current_word = ''
        continue
        
    #Si no, le agrego al final de current_word la letra actual
    current_word = current_word + letra

for elem in list:
    print(elem)