import socket
import threading
import os
import datetime
import time
import zlib

# Configurações do cliente
IP_Servidor = '127.0.0.1'
PORTA_Servidor = 5000
BUFFER_SIZE = 1024
TIMEOUT = 50  # segundos

seq_num = 0  # número de sequência para RDT 3.0
ack_recebido = threading.Event()

def calcular_checksum(mensagem):
    return zlib.crc32(mensagem.encode("utf8"))

def receber_mensagens(udp):
    # Escuta mensagens enviadas pelo servidor e as imprime na tela.
    global ack_recebido
    while True:
        try:
            mensagem, _ = udp.recvfrom(BUFFER_SIZE)
            mensagem_decodificada = mensagem.decode("utf8")

            if mensagem_decodificada.startswith("ACK|"):
                ack_seq = int(mensagem_decodificada.split('|')[1])
                print(f"[CLIENTE] ACK recebido para pacote seq={ack_seq}")
                if ack_seq == seq_num:
                    ack_recebido.set()
            else:
                print(mensagem_decodificada)
                salvar_mensagem_como_arquivo(mensagem_decodificada)
        except:
            break

def fragmentar_mensagem(mensagem, max_size=900):
    # Fragmenta a mensagem em partes menores de até 1024 bytes
    fragmentos = []
    while len(mensagem) > max_size:
        fragmentos.append(mensagem[:max_size])
        mensagem = mensagem[max_size:]
    if mensagem:
        fragmentos.append(mensagem)
    return fragmentos

def enviar_mensagem_confiavel(udp, mensagem):
    global seq_num, ack_recebido

    fragmentos = fragmentar_mensagem(mensagem)

    # Variável para armazenar os fragmentos recebidos e reconstruir a mensagem
    fragmentos_recebidos = []

    for fragmento in fragmentos:
        checksum = calcular_checksum(fragmento)
        pacote = f"RDT|{seq_num}|{checksum}|{fragmento}"

        while True:
            udp.sendto(pacote.encode("utf8"), (IP_Servidor, PORTA_Servidor))
            print(f"[CLIENTE] Pacote enviado com seq={seq_num}, aguardando ACK...")

            ack_recebido.clear()
            ack_recebido.wait(timeout=TIMEOUT)

            if ack_recebido.is_set():
                seq_num = 1 - seq_num  # alterna entre 0 e 1
                fragmentos_recebidos.append(fragmento)  # Adiciona o fragmento à lista de fragmentos recebidos
                salvar_mensagem_como_arquivo(f"{nome_usuario}: {fragmento}")
                break
            else:
                print(f"[CLIENTE] Timeout! Reenviando pacote seq={seq_num}...")

    # Após enviar todos os fragmentos, reconstrua a mensagem completa
    mensagem_reconstruida = ''.join(fragmentos_recebidos)
    salvar_mensagem_como_arquivo(f"Mensagem completa recebida: {mensagem_reconstruida}")

def enviar_arquivo(udp, caminho_arquivo):
    # Lê e envia um arquivo em fragmentos para o servidor.
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
            file_id = os.path.basename(caminho_arquivo)
            total = (len(conteudo) + BUFFER_SIZE - 1) // BUFFER_SIZE  # número total de fragmentos

            for num in range(total):
                fragmento = conteudo[num * BUFFER_SIZE:(num + 1) * BUFFER_SIZE]
                mensagem = f"FILE|{file_id}:{num}:{total}|{fragmento}"
                udp.sendto(mensagem.encode("utf8"), (IP_Servidor, PORTA_Servidor))
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

def salvar_mensagem_como_arquivo(mensagem):
    try:
        if not os.path.exists("mensagens_txt"):
            os.makedirs("mensagens_txt")
        nome_arquivo = f"mensagens_txt/mensagem_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(mensagem)
        return nome_arquivo
    except Exception as e:
        print(f"Erro ao salvar mensagem como arquivo: {e}")
        return None

try:
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.connect((IP_Servidor, PORTA_Servidor))
except Exception as e:
    print(f"Erro ao conectar ao servidor: {e}")
    exit(1)

nome_usuario = input("Digite seu nome: ")
udp.sendto(f"hi, meu nome eh {nome_usuario}".encode("utf8"), (IP_Servidor, PORTA_Servidor))

print("Conectado ao chat. Digite suas mensagens (ou 'bye' para sair):")

# iniciar a thread para receber mensagens
thread_receber = threading.Thread(target=receber_mensagens, args=(udp,))
thread_receber.start()

try:
    while True:
        mensagem = input()

        if mensagem.lower() == "bye":
            udp.sendto("bye".encode("utf8"), (IP_Servidor, PORTA_Servidor))
            print("Saindo do chat...")
            break
        elif mensagem.startswith("FILE "):
            caminho_arquivo = mensagem[5:]
            enviar_arquivo(udp, caminho_arquivo)
        else:
            enviar_mensagem_confiavel(udp, mensagem)
finally:
    udp.close()
    print("Conexão fechada.")
