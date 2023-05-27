#falta implementacion de la clase principal
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
    
