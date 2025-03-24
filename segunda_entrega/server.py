import socket
import datetime
from collections import defaultdict
import os
import zlib

MEU_IP = ''
MINHA_PORTA = 5000
BUFFER_SIZE = 1024

# criação do socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((MEU_IP, MINHA_PORTA))

print("Servidor rodando e aguardando mensagens...")

clientes = {}
file_fragments = defaultdict(dict)
seq_esperado = {}

def calcular_checksum(mensagem):
    return zlib.crc32(mensagem.encode("utf8"))

def fragmentar_mensagem(mensagem, max_size=100):
    """Fragmenta a mensagem em pacotes menores com número de sequência."""
    fragments = []
    total_fragments = (len(mensagem) // max_size) + (1 if len(mensagem) % max_size > 0 else 0)
    
    for i in range(total_fragments):
        fragment = mensagem[i * max_size:(i + 1) * max_size]
        fragments.append((i, total_fragments, fragment))  # (número de sequência, total de fragmentos, fragmento)
    
    return fragments

def processar_arquivo(mensagem, addr):
    try:
        header, content = mensagem.split('|', 1)
        file_id, num, total = header.split(':')
        num = int(num)
        total = int(total)

        file_fragments[file_id][num] = content

        if len(file_fragments[file_id]) == total:
            full_content = ''.join([file_fragments[file_id][i] for i in range(total)])
            nome_usuario = clientes[addr]
            hora_data = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            mensagem_formatada = f"{addr[0]}:{addr[1]}/~{nome_usuario}: {full_content} {hora_data}"
            print(mensagem_formatada)
            for cliente in clientes:
                udp.sendto(mensagem_formatada.encode("utf8"), cliente)
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")

def salvar_mensagem_como_arquivo(mensagem, addr):
    try:
        nome_arquivo = f"mensagem_{addr[0]}_{addr[1]}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(mensagem)
        return nome_arquivo
    except Exception as e:
        print(f"Erro ao salvar mensagem como arquivo: {e}")
        return None

try:
    while True:
        try:
            Mensagem_Recebida, END_client = udp.recvfrom(BUFFER_SIZE)
            mensagem = Mensagem_Recebida.decode("utf8").strip()

            if mensagem.startswith("hi, meu nome eh "):
                nome_usuario = mensagem[16:]
                clientes[END_client] = nome_usuario
                seq_esperado[END_client] = 0
                print(f"{END_client[0]}:{END_client[1]}/~{nome_usuario} entrou na sala.")
                udp.sendto(f"hi, meu nome eh {nome_usuario}!".encode("utf8"), END_client)
                for cliente in clientes:
                    if cliente != END_client:
                        udp.sendto(f"{END_client[0]}:{END_client[1]}/~{nome_usuario} entrou na sala.".encode("utf8"), cliente)

            elif mensagem.lower() == "bye":
                if END_client in clientes:
                    nome_usuario = clientes.pop(END_client)
                    print(f"{END_client[0]}:{END_client[1]}/~{nome_usuario} saiu da sala.")
                    udp.sendto("Você saiu do chat.".encode("utf8"), END_client)  # Informa ao cliente que ele saiu da sala.
                    for cliente in clientes:
                        udp.sendto(f"{END_client[0]}:{END_client[1]}/~{nome_usuario} saiu da sala.".encode("utf8"), cliente)  # Notifica os outros clientes.
                else:
                    udp.sendto("Você não está no chat.".encode("utf8"), END_client)  # Caso o cliente não esteja na sala.

            elif mensagem.startswith("FILE|"):
                processar_arquivo(mensagem[5:], END_client)

            elif mensagem.startswith("RDT|"):
                partes = mensagem.split('|', 3)
                if len(partes) < 4:
                    continue
                _, seq, checksum_recebido, conteudo = partes
                seq = int(seq)
                checksum_recebido = int(checksum_recebido)
                checksum_calculado = calcular_checksum(conteudo)

                print(f"[SERVIDOR] Pacote recebido de {END_client}, seq={seq}, checksum={checksum_recebido}")

                if checksum_recebido != checksum_calculado:
                    print(f"[SERVIDOR] Checksum incorreto! Enviando ACK duplicado para seq={1 - seq}")
                    udp.sendto(f"ACK|{1 - seq}".encode("utf8"), END_client)
                    continue

                if END_client not in seq_esperado:
                    seq_esperado[END_client] = 0

                if seq != seq_esperado[END_client]:
                    print(f"[SERVIDOR] Seq diferente do esperado! Ignorando duplicado. Enviando ACK para seq={1 - seq}")
                    udp.sendto(f"ACK|{1 - seq}".encode("utf8"), END_client)
                    continue

                nome_usuario = clientes[END_client]
                hora_data = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                mensagem_formatada = f"{END_client[0]}:{END_client[1]}/~{nome_usuario}: {conteudo} {hora_data}"
                print(mensagem_formatada)

                for cliente in clientes:
                    udp.sendto(mensagem_formatada.encode("utf8"), cliente)

                udp.sendto(f"ACK|{seq}".encode("utf8"), END_client)
                seq_esperado[END_client] = 1 - seq

            else:
                # Fragmentando a mensagem antes de enviar
                fragments = fragmentar_mensagem(mensagem)

                for seq, total, fragment in fragments:
                    checksum = calcular_checksum(fragment)
                    udp.sendto(f"RDT|{seq}|{checksum}|{fragment}".encode("utf8"), END_client)

        except ConnectionResetError:
            print("Conexão foi interrompida por um cliente. Continuando a execução do servidor...")

finally:
    udp.close()
    print("Servidor encerrado.")
