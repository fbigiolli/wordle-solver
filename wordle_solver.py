
# TODO: CONSIDERAR EL CASO EN EL QUE LA PALABRA DEL DATASET NO ESTA EN EL WORDLE.


class Wordle_Solver:
    # Set de palabras de 5 letras posibles
    wordset = []

    # Lista donde cada posicion corresponde a 1 letra de la palabra. Si no esta en -1 es porque la letra que aparece en la posicion forma parte de la solucion.
    result = ['-1','-1','-1','-1','-1']
    # Lista de letras que son parte de la palabra pero no conozco su posicion
    candidate_letters = []
    # Lista de letras que no son parte de la palabra
    non_candidate_letters = []

    # Constructor de la clase
    def __init__(self):

        #Abrir el archivo con las palabras
        original_txt = open('dataset.txt','r')

        #Leer el archivo con las palabras
        original_txt = original_txt.read()

        #Armar la lista con las palabras
        current_word = ''

        #Recorrer el txt armando la lista
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

            # Una vez que recorrimos todas las letras de temp, si letras disponibles tiene size 0 y se respeta el result original es porque encontramos una palabra candidata.
            if len(temp) == 0 and self.every_position_is_valid(word):
                return word
            
            # Si no se cumple el statement del if, es porque hay letras de las disponibles que no fueron ubicadas, por lo que seguimos buscando. Reiniciamos el valor de temp con las disponibles.
            temp = self.candidate_letters.copy()
    
    # Chequea que cada letra de la palabra sea valida, y por lo tanto sea candidata
    def every_position_is_valid(self,word):
        res = True
        i = 0
        # Chequeo que las letras de la palabra respeten las que ya eran candidatas, y que no haya ninguna que no sea parte de las no candidatas
        while i < 5:
            if not(self.result[i] == '-1' or word[i] == self.result[i]) or word[i] in self.non_candidate_letters :
                res = False
            i = i + 1
        return res
    
    # Actualiza el estado del wordle tras poner una palabra
    def update_wordle_status(self, non_candidate_letters, candidate_letters, result):
        # Agrega aquellas letras nuevas que no estaban en las no candidatas
        for letter in non_candidate_letters:
            if not letter in self.non_candidate_letters:
                self.non_candidate_letters.append(letter)
        
        # Lo mismo para las candidatas
        for letter in candidate_letters:
            if not letter in self.candidate_letters:
                self.candidate_letters.append(letter)
        
        # Actualiza el estado actual del result
        self.result = result
