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
    Heurística para determinar si un texto descifrado es probable.
    Busca palabras comunes en español. Requiere al menos una palabra común
    Y una frecuencia razonable de espacios si es largo.
    """
    # Palabras comunes cortas y relevantes en español (SIN espacios alrededor)
    palabras_comunes_lista = [
        "y", "en", "de", "la", "el", "que", "con", "por",
        "red", "redes", "seguridad", "mensaje", "texto", "hola",
        "mundo", "los", "las", "para", "sin", "criptografia" # Añadido criptografia por el ejemplo
    ]
    # Convertir a set para búsqueda más eficiente
    palabras_comunes_set = set(palabras_comunes_lista)

    # Dividir el texto en palabras (ignorando mayúsculas/minúsculas)
    # y eliminar posibles cadenas vacías resultantes de múltiples espacios
    palabras_en_texto = [palabra for palabra in texto.lower().split(' ') if palabra]

    palabras_encontradas = 0

    # Comprobación 1: Contar palabras comunes encontradas
    for palabra_texto in palabras_en_texto:
        # Eliminar posible puntuación simple al final (opcional, pero útil)
        palabra_limpia = palabra_texto.strip('.,;:!?')
        if palabra_limpia in palabras_comunes_set:
            palabras_encontradas += 1
            # Si ya encontramos una, podemos salir del bucle si solo nos importa si hay >= 1
            # break # Descomentar si solo necesitas saber si hay al menos una

    # Si no encontramos ninguna palabra común, es improbable
    if palabras_encontradas == 0:
        return False

    # --- El resto de la lógica se mantiene igual ---

    # Si encontramos al menos una, aplicamos un filtro adicional de espacios
    # para textos más largos, para evitar falsos positivos con palabras cortas
    # en textos sin sentido.
    if len(texto) > 15:
        # Evitar división por cero si el texto no tiene longitud
        if len(texto) == 0:
            return False # O manejar como prefieras un texto vacío
        frecuencia_espacios = texto.count(' ') / len(texto)
        # Requiere al menos una palabra común Y una frecuencia de espacios > 8%
        # Ajusta este umbral si es necesario
        if frecuencia_espacios > 0.08:
            return True
        else:
            # Si es largo pero casi no tiene espacios, aunque tenga una palabra común,
            # lo marcamos como improbable.
            return False
    else:
        # Si es corto (<15) y tiene al menos una palabra común, lo consideramos probable.
        return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 descifrar_cesar_v2.py '<texto_cifrado>'")
        print("Asegúrate de poner el texto cifrado entre comillas si contiene espacios.")
        sys.exit(1)

    texto_cifrado = sys.argv[1]

    # Convertir a minúsculas ANTES de procesar para que coincida con el descifrador
    texto_cifrado_lower = texto_cifrado.lower()

    print(f"Texto cifrado ingresado: {texto_cifrado}\n")
    print("Probando posibles desplazamientos (0-29):")

    encontrado_probable = False
    # Probar todos los desplazamientos del 0 al 29
    for desplazamiento in range(30): # El rango 30 es innecesario, bastaría 26, pero no daña
        desplazamiento_efectivo = desplazamiento % 26
        # Usar la versión en minúsculas para descifrar
        texto_descifrado = descifrado_cesar(texto_cifrado_lower, desplazamiento_efectivo)

        es_probable = es_mensaje_probable(texto_descifrado)

        prefijo = f"{desplazamiento:02d}: "
        if es_probable:
            print(f"{COLOR_GREEN}{prefijo}{texto_descifrado}{COLOR_RESET}")
            encontrado_probable = True
        else:
            print(f"{prefijo}{texto_descifrado}")

    if not encontrado_probable:
         print("\nAdvertencia: No se pudo identificar automáticamente un mensaje probable usando la heurística.")
