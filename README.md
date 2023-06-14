### MineKup

MineKup é um script simples, mas poderoso, escrito em Python, projetado para ajudar os administradores de servidores Minecraft a fazer backups de seus servidores Minecraft (Paper). Ele executa o backup do servidor localmente e remotamente (via FTP) e, em seguida, atualiza o servidor Paper para a versão especificada ou mais recente disponível.

## Recursos

- Faz backup do seu servidor de Minecraft localmente.
- Faz backup do seu servidor de Minecraft remotamente via FTP.
- Atualiza seu servidor PaperMC para a versão especificada ou mais recente disponível.
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
    "PAPER_JAR": "caminho_completo_do_paper.jar",
    "VERSION_HISTORY": "caminho_completo_do_arquivo_de_historico_de_versao",
    "API_PAPER": "https://papermc.io/api/v2/projects/paper/versions/",
    "PAPER_VERSION": "1.20"
}

```

Substitua os valores dos campos pelo seu próprio host FTP, nome de usuário, senha, etc.
Depois de ajustar as configurações, você pode executar o script com:

```shell
python minekup.py
```
Isso fará backup do seu servidor e atualizará o servidor PaperMC.

Escolhendo uma Versão Específica do PaperMC

Agora o script de backup e atualização do servidor suporta a seleção de uma versão específica do PaperMC. Essa funcionalidade permite que você escolha qual versão do PaperMC deseja que o servidor seja atualizado.

Para configurar a versão desejada, siga estes passos:

Abra o arquivo config.json.
Encontre a linha que contém "PAPER_VERSION": "1.20".
Altere o número 1.20 para a versão do PaperMC que você deseja utilizar. Por exemplo, se você deseja usar a versão 1.21, modifique a linha para "PAPER_VERSION": "1.21".
Salve e feche o arquivo config.json.
Execute o script de backup e atualização do servidor. Ele agora usará a versão do PaperMC que você especificou.
Por favor, note que a versão que você especificar deve ser uma versão válida do PaperMC. Caso contrário, o script não será capaz de baixar e instalar a versão desejada.

### English:

### MineKup

MineKup is a simple yet powerful script, written in Python, designed to assist Minecraft server administrators in backing up their Minecraft servers (Paper). It carries out the server backup locally and remotely (via FTP), and then updates the Paper server to the specified version or the latest version available.

## Features
- Backs up your Minecraft server locally.
- Backs up your Minecraft server remotely via FTP.
- Updates your PaperMC server to the specified version or the latest available version.
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

Choosing a Specific PaperMC Version
The server backup and update script now supports selecting a specific version of PaperMC. This feature allows you to choose which version of PaperMC you want the server to be updated to.

To set up the desired version, follow these steps:

Open the config.json file.
Find the line that contains "PAPER_VERSION": "1.20".
Change the number 1.20 to the version of PaperMC that you want to use. For example, if you want to use version 1.21, modify the line to "PAPER_VERSION": "1.21".
Save and close the config.json file.
Run the server backup and update script. It will now use the PaperMC version you specified.
Please note that the version you specify must be a valid PaperMC version. Otherwise, the script will not be able to download and install the desired version.

