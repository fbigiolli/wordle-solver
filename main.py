import pyautogui
import time
import pandas as pd
from wordle_solver import WordleSolver
from sklearn.neighbors import KNeighborsClassifier
from dataset_creator import create_dataset_list
from image_processing import take_screenshot, preprocess, identify_letters, crop_letters_and_classify_color


def main():
    # Asegurarse de que el wordle este abierto en la ventana a la que se accede al hacer alttab
    pyautogui.hotkey('alt', 'tab')

    # Tipear la primer palabra
    type_word('AUREO')

    # Crear instancia de wordle solver
    solver = WordleSolver()

    # Loopear hasta encontrar la palabra del dia 
    search_and_type_word_loop(solver)


# Loop que identifica letras, actualiza estado y escribe una palabra candidata.
def search_and_type_word_loop(solver):
    prev_number_of_words_tried = 1
    prev_prediction = 'AUREO'
    
    while(True):
        # Screenshot de la pagina y formateo para poder procesarla con cv2
        screenshot = take_screenshot()

        # Preprocesa, encuentra y guarda las letras encontradas en la imagen.
        preprocessed = preprocess(screenshot)
        letters_cnt = identify_letters(preprocessed)
        letters = crop_letters_and_classify_color(letters_cnt, screenshot)

        # Si no hay una nueva palabra significa que la palabra del wordset era invalida, la agrega a las invalid words.
        if prev_number_of_words_tried == len(letters) / 5:
            solver.add_invalid_word(prev_prediction)
            # Borra la palabra tipeada anteriormente
            for letter in enumerate(letters[-5:]):
                pyautogui.hotkey('backspace')
        else:
            # Si no entra en el if pasado, significa que encontramos una nueva palabra. Aumenta el contador
            prev_number_of_words_tried = prev_number_of_words_tried + 1

        # Si no encontro ninguna letra, no hace falta seguir.
        if len(letters) == 0:
            break

        # Predecir letras
        predictions = (predict_word(letters))
        update_wordle(predictions[-5:], solver)

        # Escribir la palabra
        prev_prediction = solver.search_valid_word()
        type_word(prev_prediction)


# Crea la lista de letras no candidatas y el diccionario de candidatas
def update_wordle(predictions, solver):
    non_candidate_letters = []
    candidate_letters = {}
    result = solver.result

    for i, letter in enumerate(predictions):
        if letter[1] == 'Gris':
            non_candidate_letters.append(letter[0])
        elif letter[1] == 'Amarillo':
            # Si no esta definido
            if not letter[0] in candidate_letters:
                candidate_letters[letter[0]] = [i]
            # Si esta definido
            else:
                candidate_letters[letter[0]] = i
        elif letter[1] == 'Verde':
            result[i] = letter[0]

    solver.update_wordle_status(non_candidate_letters,candidate_letters,result)


# Crea el modelo KNN
def create_knn_model(images, labels):
    knn_model = KNeighborsClassifier(n_neighbors=1)
    knn_model.fit(images, labels)
    return knn_model


# Escribe la palabra y espera
def type_word(word):
    pyautogui.write(word,interval=0.05)
    pyautogui.hotkey('enter')
    # Esperar el tiempo suficiente a que las letras tomen color
    time.sleep(1.3)


# Ya teniendo el modelo KNN, predice las letras
def predict_word(letters):
    # Crear modelo knn para identificar los caracteres
    images, labels = create_dataset_list()
    knn_model = create_knn_model(images, labels)

    res = []
    # Identificar las letras
    for letter in letters:
        current = letter[0].reshape(1,-1)
        res.append((knn_model.predict(current)[0],letter[1]))

    # Darlas vuelta
    res.reverse()

    return res


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