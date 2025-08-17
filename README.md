# YouTube Downloader


## Visão Geral

O **YouTube Downloader** é um aplicativo de desktop robusto e fácil de usar, desenvolvido em Python com a poderosa biblioteca PySide6 (Qt for Python). Ele permite que você baixe vídeos e áudios do YouTube e de outras plataformas de vídeo suportadas diretamente para o seu computador, com opções de formato e qualidade personalizáveis. Com uma interface gráfica nativa e intuitiva, este software oferece uma experiência de usuário fluida e eficiente para todas as suas necessidades de download de mídia.

## Funcionalidades Principais

- **Download Versátil**: Baixe vídeos em formatos populares como MP4 e MKV, ou extraia apenas o áudio em MP3 e M4A.
- **Seleção de Qualidade**: Escolha entre diversas opções de qualidade de vídeo (1080p, 720p, 480p, etc.) e áudio, ou deixe o aplicativo selecionar a melhor qualidade disponível.
- **Interface Intuitiva (GUI)**: Desenvolvido com PySide6, oferece uma experiência de usuário nativa e responsiva em sistemas operacionais Windows, macOS e Linux.
- **Gerenciamento de Downloads**: Acompanhe o progresso do download com uma barra de progresso em tempo real e visualize um log detalhado de todas as operações.
- **Histórico de Downloads**: Mantenha um registro dos seus downloads anteriores para fácil referência.
- **Configurações Persistentes**: Suas preferências de pasta de destino e histórico são salvas automaticamente.
- **Cancelamento de Download**: Capacidade de cancelar downloads em andamento a qualquer momento.
- **Acesso Rápido**: Botões dedicados para limpar o log, abrir a pasta de downloads e visualizar informações sobre o aplicativo e suas configurações.

## Tecnologias Utilizadas

Este projeto é construído sobre uma base tecnológica sólida, garantindo desempenho e compatibilidade:

- **Python 3.x**: A linguagem de programação principal que orquestra todas as operações.
- **PySide6**: A biblioteca oficial do Qt para Python, utilizada para construir a interface gráfica do usuário, proporcionando uma experiência nativa e multiplataforma.
- **yt-dlp**: Uma ferramenta de linha de comando altamente flexível e poderosa para download de vídeos de centenas de sites, incluindo o YouTube. É o motor por trás das capacidades de download do aplicativo.
- **FFmpeg**: Uma solução completa e multiplataforma para gravar, converter e fazer streaming de áudio e vídeo. Essencial para o processamento de mídia, como extração de áudio e conversão de formatos.
- **pyperclip**: Uma biblioteca Python para copiar e colar texto na área de transferência, utilizada para facilitar a inserção de URLs.
- **threading**: Módulo padrão do Python para lidar com operações em segundo plano, garantindo que a interface do usuário permaneça responsiva durante os downloads.

## Como Instalar e Rodar

Siga os passos abaixo para configurar e executar o YouTube Downloader Pro - Qt Edition em seu sistema.

### Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados:

- **Python 3.x**: Baixe e instale a versão mais recente do Python em [python.org](https://www.python.org/downloads/).
- **FFmpeg**: **Altamente recomendado** para todas as funcionalidades de download e conversão de áudio/vídeo. Baixe-o em [ffmpeg.org/download.html](https://ffmpeg.org/download.html) e certifique-se de adicioná-lo ao PATH do seu sistema. Isso permite que o `yt-dlp` utilize o FFmpeg para processar os arquivos de mídia.

### Instalação

1. **Clone o Repositório**:
   Abra seu terminal ou prompt de comando e clone o projeto do GitHub:
   ```bash
   git clone https://github.com/seu-usuario/youtube-downloader-qt.git
   cd youtube-downloader-qt
   ```
   *(Substitua `seu-usuario` pelo seu nome de usuário do GitHub e `youtube-downloader-qt` pelo nome do seu repositório, se for diferente.)*

2. **Crie e Ative um Ambiente Virtual** (Recomendado):
   É uma boa prática isolar as dependências do projeto em um ambiente virtual.
   ```bash
   python -m venv venv
   ```
   Ative o ambiente virtual:
   - **No Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **No macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Instale as Dependências Python**:
   Com o ambiente virtual ativado, instale as bibliotecas necessárias. Você pode usar o arquivo `requirements.txt` (se disponível) ou instalá-las manualmente:
   ```bash
   # Se você tiver um arquivo requirements.txt
   pip install -r requirements.txt
   
   # Ou instale manualmente
   pip install PySide6 yt-dlp pyperclip
   ```

### Execução

Após a instalação das dependências, você pode iniciar o aplicativo:

```bash
python main_qt.py
```

Isso abrirá a janela principal do YouTube Downloader Pro - Qt Edition.

## Estrutura do Projeto

- `main_qt.py`: O arquivo principal que contém a lógica da interface gráfica e a integração com as funcionalidades de download.
- `debug_qt.log`: Um arquivo de log gerado pela aplicação para depuração e registro de operações.
- `downloader_config.json`: Um arquivo JSON que armazena as configurações do usuário, como a pasta de destino e o histórico de downloads.
- `downloads/`: O diretório padrão onde os arquivos baixados serão salvos. Este diretório é criado automaticamente se não existir.

## Contribuição

Contribuições são **muito bem-vindas**! Se você tiver ideias para novas funcionalidades, melhorias de código, ou encontrar algum bug, sinta-se à vontade para:

1.  **Abrir uma Issue**: Descreva detalhadamente o problema ou a sugestão.
2.  **Criar um Pull Request**: Faça um fork do repositório, implemente suas mudanças e envie um pull request. Por favor, siga as boas práticas de codificação e inclua testes, se aplicável.

## Licença

Este projeto está licenciado sob a [Nome da Licença, por exemplo, Licença MIT]. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido com ❤️ por NeWBoX22**


