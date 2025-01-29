import socket

IP_Servidor = '127.0.0.1'  
PORTA_Servidor = 5000
BUFFER_SIZE = 1024

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.connect((IP_Servidor, PORTA_Servidor))

nome_usuario = input("Digite seu nome: ")
udp.sendto(f"hi, meu nome eh {nome_usuario}".encode("utf8"), (IP_Servidor, PORTA_Servidor))

print("Conectado ao chat. Digite suas mensagens (ou 'bye' para sair):")

while True:
    mensagem = input()

    if mensagem.lower() == "bye":
        udp.sendto("bye".encode("utf8"), (IP_Servidor, PORTA_Servidor))
        print("Saindo do chat...")
        break

    udp.sendto(mensagem.encode("utf8"), (IP_Servidor, PORTA_Servidor))

    try:
        udp.settimeout(1)  # Define um tempo limite para evitar bloqueios
        while True:
            resposta, _ = udp.recvfrom(BUFFER_SIZE)
            print(resposta.decode("utf8"))
    except socket.timeout:
        pass

udp.close()
