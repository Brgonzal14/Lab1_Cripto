# descifrar_cesar_v2.py

import sys

# Códigos de escape ANSI para colores en la terminal
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

def descifrado_cesar(texto_cifrado, desplazamiento):
    """
    Descifra un texto cifrado con el algoritmo César.
    Solo procesa letras minúsculas del alfabeto inglés (a-z).
    """
    resultado = ""
    for caracter in texto_cifrado:
        if 'a' <= caracter <= 'z':  # Solo procesar letras minúsculas
            # Calcula el código del carácter descifrado
            nuevo_codigo = ((ord(caracter) - ord('a') - desplazamiento + 26) % 26) + ord('a')
            resultado += chr(nuevo_codigo)
        else:
            resultado += caracter  # Mantener caracteres que no sean letras minúsculas
    return resultado

def es_mensaje_probable(texto):
    """
    Heurística MÁS ESTRICTA para determinar si un texto descifrado es probable.
    Busca palabras comunes en español rodeadas de espacios. Requiere al menos
    una palabra común Y una frecuencia razonable de espacios si es largo.
    """
    # Palabras comunes cortas y relevantes en español (añade más si es necesario)
    palabras_comunes = [
        " y ", " en ", " de ", " la ", " el ", " que ", " con ", " por ",
        " red ", " redes ", " seguridad ", " mensaje ", " texto ", " hola ",
        " mundo ", " los ", " las ", " para ", " sin "
        ]
    texto_lower = texto.lower() # Comprobar en minúsculas
    palabras_encontradas = 0

    # Comprobación 1: Contar palabras comunes encontradas
    for palabra in palabras_comunes:
        if palabra in texto_lower:
            palabras_encontradas += 1

    # Si no encontramos ninguna palabra común, es improbable
    if palabras_encontradas == 0:
        return False

    # Si encontramos al menos una, aplicamos un filtro adicional de espacios
    # para textos más largos, para evitar falsos positivos con palabras cortas
    # en textos sin sentido.
    if len(texto) > 15:
        frecuencia_espacios = texto.count(' ') / len(texto)
        # Requiere al menos una palabra común Y una frecuencia de espacios > 8%
        if frecuencia_espacios > 0.08:
            return True
        else:
            # Si es largo pero casi no tiene espacios, aunque tenga una palabra común,
            # lo marcamos como improbable.
            return False
    else:
        # Si es corto y tiene al menos una palabra común, lo consideramos probable.
        return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 descifrar_cesar_v2.py '<texto_cifrado>'")
        print("Asegúrate de poner el texto cifrado entre comillas si contiene espacios.")
        sys.exit(1)

    texto_cifrado = sys.argv[1]

    print(f"Texto cifrado ingresado: {texto_cifrado}\n")
    print("Probando posibles desplazamientos (0-29):")

    encontrado_probable = False
    # Probar todos los desplazamientos del 0 al 29
    for desplazamiento in range(30):
        desplazamiento_efectivo = desplazamiento % 26
        texto_descifrado = descifrado_cesar(texto_cifrado, desplazamiento_efectivo)

        es_probable = es_mensaje_probable(texto_descifrado)

        prefijo = f"{desplazamiento:02d}: "
        if es_probable:
            print(f"{COLOR_GREEN}{prefijo}{texto_descifrado}{COLOR_RESET}")
            encontrado_probable = True
        else:
            print(f"{prefijo}{texto_descifrado}")

    if not encontrado_probable:
         print("\nAdvertencia: No se pudo identificar automáticamente un mensaje probable usando la heurística.")