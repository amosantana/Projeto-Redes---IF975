# <p align="center">Projeto-Redes-IF975 </p>

<a name="readme-top"></a>
# <p align="center">Chat de sala única com UDP e RDT3.0</p>

Implementação de um sistema de chat com transferência confiável utilizando o protocolo RDT 3.0 sobre UDP, garantindo entrega ordenada e sem erros mesmo em condições de rede instável.

## 1) Membros da `Equipe 1` 👥:
<br>


- [Amós Kinsley (akbs)](https://github.com/amosantana)
- [Diogo Rodrigues (dsr)](https://github.com/Monkius-Maximus)
- [Saunay Coutinho (svsc)](https://github.com/saunayc)



## 2) Link para repositório git
  
   https://github.com/amosantana/Projeto-Redes---IF975


## 3) Requisitos

Python 3.x

Biblioteca socket (padrão do Python)

Biblioteca threading (padrão do Python)

Biblioteca collections (padrão do Python)

Biblioteca zlib (compactação de arquivos)

Permissão de acesso a arquivos no sistema

Estrutura do Cliente (client.py)

## 📦 Estrutura do Projeto

```
chat-rdt3/
├── client.py            # Cliente do chat
├── server.py            # Servidor central
├── mensagens_txt/       # Histórico de mensagens
├── requirements.txt     # Dependências
└── README.md            # Documentação
```

## 🚀 Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/chat-rdt3.git
cd chat-rdt3
```

2. Execute o servidor:
```bash
python server.py
```

3. Execute clientes em terminais separados:
```bash
python client.py
```

## 🔧 Funcionamento do Protocolo

## 📁 Arquivos do Projeto

### `client.py`
Implementa o cliente do chat, responsável por enviar e receber mensagens usando UDP com RDT 3.0.

#### Funcionalidades:
- **Conexão ao servidor**: Conecta-se ao servidor via UDP.
- **Envio de mensagens**: Envia mensagens fragmentadas com confirmação (ACK) usando RDT 3.0.
- **Recebimento de mensagens**: Escuta mensagens do servidor e as exibe.
- **Envio de arquivos**: Permite o envio de arquivos fragmentados.
- **Salvamento de mensagens**: Salva mensagens recebidas em arquivos locais.

#### Métodos Principais:
- `receber_mensagens(udp)`: Escuta mensagens do servidor e trata ACKs.
- `enviar_mensagem_confiavel(udp, mensagem)`: Envia mensagens com confirmação usando RDT 3.0.
- `enviar_arquivo(udp, caminho_arquivo)`: Envia um arquivo fragmentado ao servidor.
- `salvar_mensagem_como_arquivo(mensagem)`: Salva mensagens em arquivos locais.

#### Variáveis Importantes:
- `IP_Servidor`, `PORTA_Servidor`: Configurações do servidor.
- `seq_num`: Número de sequência para RDT 3.0.
- `ack_recebido`: Evento para sincronização de ACKs.

---

### `server.py`
Implementa o servidor do chat, responsável por gerenciar conexões e retransmitir mensagens.

#### Funcionalidades:
- **Gerenciamento de clientes**: Mantém uma lista de clientes conectados.
- **Processamento de mensagens**: Recebe mensagens dos clientes e as retransmite.
- **Fragmentação de mensagens**: Divide mensagens grandes em pacotes menores.
- **Processamento de arquivos**: Reconstroi arquivos enviados fragmentados.

#### Métodos Principais:
- `processar_arquivo(mensagem, addr)`: Reconstroi arquivos a partir de fragmentos.
- `salvar_mensagem_como_arquivo(mensagem, addr)`: Salva mensagens em arquivos locais.
- `fragmentar_mensagem(mensagem, max_size)`: Fragmenta mensagens para envio.

#### Variáveis Importantes:
- `clientes`: Dicionário de clientes conectados.
- `file_fragments`: Armazena fragmentos de arquivos recebidos.
- `seq_esperado`: Números de sequência esperados para cada cliente.

---

### Formato dos Pacotes
```python
# Mensagem:
f"RDT|{seq_num}|{checksum}|{mensagem}"

# ACK:
f"ACK|{seq_num}|{checksum_ack}"


## 📌 Recursos Implementados

✔️ **Transferência confiável** com RDT 3.0  
✔️ **Controle de fluxo** com números de sequência de 1 bit  
✔️ **Detecção de erros** via checksum CRC32  
✔️ **Retransmissão** após timeout  
✔️ **Tratamento de ACKs** duplicados e corrompidos  
✔️ **Simulação de erros** para demonstração  

## Integrantes

<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/amosantana">
        <img src="https://avatars.githubusercontent.com/u/157263012?v=4" width="200px;" border-radius="50%;" alt="Foto do Integrante"/><br>
        <sub><b>Amós Santana</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Monkius-Maximus">
        <img src="https://avatars.githubusercontent.com/u/149613054?v=4" width="200px;" border-radius="50%;" alt="Foto do Integrante"/><br>
        <sub><b>Diogo Rodrigues</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/saunayc">
        <img src="https://avatars.githubusercontent.com/u/90536225?v=4" width="200px;" border-radius="50%;" alt="Foto do Integrante"/><br>
        <sub><b>Saunay Coutinho</b></sub>
      </a>
    </td>
  </tr>
</table>

## 🎥 Vídeo do funcionamento do progama realizado pela equipe:

  <p align="center">
     Link de acesso:
  </p>

  ## 📌 Licença
Este projeto é open-source. Sinta-se à vontade para modificar e distribuir.