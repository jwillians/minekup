# MineKup

## Português

**MineKup** é uma ferramenta simples escrita em Python, projetada para fazer backup do seu servidor de Minecraft (Paper). Ele realiza o backup de forma local e remota via FTP, e imediatamente após, atualiza o servidor Paper para a versão mais recente disponível.

### Requisitos

* Python 3.6+
* Uma conexão FTP ativa para backup remoto
* Bibliotecas Python: `requests` e `tqdm`

### Instalação

Para instalar as bibliotecas necessárias, use o comando pip:

pip install -r requirements.txt

### Como usar

1. Faça o clone deste repositório para o seu computador.
2. Preencha o arquivo de configuração `config.json` com as informações do seu servidor e da sua conexão FTP.
3. Execute o script `minekup.py` para iniciar o backup e o processo de atualização.

## English

**MineKup** is a simple tool written in Python, designed to backup your Minecraft (Paper) server. It performs the backup both locally and remotely via FTP, and immediately afterward, updates the Paper server to the latest available version.

### Requirements

* Python 3.6+
* An active FTP connection for remote backup
* Python Libraries: `requests` and `tqdm`

### Installation

To install necessary libraries, use the pip command:

pip install -r requirements.txt

### How to Use

1. Clone this repository to your machine.
2. Fill out the `config.json` configuration file with your server's and FTP connection's information.
3. Run the `minekup.py` script to start the backup and update process.
