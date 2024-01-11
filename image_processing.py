import pyautogui
import cv2
import numpy as np
import skimage

def take_screenshot():
    # Screenshot de la pagina y formateo para poder procesarla con cv2
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    # Ajusto los colores de RGB a BGR para que la imagen se visualice correctamente
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot


def crop_letters(letters_cnt, screenshot):
    letters = []
    for letter in letters_cnt:
        x, y, w, h = cv2.boundingRect(letter)
        cropped = screenshot[y:y + h, x:x + w]
        # Nuevamente aplica threshold y filtros para identificar las letras.
        processed = process_cropped(cropped)
        letters.append(processed)
    return letters


def crop_letters_and_classify_color(letters_cnt, screenshot):
    letters = []
    for letter in letters_cnt:
        x, y, w, h = cv2.boundingRect(letter)
        cropped = screenshot[y:y + h, x:x + w]
        # Encontramos el color asociado a la letra para poder clasificarla segun su estado en el Wordle.
        color = classify_color(cropped)
        # Nuevamente aplica threshold y filtros para identificar las letras.
        processed = process_cropped(cropped)
        processed = cv2.resize(processed, (64, 64))
        processed = processed.flatten()
        letters.append((processed, color))
    return letters


def process_cropped(cropped):
    gray_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    imagen_equalizada = cv2.equalizeHist(gray_cropped)
    thresh_cropped = cv2.adaptiveThreshold(imagen_equalizada, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 13)
    bitwise = cv2.bitwise_not(thresh_cropped)
    # cv2.imshow('img',bitwise)
    # cv2.waitKey(0)
    return bitwise


# Clasifica el color segun el average. Los valores de clasificacion estan hardcodeados en base a pruebas manuales
# para observar el valor obtenido segun cada color.
def classify_color(cropped):
    average_color = np.mean(cropped, axis=(0, 1))
    if 100 < average_color[0] < 200 and 100 < average_color[1] < 200 and 100 < average_color[2] < 200:
        color = "Gris"
    elif 40 < average_color[0] < 50 and 170 < average_color[1] < 180 and 225 < average_color[2] < 235:
        color = "Amarillo"
    elif 80 < average_color[0] < 85 and 163 < average_color[1] < 168 and 75 < average_color[2] < 80:
        color = "Verde"
    else:
        color = "Desconocido"
    return color


# Preprocesar la imagen
def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)[1]
    return thresh


# Identificar las letras en la imagen ya procesada
def identify_letters(preprocessed):
    contours, _ = cv2.findContours(preprocessed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    squares_cnt = []
    for contour in contours:
        if is_square(contour):
            squares_cnt.append(contour)
    return squares_cnt


# Decide si el contorno es un cuadrado o no
def is_square(contour):
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
    if len(approx) == 4:
        _, _, w, h = cv2.boundingRect(contour)
        ratio = float(w) / h
        # Tambien filtro todo aquello que tenga area menor a 100 para que no aparezcan cuadrados sin letras
        if 0.9 <= ratio <= 1.1 and w * h > 100:
            return True
