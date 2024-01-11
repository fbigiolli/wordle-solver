

class WordleSolver:
    # Set de palabras de 5 letras posibles
    wordset = []
    # Lista donde cada posicion corresponde a 1 letra de la palabra. Si no esta en -1 es porque la letra que aparece en la posicion forma parte de la solucion.
    result = ['-1','-1','-1','-1','-1']
    # Lista de letras que son parte de la palabra pero no conozco su posicion
    candidate_letters = []
    # Lista de letras que no son parte de la palabra
    non_candidate_letters = []
    # Lista de palabras que no son validas en el wordle
    invalid_words = []
    # Lista de listas, en la que cada posicion del 0 al 4 tiene una lista de aquellas letras que NO pueden ir en esa posicion.
    banned_letters_in_index = [[],[],[],[],[]]

    # Constructor de la clase
    def __init__(self):

        #Abrir el archivo con las palabras
        original_txt = open('wordset.txt','r')

        #Leer el archivo con las palabras
        original_txt = original_txt.read()

        #Armar la lista con las palabras
        current_word = ''

        for letra in original_txt:
            #Si es un espacio lo agrego a la lista y sigo
            if letra == ' ':
                self.wordset.append(current_word)
                current_word = ''
                continue
            
            #Si no, le agrego al final de current_word la letra actual
            current_word = current_word + letra

    # Busca una palabra candidata en el estado actual del wordle
    def search_valid_word(self):
        # Buscamos en el wordset alguna palabra que sea factible sabiendo esto.
        temp = self.candidate_letters.copy()
        for word in self.wordset:
            i = 0
            # Chequeamos que esten todas las letras disponibles que encontramos
            while i < 5:
                # Si la letra de la palabra fue encontrada en las disponibles, y esa posicion no estaba ya marcada como correcta en la solucion la borramos de temp
                if (word[i] in temp) and self.result[i] == '-1':
                    temp.remove(word[i])
                i = i+1

            # Una vez que recorrimos todas las letras de temp, si letras disponibles tiene size 0 y se respeta el result original es porque encontramos una palabra candidata. Ademas nos fijamos que no este en invalid_words
            if len(temp) == 0 and self.every_position_is_valid(word) and not word in self.invalid_words:
                return word
            
            # Si no se cumple el statement del if, es porque hay letras de las disponibles que no fueron ubicadas, por lo que seguimos buscando. Reiniciamos el valor de temp con las disponibles.
            temp = self.candidate_letters.copy()
    
    # Chequea que cada letra de la palabra sea valida, y por lo tanto sea candidata
    def every_position_is_valid(self,word:str) -> bool:
        res = True
        i = 0
        # Chequeo que las letras de la palabra respeten las que ya eran candidatas, y que no haya ninguna que no sea parte de las no candidatas
        while i < 5:
            if not(self.result[i] == '-1' or word[i] == self.result[i]) or (word[i] in self.non_candidate_letters and self.result[i] == '-1') or word[i] in self.banned_letters_in_index[i]:
                res = False
            i = i + 1
        return res
    
    # Actualiza el estado del wordle tras poner una palabra
    # candidate_letters dictionary donde las keys son las letras, y el significado una lista de posiciones donde no puede ir.
    def update_wordle_status(self, non_candidate_letters:list, candidate_letters:dict, result:list):
        # Agrega aquellas letras nuevas que no estaban en las no candidatas
        for letter in non_candidate_letters:
            if not letter in self.non_candidate_letters:
                self.non_candidate_letters.append(letter)
        
        # Lo mismo para las candidatas
        for letter in candidate_letters.keys():
            if not letter in self.candidate_letters:
                self.candidate_letters.append(letter)
            
            # Ademas, actualizamos las posiciones en las que NO pueden ir las candidatas.
            for position in candidate_letters[letter]:
                if not letter in self.banned_letters_in_index[position]:
                    self.banned_letters_in_index[position].append(letter)

        # Si alguna de las candidatas encontro su posicion correcta, la sacamos de las candidatas
        for letter in result:
            if letter in self.candidate_letters:
                self.candidate_letters.remove(letter)

        # Actualiza el estado actual del result
        self.result = result

    def add_invalid_word(self,word:str):
        self.invalid_words.append(word)

    # Spoiler, no hay
    def search_word_with_w(self):
        for word in self.wordset:
            for letter in word:
                if letter == 'W':
                    return word


# sample test
# new = Wordle_Solver()
# new.update_wordle_status(['U','R','E'],{"A":[0],"O":[4]},['-1','-1','-1','-1','-1',])
# print(new.search_valid_word())
# new.update_wordle_status(['B','C','N'],{"A":[1],"O":[3]},['-1','-1','-1','-1','-1',])
# print(new.search_valid_word())
# new.update_wordle_status(['D','S'],{"I":[1],"O":[2]},['-1','-1','-1','-1','A',])
# print(new.search_valid_word())
# new.update_wordle_status(['F','L'],{},['-1','O','-1','I','A',])
# print(new.search_valid_word())
# new.update_wordle_status(['G'],{},['-1','O','M','I','A',])
# print(new.search_valid_word())
        
