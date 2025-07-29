# Caminhos
$ytDlpDir = "$env:APPDATA\yt-downloader"
$ytDlpPath = Join-Path $ytDlpDir "yt-dlp.exe"
$logFile = Join-Path $ytDlpDir "log.txt"
$dataHoje = Get-Date -Format "yyyy-MM-dd"
# Função de log
function Write-Log {
    param([string]$msg)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "[$timestamp] $msg"
}

# Cria diretório se não existir
if (!(Test-Path $ytDlpDir)) {
    New-Item -Path $ytDlpDir -ItemType Directory | Out-Null
    Write-Log "Criado diretório: $ytDlpDir"
}

# Atualização automática do yt-dlp
function Update-YtDlp {
    Write-Log "Verificando existência do yt-dlp..."
    $needDownload = $true
    if (Test-Path $ytDlpPath) {
        try {
            $localVersion = & $ytDlpPath --version
            $latestVersion = (Invoke-RestMethod "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest").tag_name
            if ($localVersion -eq $latestVersion) {
                Write-Log "yt-dlp está atualizado: $localVersion"
                $needDownload = $false
            } else {
                Write-Log "Atualização disponível: $localVersion → $latestVersion"
            }
        } catch {
            Write-Log "Erro ao verificar versão: $_"
        }
    }

    if ($needDownload) {
        Write-Log "Baixando yt-dlp.exe..."
        try {
            Invoke-WebRequest "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe" -OutFile $ytDlpPath
            Write-Log "yt-dlp.exe baixado com sucesso."
        } catch {
            Write-Log "Erro ao baixar yt-dlp: $_"
            throw "Erro ao baixar yt-dlp."
        }
    }
}
Update-YtDlp

# Caminho de salvamento customizável
$savePath = "$env:USERPROFILE\Downloads"

# Função para baixar vídeo
function Save-YouTubeVideo {
    param([string]$url)

    Write-Log "Iniciando download: $url"

     # Download + merge em MP4 + m4a sem preservar mtime original
     & $ytDlpPath $url `
        --no-playlist `
        --no-mtime `
        --output "$savePath\%(title)s_$dataHoje.%(ext)s" `
        -f "bestvideo[ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]" `
        --merge-output-format mp4

    # Encontra o arquivo baixado (o mais recente com nossa marca de data)
    $arquivo = Get-ChildItem "$savePath\*_$dataHoje.mp4" |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($arquivo) {
        # Ajusta a Data de Modificação para agora
        (Get-Item $arquivo.FullName).LastWriteTime = Get-Date
        Write-Log "Data de modificação ajustada para agora: $($arquivo.FullName)"
    } else {
        Write-Log "Não foi possível localizar o arquivo para ajuste de Data de Modificação."
    }
}

# Laço de download contínuo com cancelamento
while ($true) {
    $url = Read-Host "Cole o link do vídeo (ou digite 'sair' para encerrar)"
    if ($url -eq "sair") {
        Write-Log "Encerrando script por comando do usuário."
        break
    }

    if ($url -match "^https?://") {
        Save-YouTubeVideo -url $url
    } else {
        Write-Host "URL inválida. Tente novamente."
    }
}
