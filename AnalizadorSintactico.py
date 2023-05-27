import graphviz as gv  # Importar la biblioteca graphviz para generar gráficos

class AnalizadorSintactico:
    
    def __init__(self, tokens, derivations) -> None:
        self.tokens = tokens  # Lista de tokens
        self.derivations = derivations  # Diccionario de derivaciones
        self.augmentedStartSymbol = "W'"  # Símbolo inicial aumentado
        self.specialSymbol = "•"  # Símbolo especial
        self.derivations = self.convertDerivationsArrayToDictionary()  # Convertir las derivaciones a un diccionario
        self.automatonTransitions = {}  # Diccionario para almacenar las transiciones del autómata
        print(self.derivations)
    
    def convertDerivationsArrayToDictionary(self):
        derivationsDictionary = {}  # Diccionario para almacenar las derivaciones convertidas
        for derivation in self.derivations:  # Iterar a través de cada derivación en la lista 'derivations'
            derivationRoot = derivation.split(':')[0]  # Obtener la parte izquierda de la derivación (antes de ':')
            derivationBody = derivation.split(':')[1]  # Obtener la parte derecha de la derivación (después de ':')
            if derivationRoot not in derivationsDictionary:  # Si la clave de la derivación no existe en el diccionario
                derivationBody = derivationBody[:-1]  # Eliminar el último carácter (punto y coma)
                derivationBody = derivationBody.strip()  # Eliminar los espacios en blanco alrededor
                derivationsDictionary[derivationRoot] = [derivationBody]  # Agregar la derivación al diccionario
            else:  # Si la clave de la derivación ya existe en el diccionario
                derivationBody = derivationBody[:-1]  # Eliminar el último carácter (punto y coma)
                derivationBody = derivationBody.strip()  # Eliminar los espacios en blanco alrededor
                derivationsDictionary[derivationRoot].append(derivationBody)  # Agregar la derivación al diccionario existente
        derivationsDictionary[self.augmentedStartSymbol] = [self.derivations[0].split(':')[0]]  # Agregar la clave del símbolo inicial aumentado con su derivación correspondiente
        for key in derivationsDictionary:  # Iterar a través de las claves del diccionario
            derivationsDictionary[key] = [x.split() for x in derivationsDictionary[key]]  # Dividir cada derivación en una lista de elementos
        return derivationsDictionary  # Devolver el diccionario de derivaciones convertidas
    
    def goto(self, group, symbol):
        res = []  # Lista para almacenar los resultados
        for item in group:  # Iterar a través de cada elemento en el grupo
            derivationKey, derivationBody = item  # Obtener la clave de la derivación y su cuerpo
            dotIndex = derivationBody.index(self.specialSymbol)  # Encontrar la posición del símbolo especial
            if dotIndex == len(derivationBody) - 1 or dotIndex == -1:  # Si el símbolo especial está al final o no está presente
                continue  # Continuar con el siguiente elemento
            else:
                siguiente = derivationBody[dotIndex + 1]  # Obtener el siguiente símbolo después del símbolo especial
                if siguiente == symbol:  # Si el siguiente símbolo coincide con el símbolo dado
                    newDerivationBody = derivationBody.copy()  # Crear una copia del cuerpo de la derivación
                    newDerivationBody[dotIndex], newDerivationBody[dotIndex + 1] = newDerivationBody[dotIndex + 1], newDerivationBody[dotIndex]  # Intercambiar el símbolo especial con el siguiente símbolo
                    res.append([derivationKey, newDerivationBody])  # Agregar la nueva derivación a los resultados
                    if dotIndex + 2 <= len(newDerivationBody) - 1:  # Si hay un símbolo después del siguiente símbolo
                        nextElementAfterDot = newDerivationBody[dotIndex + 2]  # Obtener el elemento siguiente después del siguiente símbolo
                        if nextElementAfterDot in self.derivations:  # Si el elemento siguiente está en las derivaciones
                            res = self.closure(res)  # Aplicar la clausura a los resultados
        return res  # Devolver los resultados
    
    def closure(self, originalSet):
        newSet = originalSet.copy()  # Copiar el conjunto original
        hasChanged = True  # Variable para controlar si ha habido cambios en el conjunto
        while hasChanged:
            hasChanged = False  # Reiniciar la variable hasChanged
            for item in newSet.copy():  # Iterar a través de cada elemento en el conjunto copiado
                _, prodBody = item  # Obtener el cuerpo de la derivación
                dotIndex = prodBody.index(self.specialSymbol)  # Encontrar la posición del símbolo especial
                if dotIndex == len(prodBody) - 1 or dotIndex == -1:  # Si el símbolo especial está al final o no está presente
                    continue  # Continuar con el siguiente elemento
                nextElement = prodBody[dotIndex + 1]  # Obtener el siguiente elemento después del símbolo especial
                if nextElement in self.derivations:  # Si el siguiente elemento está en las derivaciones
                    productions = self.derivations[nextElement]  # Obtener las producciones correspondientes al siguiente elemento
                    for production in productions:  # Iterar a través de las producciones
                        if self.specialSymbol not in production:  # Si el símbolo especial no está en la producción
                            newProdBody = [self.specialSymbol] + production  # Construir el nuevo cuerpo de la derivación
                            newItem = (nextElement, newProdBody)  # Crear un nuevo elemento de derivación
                            if newItem not in newSet:  # Si el nuevo elemento no está en el conjunto
                                newSet.append(newItem)  # Agregar el nuevo elemento al conjunto
                                hasChanged = True  # Marcar que ha habido cambios en el conjunto
        return newSet  # Devolver el conjunto actualizado
    
    def analizar(self):
        tempArray = self.derivations[self.augmentedStartSymbol][0]  # Obtener el cuerpo de la derivación del símbolo inicial aumentado
        tempArray.insert(0, self.specialSymbol)  # Insertar el símbolo especial al principio del cuerpo de la derivación
        firstSet = self.closure([[self.augmentedStartSymbol, tempArray]])  # Aplicar la clausura al primer conjunto
        Iconjunto = [firstSet]  # Lista para almacenar los conjuntos del autómata
        breakFlag = True  # Variable para controlar el bucle principal
        while breakFlag:
            breakFlag = False  # Reiniciar la variable breakFlag
            for gramatica in Iconjunto.copy():  # Iterar a través de cada gramática en el conjunto de conjuntos
                for elemento in gramatica:  # Iterar a través de cada elemento en la gramática
                    _, derivationBody = elemento  # Obtener el cuerpo de la derivación
                    dotIndex = derivationBody.index(self.specialSymbol)  # Encontrar la posición del símbolo especial
                    if dotIndex == len(derivationBody) - 1 or dotIndex == -1:  # Si el símbolo especial está al final o no está presente
                        pass  # Pasar al siguiente elemento
                    else:
                        siguiente = derivationBody[dotIndex + 1]  # Obtener el siguiente símbolo después del símbolo especial
                        tgoto = self.goto(gramatica, siguiente)  # Calcular el conjunto siguiente mediante la función 'goto'
                        if tgoto not in Iconjunto and tgoto:  # Si el conjunto siguiente no está en el conjunto de conjuntos y no está vacío
                            Iconjunto.append(tgoto)  # Agregar el conjunto siguiente al conjunto de conjuntos
                            self.index = Iconjunto.index(gramatica)  # Obtener el índice del conjunto actual
                            if self.automatonTransitions.get((self.index, siguiente)) == None:  # Si la transición no existe en el autómata
                                self.automatonTransitions[(self.index, siguiente)] = [Iconjunto.index(tgoto)]  # Agregar la transición al autómata
                            else:  # Si la transición ya existe en el autómata
                                self.automatonTransitions[(self.index, siguiente)].append(Iconjunto.index(tgoto))  # Agregar el índice del conjunto siguiente a la transición existente
                            breakFlag = True  # Marcar que ha habido cambios en el bucle principal
                        else:
                            if tgoto:  # Si el conjunto siguiente no está vacío
                                self.index = Iconjunto.index(gramatica)  # Obtener el índice del conjunto actual
                                if self.automatonTransitions.get((self.index, siguiente)) == None:  # Si la transición no existe en el autómata
                                    self.automatonTransitions[(self.index, siguiente)] = [Iconjunto.index(tgoto)]  # Agregar la transición al autómata
                                else:  # Si la transición ya existe en el autómata
                                    if Iconjunto.index(tgoto) not in self.automatonTransitions[(self.index, siguiente)]:  # Si el índice del conjunto siguiente no está en la transición existente
                                        self.automatonTransitions[(self.index, siguiente)].append(Iconjunto.index(tgoto))  # Agregar el índice del conjunto siguiente a la transición existente
                                    
        self.ISET = Iconjunto  # Establecer el conjunto de conjuntos del autómata
        
    def formatAutomatonLR0(self):
        res = {}  # Diccionario para almacenar los nombres de los conjuntos y sus etiquetas
        for i in range(len(self.ISET)):  # Iterar a través de los índices del conjunto de conjuntos
            Iname = f"I{i}"  # Nombre del conjunto
            Ilabel = ""  # Etiqueta del conjunto
            for item in self.ISET[i]:  # Iterar a través de cada elemento en el conjunto
                derivationKey, derivationBody = item  # Obtener la clave de la derivación y el cuerpo de la derivación
                if derivationKey == self.augmentedStartSymbol and derivationBody.index(self.specialSymbol) == len(derivationBody) - 1:  # Si la clave de la derivación es el símbolo inicial aumentado y el símbolo especial está al final
                    Ilabel += f"{derivationKey} : {self.specialSymbol};\n"  # Agregar la línea a la etiqueta del conjunto
                else:
                    if derivationBody.index(self.specialSymbol) == len(derivationBody) - 1:  # Si el símbolo especial está al final
                        Ilabel += f"{derivationKey} : {self.specialSymbol} • ;\n"  # Agregar la línea a la etiqueta del conjunto
                    else:
                        dotIndex = derivationBody.index(self.specialSymbol)  # Encontrar la posición del símbolo especial
                        Ilabel += f"{derivationKey} : {' '.join(derivationBody[:dotIndex])} {self.specialSymbol} {' '.join(derivationBody[dotIndex+1:])} ;\n"  # Agregar la línea a la etiqueta del conjunto
            res[Iname] = Ilabel  # Agregar el nombre del conjunto y su etiqueta al diccionario
        return res  # Devolver el diccionario de nombres de conjuntos y etiquetas
    
    def printISet(self):
        # Imprime los conjuntos I del autómata LR(0)
        for i in range(len(self.ISET)):
            print(f"I{i} = {self.ISET[i]}")

    def graphAutomatonLR0(self):
        # Genera el gráfico del autómata LR(0)
        g = gv.Digraph(format='png')
        values = self.formatAutomatonLR0()
        for key in values:
            # Crea un nodo para cada conjunto I del autómata LR(0)
            g.node(key, label=values[key])
        for key in self.automatonTransitions:
            item, element = key
            for value in self.automatonTransitions[key]:
                # Crea una transición entre dos conjuntos I del autómata LR(0)
                g.edge(f"I{item}", f"I{value}", label=element)
        # Renderiza y muestra el gráfico del autómata LR(0)
        g.render('output/automatonLR0.gv', view=True)
