import socket
import threading
import os
import datetime

IP_Servidor = '127.0.0.1'
PORTA_Servidor = 5000
BUFFER_SIZE = 1024

def receber_mensagens(udp):
    while True:
        try:
            mensagem, _ = udp.recvfrom(BUFFER_SIZE)
            print(mensagem.decode("utf8"))
        except:
            break

def enviar_arquivo(udp, caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
            file_id = os.path.basename(caminho_arquivo)
            total = (len(conteudo) + BUFFER_SIZE - 1) // BUFFER_SIZE  #numero total de fragmentos

            for num in range(total):
                fragmento = conteudo[num * BUFFER_SIZE:(num + 1) * BUFFER_SIZE]
                mensagem = f"FILE|{file_id}:{num}:{total}|{fragmento}"
                udp.sendto(mensagem.encode("utf8"), (IP_Servidor, PORTA_Servidor))
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

def salvar_mensagem_como_arquivo(mensagem):
    try:
        nome_arquivo = f"mensagem_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
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

#iniciar a thread para receber mensagens
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
            nome_arquivo = salvar_mensagem_como_arquivo(mensagem)
            if nome_arquivo:
                enviar_arquivo(udp, nome_arquivo)
finally:
    udp.close()
    print("Conexão fechada.")