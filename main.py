import pyautogui
import cv2
import numpy as np

from wordle_solver import Wordle_Solver

def main():

    # Asegurarse de que el wordle este abierto en la ventana a la que se accede al hacer alttab
    pyautogui.hotkey('alt','tab')

    # Screenshot de la pagina, y formateo para poder procesarla con cv2
    screenshot = pyautogui.screenshot()
    # Cambio el formato a uno que pueda ser manejado por cv2
    screenshot = np.array(screenshot)
    # Ajusto los colores de RGB a BGR para que la imagen se visualice correctamente
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Preprocesar
    preprocessed = preprocess(screenshot)

    # Encontrar cada letra
    letters = identify_letters(preprocessed)



# Preprocesar la imagen
def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 200, 255,cv2.THRESH_BINARY_INV)[1]
    return thresh

# Identificar las letras en la imagen ya procesada
def identify_letters(preprocessed):
    contours,_ = cv2.findContours(preprocessed,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    squares = []
    for contour in contours:
        if is_square(contour):
            squares.append(contour)
    return squares

# Decide si el contorno es un cuadrado o no
def is_square(contour):
    x1,y1 = contour[0][0]
    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
    if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            ratio = float(w)/h
            # Tambien filtro todo aquello que tenga area menor a 100 para que no aparezcan cuadrados sin letras
            if ratio >= 0.9 and ratio <= 1.1 and w*h > 100 :
                return True

# Tipeamos la palabra seleccionada
def type_word(word):
    pyautogui.write(word,interval = 0.25)

    
