#Autor: Mariana David

#Importaciones
from LabD.yalex import *  
from lector import getContentFromFile, separateContent  # Importar funciones del módulo FileManager
from utils import formatDerivations  # Importar función del módulo Utils
from AnalizadorSintactico import AnalizadorSintactico  # Importar clase del módulo AnalizadorSintactico



if __name__ == '__main__':  # Comienzo del programa principal
    # Se crea una instancia de la clase Yalex
    #y = Yalex()
    # Se lee un archivo yalex y se carga en la instancia de Yalex
    #y.leerYalex('ArchivosYalex/slr-1.yal')
    content = getContentFromFile('ArchivosYalp/slr-1.yalp')  # Obtener contenido del archivo y guardarlo en la variable content
    tokens, derivations, comments = separateContent(content)  # Separar el contenido en tokens, derivaciones y comentarios
    formattedDerivations = formatDerivations(derivations)  # Formatear las derivaciones
    analizadorSintactico = AnalizadorSintactico(tokens, formattedDerivations)  # Crear una instancia de la clase AnalizadorSintactico
    analizadorSintactico.analizar()  # Realizar análisis sintáctico
    analizadorSintactico.printISet()  # Imprimir información del análisis sintáctico
    analizadorSintactico.graphAutomatonLR0()  # Generar gráfico del autómata LR0

