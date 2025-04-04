import sys
import time
import random
import os
from scapy.all import ICMPv6EchoRequest, ICMPv6EchoReply, IPv6, send, sr1

def enviar_icmpv6_oculto(destino, mensaje_cifrado):
    """
    Envía un mensaje oculto a través de paquetes ICMPv6 e imprime cada envío.

    Args:
        destino (str): La dirección IPv6 del destino.
        mensaje_cifrado (str): El mensaje cifrado que se va a enviar.
    """

    payload_size = 56  # Tamaño estándar del payload (ajustable)

    for i, caracter in enumerate(mensaje_cifrado):
        id_icmpv6 = random.randint(1, 65535)
        secuencia_icmpv6 = random.randint(1, 30000)
        payload_char = bytes(caracter, 'utf-8')
        padding = os.urandom(payload_size - len(payload_char))
        posicion = random.randint(0, payload_size - len(payload_char))
        full_payload = padding[:posicion] + payload_char + padding[posicion:]

        # Alternar entre ICMPv6 Echo Request y Echo Reply
        if random.random() < 0.5:
            paquete = IPv6(dst=destino) / ICMPv6EchoRequest(id=id_icmpv6, seq=secuencia_icmpv6) / full_payload
        else:
            paquete = IPv6(dst=destino) / ICMPv6EchoReply(id=id_icmpv6, seq=secuencia_icmpv6) / full_payload

        send(paquete, verbose=False)
        print(f"Paquete {i + 1} enviado: Carácter '{caracter}'") # Imprime cada envio.
        time.sleep(random.uniform(0.1, 0.5))  # Retardo aleatorio

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 pingipv6.py <IPv6_destino> '<mensaje_cifrado>'")
        sys.exit(1)

    destino = sys.argv[1]
    mensaje_cifrado = sys.argv[2]

    # ICMPv6 de prueba (normal)
    print("ICMPv6 de prueba (normal):")
    respuesta = sr1(IPv6(dst=destino) / ICMPv6EchoRequest(), timeout=1, verbose=False)
    if respuesta:
        print(f"ICMPv6 exitoso: {respuesta.summary()}")
    else:
        print("No se recibió respuesta.")

    enviar_icmpv6_oculto(destino, mensaje_cifrado)

    print("ICMPv6 de prueba (después del envío):")
    respuesta = sr1(IPv6(dst=destino) / ICMPv6EchoRequest(), timeout=1, verbose=False)
    if respuesta:
        print(f"ICMPv6 exitoso: {respuesta.summary()}")
    else:
        print("No se recibió respuesta.")