# Importa as bibliotecas necessárias
import os
import json
import ftplib
import tarfile
import shutil
import requests
import logging
import re
from tqdm import tqdm
from pathlib import Path
from datetime import datetime
from termcolor import colored

# Carrega o arquivo de configuração.
with open('config.json') as config_file:
    config = json.load(config_file)

# Pega as informações do arquivo de configuração
FTP_HOST = config["FTP_HOST"]
FTP_USER = config["FTP_USER"]
FTP_PASS = config["FTP_PASS"]
FTP_BACKUP_COUNT = config["FTP_BACKUP_COUNT"]
MINECRAFT_DIR = config["MINECRAFT_DIR"]
BACKUP_DIR = config["BACKUP_DIR"]
LOCAL_BACKUP_COUNT = config["LOCAL_BACKUP_COUNT"]
LOG_DIR = config["LOG_DIR"]
PAPER_JAR = config["PAPER_JAR"]
VERSION_HISTORY = config["VERSION_HISTORY"]
API_PAPER = config["PAPER_API"]
PAPER_VERSION = config["PAPER_VERSION"]
api_paper = API_PAPER + PAPER_VERSION + "/"

# Cria as pastas de backup e log se elas não existirem
Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# Data/hora atual
NOW = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Define o nome do arquivo de backup e log
BACKUP_FILE = f"backup_{NOW}.tar.gz"
LOG_FILE = f"{LOG_DIR}/backup_{NOW}.log"

# Configura o log
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Funções para remover cores do texto e logar mensagens
def remove_color(message):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', message)

def log_and_print(msg):
    print(msg)
    logging.info(remove_color(msg))

# Função para calcular o tamanho total do diretório
def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

# Inicia o backup
log_and_print('\n' + colored('Iniciando o processo de backup...', 'yellow') + '\n')

total_size = get_dir_size(MINECRAFT_DIR)
with tarfile.open(f"{BACKUP_DIR}/{BACKUP_FILE}", "w:gz") as tar:
    with tqdm(total=total_size, unit='B', unit_scale=True, desc=colored("Criando backup... ", "green")) as pbar:
        for dirpath, dirnames, filenames in os.walk(MINECRAFT_DIR):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                tar.add(fp)
                pbar.update(os.path.getsize(fp))

log_and_print('\n' + colored('Backup criado!', 'green') + '\n')
log_and_print('\n' + colored('Iniciando o processo de upload FTP...','yellow') + '\n')

# Função para fazer upload com progresso
def upload_with_progress(filename, filepath):
    with open(filepath, 'rb') as f:
        total_size = os.path.getsize(filepath)
        upload_size = 0
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=colored("Enviando... ", "green"))

        def handle_buffer(buf):
            nonlocal upload_size
            upload_size += len(buf)
            progress_bar.update(len(buf))

        ftp.storbinary('STOR %s' % filename, f, 1024, handle_buffer)
        progress_bar.close()

# Configura FTP e faz upload
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(config["FTP_DIR"])

upload_with_progress(BACKUP_FILE, f'{BACKUP_DIR}/{BACKUP_FILE}')

# Verifica se o upload foi bem sucedido
try:
    ftp.voidcmd('NOOP')
    log_and_print('\n' + colored('Upload FTP concluído com sucesso!', 'green') + '\n')
except:
    log_and_print('\n' + colored('Falha no upload FTP!', 'red') + '\n')

# Removendo backups locais mais antigos
backups = sorted(Path(BACKUP_DIR).glob('backup_*.tar.gz'))
if len(backups) > LOCAL_BACKUP_COUNT:
    for backup in backups[:-LOCAL_BACKUP_COUNT]:
        backup.unlink()

# Removendo backups FTP mais antigos
ftp_files = ftp.nlst()
ftp_files.sort(reverse=True)
ftp_files = [file for file in ftp_files if 'backup' in file]

if len(ftp_files) > FTP_BACKUP_COUNT:
    for file in ftp_files[FTP_BACKUP_COUNT:]:
        ftp.delete(file)

# Inicia a atualização do servidor Minecraft
log_and_print('\n' + colored('Iniciando a atualização do servidor Minecraft...','yellow') + '\n')

# Obtém a versão mais recente do servidor PaperMC
response = requests.get(api_paper)
response.raise_for_status()

latest_build = response.json()['builds'][-1]
full_version = f"{PAPER_VERSION}-{latest_build}"
latest_paper_url = f"https://papermc.io/api/v2/projects/paper/versions/{PAPER_VERSION}/builds/{latest_build}/downloads/paper-{full_version}.jar"

# Verifica se a versão já foi baixada
try:
    with open(VERSION_HISTORY, 'r') as f:
        version_history = json.load(f)
except FileNotFoundError:
    version_history = {}

# Obtém a versão atual do servidor
current_version = list(version_history.values())[-1] if version_history else "N/A"

if full_version in version_history.values():
    log_and_print(colored(f"Versão atual ", "green") + colored(f"{full_version}", "red") + colored(" já é a mais recente.", "green"))
else:
    log_and_print(colored("Versão atual do servidor: ", "green") + colored(f"{current_version}", "red"))
    log_and_print(colored("Atualizando para a versão: ", "green") + colored(f"{full_version}", "red"))

    # Remove o arquivo antigo, se existir
    old_paper_jar = f"{MINECRAFT_DIR}/paper.jarOLD"
    if os.path.exists(old_paper_jar):
        os.remove(old_paper_jar)
        log_and_print(colored(f"Arquivo ", "green") + colored(f"{old_paper_jar}", "red") + colored(" removido.", "green"))

    # Renomeia o arquivo paper.jar atual para paper.jarOLD
    if os.path.exists(PAPER_JAR):
        os.rename(PAPER_JAR, old_paper_jar)
        log_and_print(colored(f"Arquivo ", "green") + colored(f"{PAPER_JAR}", "red") + colored(" renomeado para ", "green") + colored(f"{old_paper_jar}", "red"))

    # Faz download da versão mais recente
    response = requests.get(latest_paper_url, stream=True)
    response.raise_for_status()
    
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=colored(f"Baixando build ", "green") + colored(f"{latest_build}", "red"))

    # Salva o arquivo com um nome temporário
    temp_paper_jar = f"{MINECRAFT_DIR}/paper-{latest_build}.jar"
    with open(temp_paper_jar, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            progress_bar.update(len(chunk))
            f.write(chunk)

    progress_bar.close()

    # Renomeia o novo arquivo para paper.jar
    os.rename(temp_paper_jar, PAPER_JAR)
    log_and_print(colored(f"Arquivo ", "green") + colored(f"{temp_paper_jar}", "red") + colored(" renomeado para ", "green") + colored(f"{PAPER_JAR}", "red"))

    # Adicione a nova versão ao arquivo de histórico
    version_history[str(datetime.now())] = full_version
    with open(VERSION_HISTORY, 'w') as f:
        json.dump(version_history, f, indent=4)

    log_and_print(colored(f"Versão ", "green") + colored(f"{full_version}", "red") + colored(" baixada com sucesso.", "green"))

log_and_print(colored("Atualização do servidor Minecraft concluída com sucesso!", "green"))

# Fecha a conexão FTP
ftp.quit()
