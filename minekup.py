import os
import json
import ftplib
import tarfile
import shutil
import requests
import logging
from tqdm import tqdm
from pathlib import Path
from datetime import datetime

# Carrega o arquivo de configuração.
with open('config.json') as config_file:
    config = json.load(config_file)

FTP_HOST = config["FTP_HOST"]
FTP_USER = config["FTP_USER"]
FTP_PASS = config["FTP_PASS"]
MINECRAFT_DIR = config["MINECRAFT_DIR"]
BACKUP_DIR = config["BACKUP_DIR"]
LOG_DIR = config["LOG_DIR"]
PAPER_JAR = config["PAPER_JAR"]
API_PAPER = config["PAPER_API"]
VERSION_HISTORY = config["VERSION_HISTORY"]

# Cria as pastas de backup e log se elas não existirem
Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# Data/hora atual
NOW = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Define o nome do arquivo de backup e log
BACKUP_FILE = f"backup_{NOW}.tar.gz"
LOG_FILE = f"{LOG_DIR}/backup_{NOW}.log"

# Configurando o logger
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def log_and_print(msg):
    print(msg)
    logging.info(msg)

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

log_and_print("Iniciando o processo de backup...")

total_size = get_dir_size(MINECRAFT_DIR)
with tarfile.open(f"{BACKUP_DIR}/{BACKUP_FILE}", "w:gz") as tar:
    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Criando backup") as pbar:
        for dirpath, dirnames, filenames in os.walk(MINECRAFT_DIR):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                tar.add(fp)
                pbar.update(os.path.getsize(fp))

log_and_print("Backup criado")
log_and_print("Iniciando o processo de upload FTP...")

def upload_with_progress(filename, filepath):
    with open(filepath, 'rb') as f:
        total_size = os.path.getsize(filepath)
        upload_size = 0
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc="Carregando...")

        def handle_buffer(buf):
            nonlocal upload_size
            upload_size += len(buf)
            progress_bar.update(len(buf))

        ftp.storbinary('STOR %s' % filename, f, 1024, handle_buffer)
        progress_bar.close()

ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)
ftp.cwd(config["FTP_DIR"])

upload_with_progress(BACKUP_FILE, f'{BACKUP_DIR}/{BACKUP_FILE}')

try:
    ftp.voidcmd('NOOP')
    log_and_print("Upload FTP concluído com sucesso")
except:
    log_and_print("Falha no upload FTP")

backups = sorted(Path(BACKUP_DIR).glob('backup_*.tar.gz'))
if len(backups) > 5:
    for backup in backups[:-5]:
        backup.unlink()

log_and_print("Backups antigos removidos")

ftp_files = ftp.nlst()
ftp_files.sort(reverse=True)
ftp_files = [file for file in ftp_files if 'backup' in file]

if len(ftp_files) > 5:
    for file in ftp_files[5:]:
        ftp.delete(file)

# Inicia a atualização do servidor Minecraft
log_and_print("Iniciando a atualização do servidor Minecraft...")

# Obtém a versão mais recente do servidor PaperMC
response = requests.get(API_PAPER)
response.raise_for_status()

latest_build = response.json()['builds'][-1]
latest_paper_url = f"https://papermc.io/api/v2/projects/paper/versions/1.19.4/builds/{latest_build}/downloads/paper-1.19.4-{latest_build}.jar"

# Verifique se a versão já foi baixada
try:
    with open(VERSION_HISTORY, 'r') as f:
        version_history = json.load(f)
except FileNotFoundError:
    version_history = {}

if latest_build in version_history.values():
    log_and_print(f"Versão {latest_build} já baixada.")
else:
    # Remove o arquivo antigo, se existir
    old_paper_jar = f"{MINECRAFT_DIR}/paper.jarOLD"
    if os.path.exists(old_paper_jar):
        os.remove(old_paper_jar)
        log_and_print(f"Arquivo {old_paper_jar} removido.")

    # Renomeia o arquivo paper.jar atual para paper.jarOLD
    if os.path.exists(PAPER_JAR):
        os.rename(PAPER_JAR, old_paper_jar)
        log_and_print(f"Arquivo {PAPER_JAR} renomeado para {old_paper_jar}")

    # Faz download da versão mais recente
    response = requests.get(latest_paper_url, stream=True)
    response.raise_for_status()
    
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=f"Baixando build {latest_build}")

    # Salva o arquivo com um nome temporário
    temp_paper_jar = f"{MINECRAFT_DIR}/paper-{latest_build}.jar"
    with open(temp_paper_jar, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            progress_bar.update(len(chunk))
            f.write(chunk)

    progress_bar.close()

    # Renomeia o novo arquivo para paper.jar
    os.rename(temp_paper_jar, PAPER_JAR)
    log_and_print(f"Arquivo {temp_paper_jar} renomeado para {PAPER_JAR}")

    # Adicione a nova versão ao arquivo de histórico
    version_history[str(datetime.now())] = latest_build
    with open(VERSION_HISTORY, 'w') as f:
        json.dump(version_history, f, indent=4)

    log_and_print(f"Versão {latest_build} baixada com sucesso.")

log_and_print("Atualização do servidor Minecraft concluída com sucesso")

ftp.quit()
