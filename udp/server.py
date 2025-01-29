import socket

MEU_IP = ''  # ouvirá em todas as interfaces
MINHA_PORTA = 5000  # porta escolhida para comunicação

# sock_dgram = usando UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Faz o bind do IP e a porta
MEU_SERVIDOR = (MEU_IP, MINHA_PORTA)
udp.bind(MEU_SERVIDOR)

print("Servidor rodando e aguardando mensagens...")

# Loop para manter o servidor ativo
while True:
    Mensagem_Recebida, END_client = udp.recvfrom(1024)
    print("Recebi =", Mensagem_Recebida.decode("utf8"), ", Do cliente", END_client)
    