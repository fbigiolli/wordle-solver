import cv2
import os
import numpy as np
import pandas as pd
import pyautogui
from image_processing import take_screenshot, preprocess, identify_letters, crop_letters


data_directory = "C:/Users/felub/Documents/Projects/wordle-solver/images"
output_directory = "C:/Users/felub/Documents/Projects/wordle-solver/images"


def create_dataset():
    images, labels = create_dataset_list()

    # Convertir las listas a matrices numpy
    x = np.array(images, dtype=object)
    y = np.array(labels)

    # Crear un DataFrame de pandas
    df = pd.DataFrame(data={'label': y})
    df = pd.concat([df, pd.DataFrame(x)], axis=1)

    # Guardar el DataFrame como un archivo CSV
    csv_filename = "dataset.csv"
    df.to_csv(csv_filename, index=False)


def create_dataset_list():
    # Lista para almacenar las imágenes y etiquetas
    images = []
    labels = []

    # Iterar sobre cada archivo en el directorio
    for filename in os.listdir(data_directory):
        if filename.endswith(".png"):
            image_path = os.path.join(data_directory, filename)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (64, 64))
            img = img.flatten()
            images.append(img)
            # A imread no le gusta la ñ, por eso esto
            if filename[0] == 'ENIE':
                labels.append('Ñ')
            else:
                labels.append(filename[0])

    return images, labels


# Con esta funcion se toma screenshot de la pantalla y guarda en /images las letras que hay en el wordle.
def get_letters():
    pyautogui.hotkey('alt', 'tab')
    # Screenshot de la pagina y formateo para poder procesarla con cv2
    screenshot = take_screenshot()

    # Preprocesa, encuentra y guarda las letras encontradas en la imagen.
    preprocessed = preprocess(screenshot)
    letters_cnt = identify_letters(preprocessed)
    letters = crop_letters(letters_cnt, screenshot)

    i = 0
    for letter in letters:
        output_path = os.path.join(output_directory, f"letra_{i}.png")
        cv2.imwrite(output_path, letter)
        i = i+1