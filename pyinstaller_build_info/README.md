## Instruções para Compilação com PyInstaller

Este diretório contém o comando PyInstaller para compilar o aplicativo `yt-downloader` em um executável (EXE) para Windows.

### Pré-requisitos:

1.  **Python 3.x** instalado.
2.  **pip** (gerenciador de pacotes do Python) instalado.
3.  **PyInstaller** instalado: `pip install pyinstaller`
4.  **yt-dlp** e **PySide6** instalados: `pip install -r ../requirements.txt`
5.  **FFmpeg** e **FFprobe** devem estar disponíveis no diretório `bin/` dentro do projeto, ou no PATH do sistema.

### Comando de Compilação:

Para compilar o aplicativo, navegue até o diretório raiz do projeto (`yt-downloader`) no terminal e execute o seguinte comando:

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "assets;assets" --add-data "bin;bin" --icon="assets/icon.ico" main.py
```

**Explicação dos parâmetros:**

*   `--noconfirm`: Sobrescreve arquivos de saída existentes sem pedir confirmação.
*   `--onefile`: Cria um único arquivo executável.
*   `--windowed` ou `--noconsole`: Impede que uma janela de console (terminal) seja exibida ao iniciar o aplicativo GUI.
*   `--add-data "assets;assets"`: Inclui o diretório `assets` e seu conteúdo no executável. O primeiro `assets` é o caminho de origem e o segundo `assets` é o nome do diretório dentro do executável.
*   `--add-data "bin;bin"`: Inclui o diretório `bin` (onde FFmpeg/FFprobe devem estar) e seu conteúdo no executável.
*   `--icon="assets/icon.ico"`: Define o ícone do executável usando o arquivo `icon.ico` localizado na pasta `assets`.
*   `main.py`: O arquivo principal do seu aplicativo Python.

### Após a Compilação:

O executável será gerado na pasta `dist/` dentro do diretório raiz do projeto.

### Observações:

*   Certifique-se de que os arquivos `ffmpeg.exe` e `ffprobe.exe` (ou seus equivalentes para outros sistemas operacionais) estejam presentes na pasta `bin/` antes de compilar, caso contrário, o aplicativo pode não funcionar corretamente para downloads de vídeo/áudio.
*   O `yt-dlp` é uma dependência crucial e será incluído automaticamente pelo PyInstaller se estiver no seu ambiente Python. No entanto, o FFmpeg/FFprobe precisam ser adicionados manualmente via `--add-data` ou estarem no PATH do sistema.


