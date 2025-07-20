# Caminho para yt-dlp
$ytDlpPath = "$env:APPDATA\yt-downloader\yt-dlp.exe"

# Criação da pasta, se não existir
if (-not (Test-Path $ytDlpPath)) {
    Write-Host "Baixando yt-dlp.exe na pasta %APPDATA%\yt-downloader..."
    $ytDlpFolder = Split-Path $ytDlpPath
    New-Item -ItemType Directory -Path $ytDlpFolder -Force | Out-Null
    Invoke-WebRequest -Uri "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe" -OutFile $ytDlpPath
}

# Pasta Downloads
$downloadsPath = [Environment]::GetFolderPath("UserProfile")
$savePath = Join-Path $downloadsPath "Downloads"


function Test-YouTubeLink($url) {
    return $url -match '^https?://(www\.)?(youtube\.com|youtu\.be)/'
}

function Get-YouTubeVideoData($url) {
    $json = & $ytDlpPath $url --print-json --skip-download 2>$null
    if (-not $json) { return $null }
    return $json | ConvertFrom-Json
}

function Save-YouTubeVideo($url) {
    try {
        if (-not (Test-YouTubeLink $url)) {
            Write-Warning "Link inválido. Insira uma URL do YouTube válida."
            return
        }

        $dados = Get-YouTubeVideoData $url
        if (-not $dados) {
            Write-Warning "Não foi possível obter informações do vídeo."
            return
        }

        $titulo = $dados.title -replace '[\\\/:*?"<>|]', ''
        $dataHoje = Get-Date -Format "yyyy-MM-dd"
        $nomeArquivoFinal = "${titulo}_$dataHoje.mp4"
        $caminhoCompleto = Join-Path $savePath $nomeArquivoFinal

        & $ytDlpPath $url `
            -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4" `
            --merge-output-format mp4 `
            -o "$caminhoCompleto" 2>&1 | Out-Null

        if (Test-Path $caminhoCompleto) {
            # Ajustar a data de modificação para a data de hoje
            (Get-Item $caminhoCompleto).LastWriteTime = Get-Date
            Write-Host "Vídeo salvo em: $caminhoCompleto"
        } else {
            Write-Warning "Falha ao baixar o vídeo."
        }

    } catch {
        Write-Error "Ocorreu um erro: $_"
    }
}

do {
    Write-Host "`nCole o link do vídeo do YouTube:"
    $url = Read-Host
    if ($url) {
        Save-YouTubeVideo $url
    }
    $continuar = Read-Host "`nDeseja baixar outro vídeo? (s/n)"
} while ($continuar -match '^(s|sim)$')
