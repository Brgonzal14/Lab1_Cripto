import sys
import time
from scapy.all import ICMP, IP, send, sr1

def enviar_ping(destino, mensaje_cifrado):
    print(f"Enviando mensaje oculto a {destino}...")

    # Enviar un paquete por cada carácter del mensaje cifrado
    for i, caracter in enumerate(mensaje_cifrado, start=1):
        paquete = IP(dst=destino) / ICMP() / caracter
        send(paquete, verbose=False)  # Enviar el paquete
        print(f"Sent {i} packets.")  # Imprimir cada vez que se envía un paquete
        time.sleep(0.2)  # Introducir una pequeña pausa entre envíos

    print("Todos los paquetes han sido enviados.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 ping.py <IP_destino> '<mensaje_cifrado>'")
        sys.exit(1)

    destino = sys.argv[1]
    mensaje_cifrado = sys.argv[2]

    # Enviar un ping de prueba normal para comparar
    print("Ping de prueba (normal):")
    respuesta = sr1(IP(dst=destino) / ICMP(), timeout=1, verbose=False)
    if respuesta:
        print(f"Ping exitoso: {respuesta.summary()}")
    else:
        print("No se recibió respuesta.")

    # Enviar el mensaje cifrado en pings
    enviar_ping(destino, mensaje_cifrado)

    # Enviar otro ping normal para verificar que el tráfico sigue igual
    print("Ping de prueba (después del envío):")
    respuesta = sr1(IP(dst=destino) / ICMP(), timeout=1, verbose=False)
    if respuesta:
        print(f"Ping exitoso: {respuesta.summary()}")
    else:
        print("No se recibió respuesta.")
