<h1 align="center">YouTube Downloader</h2>

<div align="center">

![GitHub Release](https://img.shields.io/github/v/release/NeWBoX22/yt-downloader)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/NeWBoX22/yt-downloader/main)
![GitHub top language](https://img.shields.io/github/languages/top/NeWBoX22/yt-downloader)
![License](https://img.shields.io/github/license/NeWBoX22/yt-downloader)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/NeWBoX22/yt-downloader/total)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/NeWBoX22/yt-downloader)
![Status](https://img.shields.io/badge/status-active-brightgreen)

</div>

## Visão Geral

O **YouTube Downloader** é um aplicativo de desktop robusto e fácil de usar que permite baixar vídeos e áudios do YouTube e de outras plataformas diretamente para o seu computador. Com uma interface gráfica nativa e intuitiva, este software oferece uma experiência fluida e eficiente, com opções de formato e qualidade personalizáveis.

##  Funcionalidades Principais

- **Download Versátil**: Baixe vídeos em formatos populares como MP4 e MKV, ou extraia apenas o áudio em MP3 e M4A.
- **Seleção de Qualidade Dinâmica**: Escolha entre diversas opções de qualidade de vídeo (1080p, 720p, etc.) e áudio (320k, 192k, etc.), ou deixe o aplicativo selecionar a melhor qualidade disponível.
- **Interface Intuitiva (GUI)**: Desenvolvido com PySide6 (Qt for Python), oferece uma experiência de usuário nativa e responsiva.
- **Totalmente Portátil**: A versão para Windows é um executável único (`.exe`) que já inclui todas as dependências. **Não é necessário instalar Python ou FFmpeg.**
- **Gerenciamento de Downloads**: Acompanhe o progresso com uma barra em tempo real e visualize um log detalhado de todas as operações.
- **Histórico e Configurações**: Suas preferências de pasta e o histórico de downloads são salvos automaticamente.

---

## 🚀 Como Usar (Versão para Windows)

A maneira mais fácil de usar o aplicativo, sem precisar instalar nada.

1.  **Acesse a página de [Releases](https://github.com/NeWBoX22/yt-downloader/releases )**.
2.  Na seção **Assets** da versão mais recente, baixe o arquivo `.exe`.
3.  **Execute o arquivo baixado.** E pronto! O aplicativo está pronto para ser usado.

---

##  Para Desenvolvedores: Rodando a Partir do Código-Fonte

Se você deseja executar o projeto a partir do código-fonte para contribuir ou fazer modificações, siga os passos abaixo.

### Pré-requisitos

- **Python 3.x**: Baixe e instale a versão mais recente em [python.org](https://www.python.org/downloads/ ).
- **FFmpeg**: Baixe-o em [ffmpeg.org/download.html](https://ffmpeg.org/download.html ) e coloque o `ffmpeg.exe` dentro da pasta `bin/` na raiz do projeto.

### Instalação

1.  **Clone o Repositório**:
    ```bash
    git clone https://github.com/NeWBoX22/yt-downloader.git
    cd yt-downloader
    ```

2.  **Crie e Ative um Ambiente Virtual** (Recomendado ):
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Instale as Dependências**:
    ```bash
    pip install PySide6 yt-dlp pyperclip
    ```

### Execução

Com o ambiente virtual ativado, inicie o aplicativo:
```
python main.py
```

## Tecnologias Utilizadas
  - Python 3.x: A linguagem de programação principal.
  - PySide6: Biblioteca oficial do Qt para Python, usada para construir a interface gráfica.
  - yt-dlp: O motor por trás das capacidades de download de vídeos.
  - FFmpeg: Essencial para o processamento de mídia, como extração de áudio e conversão de formatos.

## Contribuição
   Contribuições são muito bem-vindas! Se você tiver ideias para novas funcionalidades, melhorias de código, ou encontrar algum bug, sinta-se à vontade para abrir uma Issue ou criar um Pull Request.

## Licença
  - Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
---

Desenvolvido com ❤️ por NeWBoX22
