import socket
import datetime

MEU_IP = ''
MINHA_PORTA = 5000
BUFFER_SIZE = 1024

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((MEU_IP, MINHA_PORTA))

print("Servidor rodando e aguardando mensagens...")

clientes = {}

while True:
    Mensagem_Recebida, END_client = udp.recvfrom(BUFFER_SIZE)
    mensagem = Mensagem_Recebida.decode("utf8").strip()

    if mensagem.startswith("hi, meu nome eh "):
        nome_usuario = mensagem[16:]
        clientes[END_client] = nome_usuario
        print(f"{nome_usuario} ({END_client}) entrou na sala.")

        alerta = f"SERVIDOR: {nome_usuario} entrou na sala."
        for cliente in clientes:
            if cliente != END_client:
                udp.sendto(alerta.encode("utf8"), cliente)
        continue

    elif mensagem.lower() == "bye":
        nome_usuario = clientes.pop(END_client, "Usuário desconhecido")
        print(f"{nome_usuario} ({END_client}) saiu da sala.")

        alerta = f"SERVIDOR: {nome_usuario} saiu da sala."
        for cliente in clientes:
            udp.sendto(alerta.encode("utf8"), cliente)
        continue

    horario = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")

    nome_usuario = clientes.get(END_client, "Desconhecido")
    mensagem_formatada = f"{END_client[0]}:{END_client[1]}/~{nome_usuario}: {mensagem} {horario}"
    print(mensagem_formatada)

    for cliente in clientes:
        if cliente != END_client:
            udp.sendto(mensagem_formatada.encode("utf8"), cliente)
