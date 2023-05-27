#FUNCION NUEVA PARA EL E para el formato de las derivaciones
def formatDerivations(derivations):
    formattedDerivationsArray = []  # Lista para almacenar las derivaciones formateadas

    for derivation in derivations:  # Iterar a través de cada derivación en la lista 'derivations'
        derivationRoot = derivation.split(':')[0]  # Obtener la parte izquierda de la derivación (antes de ':')
        derivationBody = derivation.split(':')[1]  # Obtener la parte derecha de la derivación (después de ':')
        derivationBody = derivationBody.split('|')  # Dividir la parte derecha en subderivaciones separadas por '|'

        for subderivation in derivationBody:  # Iterar a través de cada subderivación en la lista 'derivationBody'
            if ";" not in subderivation:  # Si no hay un punto y coma al final de la subderivación
                subderivation += ';'  # Agregar un punto y coma al final de la subderivación
            formattedDerivation = derivationRoot + ':' + subderivation  # Construir la derivación formateada
            formattedDerivationsArray.append(formattedDerivation)  # Agregar la derivación formateada a la lista 'formattedDerivationsArray'

    return formattedDerivationsArray  # Devolver la lista 'formattedDerivationsArray'

#-----------------------------------------------------------
#SOLO ME ENCARGO DE TRANFORMAR Y CONCATENAR CORRECTAMENTE
# Transforma la expresión regular que tenga cerradura positiva a su expansión con cerradura de Kleene
def trans_positive(cadena):
    partes = cadena.split("♦")  # Dividir la cadena en partes utilizando "♦" como separador
    print(partes)
    resultado = ""
    idx = 0
    for parte in partes:
        to_exp = ""
        if "˃" in parte and idx != len(partes)-1:
            # Verificar si la parte contiene el símbolo "˃" y no es la última parte
            print(len(partes), idx)
            print(parte)
            indice_primer_derecho = parte.rindex("˃")
            # Obtener el índice de la última aparición del símbolo "˃" en la parte actual
            i = indice_primer_derecho
            substr = ""
            idx = idx + 1
            while i >= 0:
                # Construir una subcadena que comienza desde la última aparición de "˃" hacia la izquierda
                substr = parte[i] + substr
                i = i - 1
                num_izquierdos = substr.count("˂")  # Contar la cantidad de "˂" en la parte actual
                num_derechos = substr.count("˃")
                if num_derechos == num_izquierdos:
                    # Si el número de "˂" es igual al número de "˃", se ha encontrado la subcadena completa
                    to_exp = substr + "♣"  # Agregar el símbolo "♣" al final de la subcadena
                    break

        last_index = parte.rfind(to_exp.replace("♣", ""))
        # Obtener el índice de la última aparición de la subcadena sin el símbolo "♣"
        if last_index != -1:
            # Si se encontró la subcadena en la parte actual
            partediff = parte[:last_index] + parte[last_index:].replace(to_exp.replace("♣", ""), "", 1)
            # Reemplazar la primera aparición de la subcadena por una cadena vacía
        else:
            partediff = ""
            # Si no se encontró la subcadena en la parte actual, se asigna una cadena vacía

        toadd = partediff + to_exp.replace("♣", "") + to_exp
        # Construir la parte modificada agregando la subcadena y su expansión con cerradura de Kleene
        resultado = resultado + toadd
        # Concatenar la parte modificada al resultado final
    print(resultado)
    return resultado
    # Retornar el resultado final

# Toma la expresión regular inicial y la transforma al expandir el símbolo "?"
def transform_exp(regular_exp):
    while "˃☺" in regular_exp:
        # Repetir el proceso mientras la expresión regular contenga "˃☺"
        base = []
        i = 0
        starting = []

        while i < len(regular_exp) - 1:
            # Recorrer la expresión regular
            if regular_exp[i] == "˂":
                # Si se encuentra el símbolo "˂", se guarda su posición en una lista
                starting.append(i)
            
            if regular_exp[i] == "˃":
                # Si se encuentra el símbolo "˃"
                base.append(regular_exp[i])
                if regular_exp[i+1] == "☺":
                    # Si el siguiente símbolo es "☺", se realiza la expansión para "?"
                    base.append("°")
                    base.append("ε")
                    base.append("˃")
                    base.insert(starting[-1], "˂")  # Se inserta el símbolo "˂" en la posición guardada previamente
                    i += 1
                    break
                else:
                    starting.pop()  # Si no se cumple la condición anterior, se elimina la posición guardada
            else:
                base.append(regular_exp[i])
            i += 1

        regular_exp = "".join(base) + regular_exp[i + 1:]
        # Se reconstruye la expresión regular con la base y el resto de la expresión original

    if "☺" in regular_exp:
        # Si aún quedan símbolos "?" en la expresión regular
        while "☺" in regular_exp:
            i = regular_exp.find("☺")
            symbol = regular_exp[i - 1]
            # Se encuentra el símbolo anterior al "?"
            regular_exp = regular_exp.replace(symbol + "☺", "˂" + symbol + "°ε˃")
            # Se reemplaza el símbolo anterior y el "?" por su expansión correspondiente

    if regular_exp.count("˂") > regular_exp.count("˃"):
        # Si hay más símbolos "˂" que "˃" en la expresión regular
        for i in range(regular_exp.count("˂") - regular_exp.count("˃")):
            regular_exp += "˃"  # Se agrega la cantidad faltante de símbolos "˃" al final de la expresión

    elif regular_exp.count("˂") < regular_exp.count("˃"):
        # Si hay más símbolos "˃" que "˂" en la expresión regular
        for i in range(regular_exp.count("˃") - regular_exp.count("˂")):
            regular_exp = "˂" + regular_exp  # Se agrega la cantidad faltante de símbolos "˂" al inicio de la expresión

    return regular_exp
    # Se retorna la expresión regular transformada

# Añade la concatenación explícita, esto se hace para facilitar la lectura de algunos operadores
def add_concat(expresion):
    modified = ""
    operators = ["♣","°","˂"]  # Operadores: cerradura de Kleene, alternancia o unión, concatenación
    idx = 0
    while idx < len(expresion):
        # Recorrer la expresión regular

        if expresion[idx] == "♣" and not ((expresion[idx+1] in operators) or expresion[idx+1] == "˃"):
            # Si se encuentra el símbolo de cerradura de Kleene y el siguiente símbolo no es un operador o el símbolo "˃"
            modified += expresion[idx]+"►"
        elif expresion[idx] == '♣' and expresion[idx+1] == '˂':
            # Si se encuentra el símbolo de cerradura de Kleene y el siguiente símbolo es "˂"
            modified += expresion[idx]+"►"
        elif not (expresion[idx] in operators) and expresion[idx+1] == "˃":
            # Si el símbolo actual no es un operador y el siguiente símbolo es "˃"
            modified += expresion[idx]
        elif (not (expresion[idx] in operators) and not (expresion[idx+1] in operators)) or (not (expresion[idx] in operators) and (expresion[idx+1] == "˂")):
            # Si el símbolo actual no es un operador y el siguiente símbolo no es un operador o es "˂"
            modified += expresion[idx]+"►"
        else:
            modified += expresion[idx]
    
        idx += 1

        if idx+1 >= len(expresion):
            modified += expresion[-1]  # Añadir el último símbolo de la expresión
            break
        
    return modified
    # Se retorna la expresión modificada con la concatenación explícita
