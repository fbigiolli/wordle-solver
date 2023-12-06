import pyautogui

class Gui_Automation:

    # Es suficientemente declarativo como para explicarlo
    def alt_tab(self):
        pyautogui.hotkey('alt','tab')

    # Tipeamos la palabra seleccionada
    def type_word(self,word):
        pyautogui.write(word,interval = 0.25)

    

