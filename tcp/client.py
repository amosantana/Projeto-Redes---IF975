import socket
import hashlib
import time

# Configuração do servidor
IP_SERVIDOR = '127.0.0.1'
PORTA_SERVIDOR = 5000
BUFFER_SIZE = 1024
TIMEOUT = 2  # Tempo de espera pelo ACK (segundos)

# Função para calcular o checksum
def calcular_checksum(mensagem):
    return hashlib.md5(mensagem.encode()).hexdigest()

# Função para enviar mensagens de forma confiável com RDT 3.0
def enviar_mensagem(udp, mensagem, endereco):
    seq_num = 0  # Alterna entre 0 e 1 para controle
    while True:
        # Criar pacote com número de sequência e checksum
        checksum = calcular_checksum(mensagem)
        pacote = f"{seq_num}|{checksum}|{mensagem}"
        udp.sendto(pacote.encode(), endereco)
        print(f"[CLIENTE] Pacote enviado: {pacote}")

        try:
            udp.settimeout(TIMEOUT)
            resposta, _ = udp.recvfrom(BUFFER_SIZE)
            ack = resposta.decode()
            print(f"[CLIENTE] Recebeu ACK: {ack}")

            # Verifica se o ACK é válido e tem o número de sequência correto
            if ack == f"ACK|{seq_num}":
                print("[CLIENTE] Mensagem entregue com sucesso!")
                break  # Sai do loop se o pacote for confirmado
        except socket.timeout:
            print("[CLIENTE] Timeout! Reenviando pacote...")
        
        # Alterna o número de sequência para a retransmissão
        seq_num = 1 - seq_num

# Inicia o socket UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nome_usuario = input("Digite seu nome: ")

try:
    while True:
        mensagem = input("Digite sua mensagem (ou 'bye' para sair): ")
        if mensagem.lower() == "bye":
            enviar_mensagem(udp, "bye", (IP_SERVIDOR, PORTA_SERVIDOR))
            print("Saindo do chat...")
            break
        else:
            enviar_mensagem(udp, f"{nome_usuario}: {mensagem}", (IP_SERVIDOR, PORTA_SERVIDOR))
finally:
    udp.close()
    print("Conexão fechada.")
