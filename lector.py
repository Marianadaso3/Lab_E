# Esta función lee el contenido de un archivo y lo devuelve como una cadena.

def getContentFromFile(filepath: str):
    try:
        with open(filepath, 'r') as f:
            content = f.read()  # Lee el contenido del archivo y lo guarda en la variable 'content'
        return content
    except FileNotFoundError:
        return False


# Este código toma una cadena que representa una gramática y separa los tokens, derivaciones y comentarios en sus propias listas.
# Lo hace iterando a través de la cadena y agregando el contenido correspondiente a la lista correspondiente.
# También formatea las derivaciones para que sean más fáciles de leer, eliminando espacios adicionales y agregando un punto y coma al final de cada derivación.
def separateContent(content: str):
    tokens = []  # Lista para almacenar los tokens
    derivations = []  # Lista para almacenar las derivaciones
    comments = []  # Lista para almacenar los comentarios
    tempString = ''  # Cadena temporal para construir las derivaciones

    for line in content.split('\n'):  # Iterar a través de cada línea del contenido separado por saltos de línea
        if line.startswith('%token'):  # Si la línea comienza con '%token'
            tokenName = line.split()[1]  # Obtener el nombre del token
            tokens.append(tokenName)  # Agregar el nombre del token a la lista 'tokens'
        elif line.startswith('/*'):  # Si la línea comienza con '/*'
            comments.append(line)  # Agregar la línea a la lista 'comments'
        else:
            if line == ';':  # Si la línea es un punto y coma
                tempString = ' '.join(tempString.split())  # Eliminar espacios adicionales en la cadena temporal
                tempString += ' ;'  # Agregar un punto y coma al final de la cadena temporal
                derivations.append(tempString)  # Agregar la cadena temporal a la lista 'derivations'
                tempString = ''  # Restablecer la cadena temporal
            else:
                tempString += line + ' '  # Agregar la línea a la cadena temporal, seguida de un espacio

    return tokens, derivations, comments  # Devolver las listas 'tokens', 'derivations' y 'comments'
