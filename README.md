# Wordle Solver

## Demo
![demo](https://github.com/fbigiolli/wordle-solver/assets/102247438/5237d8e6-fe78-4fc9-aec5-8d281f31b8b8)

## About
Creé este proyecto como una excusa para aprender sobre machine learning, computer vision, GUI automation y procesamiento de imágenes. Se trata de un programa que resuelve el famoso juego wordle en su [versión en español](https://lapalabradeldia.com/). Para usarlo hay que tener el wordle en la ventana más proxima, de modo que al hacer alt tab quede abierta la ventana, y correr main.py.

## Algoritmo
El approach para resolver el juego es naive: empieza con una palabra predefinida (AUREO), y para encontrar una palabra que sea candidata se busca sobre una lista de palabras de 5 letras teniendo en cuenta la información que da el juego cada vez que se ingresa una palabra. Decidí que este sea el approach porque el objetivo era enfocarme más en la parte de machine learning, y dado que la lista de palabras no tiene un tamaño demasiado grande, el programa no requiere demasiado tiempo para encontrar una palabra candidata.

## Procesamiento de Imágenes y Computer Vision
Para el procesamiento de imagenes y creación del dataset usé las librerias cv2, numpy, os, pyautogui y pandas. Se toma una screenshot de la pantalla, se aplican filtros sobre la imagen y con cv2 se buscan los contornos correspondientes a las letras. Los filtros están ajustados tras varias pruebas, ya que si se aplica un filtrado muy agresivo luego el modelo confunde algunas letras con otras.

## GUI Automation
Usando la libreria pyautogui se toma screenshot de la pantalla, y el programa se encarga de escribir automáticamente cada palabra candidata y recopilar la información que da el juego tras ingresarla. También reconoce si la palabra ingresada no fue válida, caso en el que la borra y deja de tenerla en cuenta para predecir.

## Machine Learning
Para reconocer que letra hay en cada cuadrado del wordle, se usa el modelo K-Nearest Neighbors (KNN). Dado que las letras son siempre iguales, el modelo permite identificar de manera precisa la letra que se muestra en pantalla. Para resolver el wordle no es necesario implementar un modelo como este, ya que sabemos cuáles son las letras que introduce el programa sin necesidad de identificarlas, pero el proyecto en sí era una excusa para aprender sobre machine learning. 
