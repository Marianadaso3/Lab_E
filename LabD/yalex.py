
class Yalex:
    def __init__(self):
        self.specialtoks = [] # Lista que guarda los nombres de los estados ficticios creados
        self.infix = '' # Expresión regular en formato infix
        self.kleenCer = '♣'  # Simbolo utilizado para la cerradura de kleen
        self.tokens = {}    # Diccionario que guarda el nombre del identificador y su expresion regular

    #Funcion basada en el algoritmo de shunting-yard
    def shunting(self, regex): #regex-value
        # Si el regex no es una clase de caracteres, reemplaza la expresión "[+'-']" por "('+'|'-')"
        if regex[0] != '[': #al primer carácter del regex
            return regex.replace("['+''-']", "('+'|'-')")

        # Si el regex es una clase de caracteres con comillas simples ('), procesa los rangos y los convierte en una
        # expresión regular con la sintaxis correcta. Por ejemplo, '[a-z]' se convierte en '(a|b|c|...|z)'
        string = regex[2:-2] # esta línea elimina los corchetes iniciales y finales de la expresión regular contenida en regex= ''['//s''//t''//n']''-->
        #regex= ''['//s''//t''//n']''--> ' '//s' '//t' '//n' '
        if regex[1] == "'": # se verifica si el segundo carácter de regex es una comilla simple (') para determinar si se trata de una clase de caracteres delimitada por comillas simples o no.
            groups = string.split("''")  # Separa los grupos delimitados por comillas simples (') = ['\\s', '\\t', '\\n']
            resultado = '' #se inicializa una cadena de caracteres vacía que se usará para ir construyendo la expresión regular final
            for group in groups:
                if "-" in group:  # verifica si el elemento "group" contiene un guion, lo que indica que es un rango de caracteres.
                    # Genera la cadena de caracteres correspondiente al rango
                    group = '°'.join([ # Se comienza a utilizar el simbolo ° como operador or, para evitar confuciones en la gramatica por si viene algun |
                        chr(i)
                        for i in range(ord(group[0]), ord(group[-1]) + 1)
                    ])
                resultado += "°" + group #resultado = '|\\s |\\t |\\n '
            return "˂" + resultado[1:] + "˃" #le quito el | y lo regreso estructura #resultado = '(\\s |\\t |\\n) '

        # verifica si el primer caracter regex es una clase de caracteres con comillas dobles ("), procesa los escapes de caracteres
        if regex[1] == '"':
            chars = list(string)  # Convierte la cadena de caracteres en una lista
            stack = []  # Pila para procesar los escapes
            i = 0
            while len(chars) > 0: #se ejecuta mientras tenga elementos 
                char = chars.pop(0) # En cada iteración del bucle, se saca el primer elemento de la lista chars y se asigna a la variable char
                if char == '\\':  # Si el caracter es un esc
                    stack.append(char + chars.pop(0))  # Agrega el escape y el siguiente caracter a la pila
                    
                else:
                    stack.append(char)  # Si no es un escape, agrega el caracter directamente
                #i += 1
    
            # Une todos los elementos de la pila con el operador "|" y los encierra en paréntesis
            return f"˂{'°'.join(stack)}˃"

    def leerYalex(self, file, banderaSpecialtok=False):
            rule = False  # Indica si se está procesando una regla de producción
            vars = {}  # Diccionario que almacena las variables definidas en el archivo YALex
            infix = ''  # Expresión regular en notación infix para las reglas de producción definidas en el archivo YALex
            n_line = 2  # Número de línea actual (se inicia en 2 debido a que la primera línea se omite)

            with open(file) as yal:
                for line in yal:
                    if len(line) > 1:  # Ignora las líneas vacías
                        try:
                            tokens = line.split()  # Separa la línea en tokens
                            if not tokens[0] == "(*":  # Ignora los comentarios
                                if tokens[0] == 'let':  # Si la línea define una variable
                                    value = tokens[3]  # Obtiene el valor de la variable
                                    for var in vars.keys():
                                       #print ("VER EL KEY: " + var)
                                        #print ("PRUEBA" + vars[var])
                                        value = value.replace(var, vars[var])  # Reemplaza las variables por sus valores
                                        #print ("DEPUES DE REPLACE"+ value)
                                    value = self.shunting(value)  # shuntinge la variable en una expresión regular
                                    value = value.replace("(","˂").replace(")","˃")     #Para evitar confuciones con los mismos tokens de la gramatica se cambian los parentesis por pico parentesis
                                    vars[tokens[1]] = value  # Agrega la variable al diccionario
                                if tokens[0] == 'rule':  # Si la línea define una regla de producción
                                    rule = True  # Indica que se está procesando una regla de producción
                                    continue
                                if rule:  # Si se está procesando una regla de producción
                                    pos = not tokens[0] == '|'
                                    #el token esta en la pos 0 o 1 
                                    token = tokens[0] if pos else tokens[1]  # Obtiene el token y su posición en la regla de producción
                                    #el specialt "nombre de la regla"
                                    especialt = tokens[3] if pos else tokens[4]  # Obtiene el token especialt y su posición en la regla de producción
                                    self.specialtoks.append(especialt)  # Agrega el token especialt a la lista de tokens specialtoks    
                                    if banderaSpecialtok: #TRUE = Agarra lit la palabra como token y remplaza por el simbolo (si o no hago la conversion)
                                        especialt = self.kleenCer  # Reemplaza el token especialt por un marcador de posición
                                    if token in vars.keys():  # Si el token es una variable
                                        special_token = '((' + vars[token] + ')' + especialt + ')'# Crea un token especialt para la variable
                                        self.tokens[especialt] = { "expresion": vars[token].replace("'", "").replace("˃*", "˃"+self.kleenCer).replace("|", "°").replace("˃?", "˃☺").replace("˃+", "˃♦").replace("9˃s", "9˃♦")} #cambiar a ♦ que es +
                                    else:
                                        special_token = '|((' + token + ')' + especialt + ')' # Crea un token especialt para el token
                                        self.tokens[especialt] = { "expresion": token.replace("'", "").replace("˃*", "˃"+self.kleenCer).replace("|", "°").replace("˃?", "˃☺").replace("˃+", "˃♦").replace("9˃s", "9˃♦").replace('"', '')} #cambiar a ♦ que es +
                                    infix += special_token  # Agrega el token especialt a la expresión regular en notación infix
                        except:
                            print("ERROR en la linea " + str(n_line))# Imprime un mensaje de error si ocurre un error de sintaxis
                    n_line += 1
                    
                self.infix = infix[1:].replace("9)s", "9)+")# Crea la expresión regular final y la almacena en la propiedad infix - A PARTRI DEL INDICE 1 PORQUE TIENE  | 