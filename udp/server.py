import socket
import datetime
from collections import defaultdict
import os

MEU_IP = ''
MINHA_PORTA = 5000
BUFFER_SIZE = 1024

# criação do socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((MEU_IP, MINHA_PORTA))

print("Servidor rodando e aguardando mensagens...")

clientes = {}
file_fragments = defaultdict(lambda: defaultdict(str))  # {file_id: {num: data}}
file_fragment_count = {}  # {file_id: total_fragments}

# Função para processar fragmentos de arquivos
def processar_arquivo(mensagem, addr):
    try:
        header, content = mensagem.split('|', 1)
        file_id, num, total = header.split(':')
        num = int(num)
        total = int(total)
        
        # Armazenamento do fragmento
        file_fragments[file_id][num] = content
        file_fragment_count[file_id] = total
        
        # Verifica se todos os fragmentos foram recebidos
        if len(file_fragments[file_id]) == total:
            # Reconstruir o arquivo
            full_content = ''.join(file_fragments[file_id][i] for i in range(total))
            
            # Formatar a mensagem
            nome_usuario = clientes[addr]
            hora_data = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            mensagem_formatada = f"{addr[0]}:{addr[1]}/~{nome_usuario}: {full_content} {hora_data}"
            print(mensagem_formatada)
            
            # Enviar para todos os clientes
            for cliente in clientes:
                udp.sendto(mensagem_formatada.encode("utf8"), cliente)
            
            # Remover fragmentos após reconstrução
            del file_fragments[file_id]
            del file_fragment_count[file_id]
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")

# Função para salvar arquivo
def salvar_mensagem_como_arquivo(mensagem, addr):
    try:
        nome_arquivo = f"mensagem_{addr[0]}_{addr[1]}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(mensagem)
        return nome_arquivo
    except Exception as e:
        print(f"Erro ao salvar mensagem como arquivo: {e}")
        return None

# Loop principal para receber mensagens e processá-las
try:
    while True:
        Mensagem_Recebida, END_client = udp.recvfrom(BUFFER_SIZE)
        mensagem = Mensagem_Recebida.decode("utf8").strip()

        if mensagem.startswith("hi, meu nome eh "):
            nome_usuario = mensagem[16:]
            clientes[END_client] = nome_usuario
            print(f"{END_client[0]}:{END_client[1]}/~{nome_usuario} entrou na sala.")
            udp.sendto(f"hi, meu nome eh {nome_usuario}!".encode("utf8"), END_client)
            
            # Notificação de um novo usuário
            for cliente in clientes:
                if cliente != END_client:
                    udp.sendto(f"{END_client[0]}:{END_client[1]}/~{nome_usuario} entrou na sala.".encode("utf8"), cliente)
        elif mensagem.lower() == "bye":
            if END_client in clientes:
                nome_usuario = clientes.pop(END_client)
                print(f"{END_client[0]}:{END_client[1]}/~{nome_usuario} saiu da sala.")
                udp.sendto("Você saiu do chat.".encode("utf8"), END_client)
                
                # Notificação
                for cliente in clientes:
                    udp.sendto(f"{END_client[0]}:{END_client[1]}/~{nome_usuario} saiu da sala.".encode("utf8"), cliente)
            else:
                udp.sendto("Você não está no chat.".encode("utf8"), END_client)
        elif mensagem.startswith("FILE|"):
            processar_arquivo(mensagem[5:], END_client)
        else:
            if END_client in clientes:
                nome_usuario = clientes[END_client]
                hora_data = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                mensagem_formatada = f"{END_client[0]}:{END_client[1]}/~{nome_usuario}: {mensagem} {hora_data}"
                print(mensagem_formatada)
                for cliente in clientes:
                    udp.sendto(mensagem_formatada.encode("utf8"), cliente)
finally:
    udp.close()
    print("Servidor encerrado.")
