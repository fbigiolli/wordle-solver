import pyautogui
from wordle_solver import Wordle_Solver

def main():
    new = Wordle_Solver()
    result = ['-1','U','R','-1','-1']
    non_candidate_words = ['A','E','O','B','L']
    new.update_wordle_status(non_candidate_words,['I'],result)
    print(new.search_valid_word())

    # # Asegurarse de que el wordle este abierto en la ventana a la que se accede al hacer alttab
    # alt_tab()

    # # Screenshot de la pagina y encontrar el wordle
    # screenshot = pyautogui.screenshot()



# Es suficientemente declarativo como para explicarlo
def alt_tab(self):
    pyautogui.hotkey('alt','tab')

# Tipeamos la palabra seleccionada
def type_word(self,word):
    pyautogui.write(word,interval = 0.25)

    

main()