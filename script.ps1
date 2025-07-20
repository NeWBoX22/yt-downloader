# Define pasta do yt-dlp no %APPDATA%
$ytDlpFolder = Join-Path $env:APPDATA "yt-downloader"
New-Item -ItemType Directory -Path $ytDlpFolder -Force | Out-Null
$ytDlpPath = Join-Path $ytDlpFolder "yt-dlp.exe"

# Baixa yt-dlp se ainda não existir
if (!(Test-Path $ytDlpPath)) {
    Write-Host "Baixando yt-dlp.exe..."
    Invoke-WebRequest -Uri "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe" -OutFile $ytDlpPath
}

# Define pasta de destino (Downloads)
$downloadsPath = [Environment]::GetFolderPath("UserProfile")
$savePath = Join-Path $downloadsPath "Downloads"

# Início
Clear-Host
Write-Host "`nYouTube Downloader via PowerShell`n"
Write-Host "⚠️  AVISO: Ctrl + V NÃO funciona aqui."
Write-Host "Use o botão direito do mouse para colar, ou toque com dois dedos no touchpad.`n"

# Entrada do link
$url = Read-Host "Cole o link do vídeo do YouTube"

# Data atual formatada
$dataHoje = Get-Date -Format "yyyy-MM-dd"

# Monta o nome do arquivo
$filenameTemplate = "%(title)s_$dataHoje.%(ext)s"

# Executa o download
& $ytDlpPath $url `
    --output "$savePath\$filenameTemplate" `
    -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4" `
    --merge-output-format mp4

# Procura o arquivo baixado
$info = & $ytDlpPath $url --print "%(title)s"
$title = $info.Trim()
$finalFileName = "$title" + "_$dataHoje.mp4"
$finalFile = Join-Path $savePath $finalFileName


# Define data de modificação (opcional)
if (Test-Path $finalFile) {
    (Get-Item $finalFile).LastWriteTime = Get-Date
    Write-Host "`n✅ Download concluído:"
    Write-Host "$finalFile"
} else {
    Write-Host "`n⚠️  Não foi possível encontrar o arquivo baixado."
}
