
# YouTube Downloader via PowerShell
> Desenvolvido por NeWBoX22 - Projeto ainda em desenvolvimento

Esse repositório contém um script PowerShell (`script.ps1`) que baixa vídeos do YouTube diretamente para a sua pasta **Downloads**, salvando-os como arquivos MP4 com áudio AAC.

---

## 🔥 Pré‑requisitos

- Windows 10/11  
- PowerShell (versão ≥ 5.1 ou PowerShell 7+)  
- Conexão com internet  
- Permissão para executar scripts locais (caso necessário, abra PowerShell **como Administrador** e digite:  

  ```powershell

  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
---

## 🚀 Como usar

1. **Abra o PowerShell** (não use VS Code integrado, pode interferir no progresso).

2. **Execute o comando** abaixo para baixar e rodar o script diretamente do GitHub (use o link raw do arquivo):

   ```powershell
   irm 'https://raw.githubusercontent.com/NeWBoX22/yt-downloader/main/script.ps1' | iex
   ```

3. **Cole a URL** do vídeo YouTube quando solicitado:

   ```
   Cole o link do vídeo (ou digite 'sair' para encerrar):
   ```

4. Aguarde o **progresso** nativo do yt‑dlp (barra de progresso, fragmentos baixados e taxa de transferência).

5. Ao final, encontre o arquivo em:

   ```
   C:\Users\<SeuUsuario>\Downloads\Nome do Vídeo_YYYY-MM-DD.mp4
   ```

---

## ⚙️ O que o script faz

*  **Baixa** ou **atualiza** automaticamente o `yt-dlp.exe` em `%APPDATA%\yt-downloader\`.
*  Força saída em **MP4** (vídeo MP4 + áudio M4A muxados em container MP4).
*  Adiciona **data de download** (`YYYY-MM-DD`) ao nome do arquivo.
*  Ajusta a **Data de Modificação** do arquivo para o momento exato do download.
*  Exibe o **progresso** padrão do yt‑dlp no console.
*  Registra eventos e erros em `%APPDATA%\yt-downloader\log.txt`.
*  Permite baixar **vários vídeos** em sequência; digite `sair` para encerrar.

---

## 🛡️ Avisos de segurança

* **Ctrl + V não cola** no PowerShell tradicional. Use **botão direito do mouse** ou toque com dois dedos no touchpad para colar.
* Sempre confira o conteúdo do script antes de rodá-lo via `irm | iex`.
* Scripts remotos são poderosos, mas podem ser perigosos se de fontes não confiáveis.

---

## 📝 Licença

Este projeto está disponível sob a [MIT License](LICENSE). Sinta‑se à vontade para clonar, modificar e usar conforme sua necessidade.

---


