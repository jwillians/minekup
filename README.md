### MineKup

MineKup é um script simples, mas poderoso, escrito em Python, projetado para ajudar os administradores de servidores Minecraft a fazer backups de seus servidores Minecraft (Paper). Ele executa o backup do servidor localmente e remotamente (via FTP) e, em seguida, atualiza o servidor Paper para a versão mais recente disponível.

## Recursos

- Faz backup do seu servidor de Minecraft localmente.
- Faz backup do seu servidor de Minecraft remotamente via FTP.
- Atualiza seu servidor PaperMC para a versão mais recente disponível.
- Configurações facilmente ajustáveis em um arquivo de configuração JSON.

## Dependências

Este script usa os módulos Python `requests` e `tqdm`. Você pode instalá-los com o seguinte comando:

```shell
pip install requests tqdm
```
## Uso
Primeiro, clone este repositório para o seu sistema.
Depois, ajuste as configurações no arquivo config.json. Aqui está um exemplo de como o arquivo de configuração pode ser:

```shell
{
    "FTP_HOST": "seu.host.ftp",
    "FTP_USER": "seu_usuario_ftp",
    "FTP_PASS": "sua_senha_ftp",
    "FTP_DIR": "diretorio_destino",
    "MINECRAFT_DIR": "nome_diretorio_minecraft",
    "BACKUP_DIR": "nome_diretorio_backups",
    "LOG_DIR": "nome_diretorio_logs",
    "PAPER_API": "url_da_api_papermc",
    "VERSION_HISTORY": "nome_arquivo_historico_versao"
}
```

Substitua os valores dos campos pelo seu próprio host FTP, nome de usuário, senha, etc.
Depois de ajustar as configurações, você pode executar o script com:

```shell
python minekup.py
```
Isso fará backup do seu servidor e atualizará o servidor PaperMC.

### English:

### MineKup

MineKup is a simple yet powerful script written in Python, designed to help Minecraft server administrators back up their Minecraft servers (Paper). It performs the backup of your server locally and remotely (via FTP) and then updates the Paper server to the latest version available.

## Features
- Backs up your Minecraft server locally.
- Backs up your Minecraft server remotely via FTP.
- Updates your PaperMC server to the latest available version.
- Easily adjustable settings in a JSON configuration file.


## Dependencies

This script uses the Python modules requests and tqdm. You can install them with the following command:

```shell
pip install requests tqdm
```

## Usage

First, clone this repository to your system.
Then adjust the settings in the config.json file. Here's an example of what the configuration file might look like:

```shell
{
    "FTP_HOST": "your.ftp.host",
    "FTP_USER": "your_ftp_user",
    "FTP_PASS": "your_ftp_pass",
    "FTP_DIR": "destination_directory",
    "MINECRAFT_DIR": "minecraft_directory_name",
    "BACKUP_DIR": "backups_directory_name",
    "LOG_DIR": "logs_directory_name",
    "PAPER_API": "papermc_api_url",
    "VERSION_HISTORY": "version_history_file_name"
}
```
Replace the values of the fields with your own FTP host, username, password, etc.
After adjusting the settings, you can run the script with:

```shell
python minekup.py
```
This will back up your server and update the PaperMC server.

