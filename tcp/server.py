import socket
import hashlib

# Configuração do servidor
MEU_IP = ''
MINHA_PORTA = 5000
BUFFER_SIZE = 1024

# Função para calcular o checksum
def calcular_checksum(mensagem):
    return hashlib.md5(mensagem.encode()).hexdigest()

# Inicializa o socket UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((MEU_IP, MINHA_PORTA))

print("[SERVIDOR] Servidor aguardando mensagens...")

ultimo_seq = -1  # Número de sequência do último pacote recebido corretamente

try:
    while True:
        mensagem_recebida, endereco_cliente = udp.recvfrom(BUFFER_SIZE)
        mensagem_recebida = mensagem_recebida.decode()
        print(f"[SERVIDOR] Pacote recebido: {mensagem_recebida}")
        
        # Divide o pacote nos componentes esperados
        try:
            seq_num, checksum_recebido, mensagem = mensagem_recebida.split('|', 2)
            seq_num = int(seq_num)
        except ValueError:
            print("[SERVIDOR] Erro ao dividir o pacote. Descartando...")
            continue

        # Calcula o checksum para validar integridade
        checksum_calculado = calcular_checksum(mensagem)
        if checksum_recebido != checksum_calculado:
            print("[SERVIDOR] Pacote corrompido! Reenviando último ACK...")
            udp.sendto(f"ACK|{ultimo_seq}".encode(), endereco_cliente)
            continue
        
        # Verifica se o pacote é duplicado
        if seq_num == ultimo_seq:
            print("[SERVIDOR] Pacote duplicado! Reenviando último ACK...")
            udp.sendto(f"ACK|{ultimo_seq}".encode(), endereco_cliente)
            continue
        
        # Mensagem válida, processamos normalmente
        print(f"[SERVIDOR] Mensagem entregue: {mensagem}")
        ultimo_seq = seq_num  # Atualiza o último número de sequência recebido

        # Enviar ACK confirmando o recebimento
        udp.sendto(f"ACK|{seq_num}".encode(), endereco_cliente)
        print(f"[SERVIDOR] Enviando ACK {seq_num}")

finally:
    udp.close()
    print("[SERVIDOR] Servidor encerrado.")
