import socket

IP_Servidor = '127.0.0.1'  # IP do servidor (use 127.0.0.1 se for a mesma máquina)
PORTA_Servidor = 5000       # porta usada no servidor

# sock_dgram = usando UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Destino (IP + porta do servidor)
DESTINO = (IP_Servidor, PORTA_Servidor)

# Enviar mensagens em um loop (ou só uma vez)
while True:
    Mensagem = input("Digite uma mensagem (ou 'sair' para encerrar): ")
    if Mensagem.lower() == 'sair':
        print("Encerrando cliente...")
        break
    udp.sendto(bytes(Mensagem, "utf8"), DESTINO)
    print("Mensagem enviada.")
    
udp.close()
