# <p align="center">Projeto-Redes-IF975 </p>

Repositório para o projeto da disciplina IF975 sobre redes de computadores.
Documentação do Cliente e Servidor UDP

## 1) Membros da `Equipe 1`:
<br>


- [Amós Kinsley (akbs)](https://github.com/amosantana)
- [Diogo Rodrigues (dsr)](https://github.com/Monkius-Maximus)
- [Saunay Coutinho (svsc)](https://github.com/saunayc)


<br>


## 2) Link para repositório git
  
   https://github.com/amosantana/Projeto-Redes---IF975

<br>


## 3) Introdução

Este documento descreve o funcionamento do cliente e servidor UDP para comunicação em rede, utilizando a biblioteca socket em Python. O sistema permite a troca de mensagens de texto e o envio de arquivos de texto entre múltiplos clientes conectados ao servidor.

## 4) Requisitos

Python 3.x

Biblioteca socket (padrão do Python)

Biblioteca threading (padrão do Python)

Biblioteca collections (padrão do Python)

Permissão de acesso a arquivos no sistema

Estrutura do Cliente (client.py)

## 5) Configuração Inicial

IP_Servidor = '127.0.0.1'
PORTA_Servidor = 5000
BUFFER_SIZE = 1024

Define o endereço IP do servidor, a porta utilizada e o tamanho do buffer para transmissão de dados.

## 5.1) Funções

### receber_mensagens(udp)

Inicia uma thread que escuta mensagens recebidas do servidor e as imprime na tela.

### enviar_arquivo(udp, caminho_arquivo)

Lê um arquivo do sistema de arquivos e o envia fragmentado para o servidor, incluindo metadados como ID do arquivo e sequência de pacotes.

### salvar_mensagem_como_arquivo(mensagem)

Salva mensagens de chat como arquivos de texto com um timestamp no nome do arquivo.

### Conexão ao Servidor

O cliente inicia um socket UDP e envia uma mensagem de saudação com o nome do usuário.

### Loop de Entrada

O programa entra em um loop onde o usuário pode:

Digitar mensagens comuns

Enviar arquivos usando FILE <caminho_do_arquivo>

Digitar bye para encerrar a conexão

### Encerramento

Ao sair, o cliente fecha o socket UDP e exibe uma mensagem de encerramento.

## 6) Estrutura do Servidor (server.py)

### Configuração Inicial

MEU_IP = ''
MINHA_PORTA = 5000
BUFFER_SIZE = 1024

Define a porta do servidor e o buffer de transmissão.

### Gerenciamento de Clientes e Arquivos

O servidor armazena clientes conectados e fragmentos de arquivos recebidos:

clientes = {}
file_fragments = defaultdict(dict)

## 6.1) Funções

## processar_arquivo(mensagem, addr)

Processa arquivos recebidos fragmentados, reconstroi-os e retransmite aos clientes conectados.

## salvar_mensagem_como_arquivo(mensagem, addr)

Salva mensagens recebidas em arquivos de texto com timestamp e endereço IP do remetente.

## Loop Principal

O servidor:

Aguarda conexões de clientes

Registra e notifica novas conexões

Gerencia saídas de clientes

Encaminha mensagens e arquivos para todos os clientes conectados

## 7) Encerramento

Quando o servidor é encerrado, após o recebimento da mensagem 'bye' o socket UDP é fechado de forma segura.