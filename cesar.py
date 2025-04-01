import sys

def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if 'a' <= caracter <= 'z':  # Solo procesar letras minúsculas
            nuevo_codigo = ((ord(caracter) - ord('a') + desplazamiento) % 26) + ord('a')
            resultado += chr(nuevo_codigo)
        else:
            resultado += caracter  # Mantener caracteres que no sean letras minúsculas
    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py '<texto>' <desplazamiento>")
        sys.exit(1)

    texto = sys.argv[1]
    try:
        desplazamiento = int(sys.argv[2])
    except ValueError:
        print("El desplazamiento debe ser un número entero.")
        sys.exit(1)

    texto_cifrado = cifrado_cesar(texto, desplazamiento)
    print(texto_cifrado)
