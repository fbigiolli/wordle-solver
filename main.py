import pyautogui
import cv2
import numpy as np
import pytesseract
from wordle_solver import WordleSolver

def main():

    # Asegurarse de que el wordle este abierto en la ventana a la que se accede al hacer alttab
    pyautogui.hotkey('alt','tab')

    # Screenshot de la pagina y formateo para poder procesarla con cv2
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    # Ajusto los colores de RGB a BGR para que la imagen se visualice correctamente
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Preprocesa, encuentra y guarda las letras encontradas en la imagen.
    preprocessed = preprocess(screenshot)
    letters_cnt = identify_letters(preprocessed)
    letters = []
    
    for letter in letters_cnt:
        x,y,w,h = cv2.boundingRect(letter)
        cropped = screenshot[y:y+h, x:x+w]
        # Encontramos el color asociado a la letra para poder clasificarla segun su estado en el Wordle. 
        color = classify_color(cropped)
        letters.append((cropped, color))

    # Nuevamente aplica threshold y filtros para poder usar pytesseract para identificar las letras.
    

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
    thresh = cv2.threshold(blurred, 200, 255,cv2.THRESH_BINARY_INV)[1]
    return thresh

# Identificar las letras en la imagen ya procesada
def identify_letters(preprocessed):
    contours,_ = cv2.findContours(preprocessed,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    squares_cnt = []
    for contour in contours:
        if is_square(contour):
            squares_cnt.append(contour)
    return squares_cnt

# Decide si el contorno es un cuadrado o no
def is_square(contour):
    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
    if len(approx) == 4:
            _,_,w,h = cv2.boundingRect(contour)
            ratio = float(w)/h
            # Tambien filtro todo aquello que tenga area menor a 100 para que no aparezcan cuadrados sin letras
            if ratio >= 0.9 and ratio <= 1.1 and w*h > 100 :
                return True

    
main()

    # contours,_ = cv2.findContours(preprocessed,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for cnt in contours:
    #     x1,y1 = cnt[0][0]
    #     approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    #     if len(approx) == 4:
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         ratio = float(w)/h
    #         if ratio >= 0.9 and ratio <= 1.1 and w*h > 100:
    #             squares += 1
    #             screenshot = cv2.drawContours(screenshot, [cnt], -1, (0,255,255), 3)
    #             cv2.putText(screenshot, 'Square', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # print(squares)
    # cv2.imshow('img',screenshot)
    # cv2.waitKey(0)