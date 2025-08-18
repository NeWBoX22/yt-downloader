
import sys
import asyncio
import os
import time
import threading
import json
from pathlib import Path
from datetime import datetime
import yt_dlp
import traceback

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar, QTextEdit,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QFont

import logging
logging.basicConfig(filename='debug_qt.log', level=logging.DEBUG, filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')

class WorkerSignals(QObject):
    # Define signals for communication from worker thread to main thread
    update_status = Signal(str, int)
    log_message = Signal(str)
    error_dialog = Signal(str, str)
    info_dialog = Signal(str, str)
    video_info_updated = Signal(str)

class YouTubeDownloaderQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.downloads_path = Path("downloads")
        self.downloads_path.mkdir(exist_ok=True)
        self.config_file = Path("downloader_config.json")
        self.download_history = []
        self.is_downloading = False
        self.download_thread = None
        self.cancel_event = threading.Event()
        self.load_config()

        self.signals = WorkerSignals()
        self.signals.update_status.connect(self._update_status_ui)
        self.signals.log_message.connect(self._update_log_text)
        self.signals.error_dialog.connect(self._show_error_dialog)
        self.signals.info_dialog.connect(self._show_info_dialog)
        self.signals.video_info_updated.connect(self._update_video_info_label)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Título
        title_label = QLabel("YouTube Downloader")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Seção URL
        url_box = QHBoxLayout()
        url_label = QLabel("URL:")
        url_label.setFixedWidth(80)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole aqui a URL do vídeo do YouTube...")
        paste_btn = QPushButton("Colar")
        paste_btn.setFixedWidth(80)
        paste_btn.clicked.connect(self.paste_url)

        url_box.addWidget(url_label)
        url_box.addWidget(self.url_input)
        url_box.addWidget(paste_btn)
        main_layout.addLayout(url_box)

        # Seção pasta de destino
        folder_box = QHBoxLayout()
        folder_label = QLabel("Pasta:")
        folder_label.setFixedWidth(80)
        self.folder_input = QLineEdit()
        self.folder_input.setText(str(self.downloads_path.absolute()))
        browse_btn = QPushButton("Procurar")
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self.browse_folder)

        folder_box.addWidget(folder_label)
        folder_box.addWidget(self.folder_input)
        folder_box.addWidget(browse_btn)
        main_layout.addLayout(folder_box)

        # Configurações de download
        config_box = QHBoxLayout()

        type_label = QLabel("Tipo:")
        type_label.setFixedWidth(80)
        self.download_type_selection = QComboBox()
        self.download_type_selection.addItems(["Vídeo (MP4)", "Áudio (MP3)", "Áudio (M4A)", "Vídeo + Áudio (MKV)"])
        self.download_type_selection.setCurrentText("Vídeo (MP4)")
        self.download_type_selection.setFixedWidth(150)
        self.download_type_selection.currentIndexChanged.connect(self.update_quality_options)

        quality_label = QLabel("Qualidade:")
        quality_label.setFixedWidth(80)
        self.quality_selection = QComboBox()
        self.quality_selection.addItems(["Melhor", "Pior", "1080p", "720p", "480p", "360p", "240p"])
        self.quality_selection.setCurrentText("720p")
        self.quality_selection.setFixedWidth(100)

        config_box.addWidget(type_label)
        config_box.addWidget(self.download_type_selection)
        config_box.addWidget(quality_label)
        config_box.addWidget(self.quality_selection)
        config_box.addStretch(1) # Adiciona um espaço flexível para empurrar os widgets para a esquerda
        main_layout.addLayout(config_box)

        # Botões de ação
        buttons_box = QHBoxLayout()

        self.download_btn = QPushButton("Baixar")
        self.download_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        self.download_btn.clicked.connect(self.start_download)

        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setStyleSheet("background-color: #f44336; color: white;")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_download)

        history_btn = QPushButton("Histórico")
        history_btn.setStyleSheet("background-color: #2196F3; color: white;")
        history_btn.clicked.connect(self.show_history)

        buttons_box.addWidget(self.download_btn)
        buttons_box.addWidget(self.cancel_btn)
        buttons_box.addWidget(history_btn)
        main_layout.addLayout(buttons_box)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        main_layout.addWidget(self.progress_bar)

        # Status
        self.status_label = QLabel("Pronto para download")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #2196F3;")
        main_layout.addWidget(self.status_label)

        # Área de log
        log_label = QLabel("Log de operações:")
        log_font = QFont()
        log_font.setBold(True)
        log_label.setFont(log_font)
        main_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlainText("Aplicativo iniciado. Pronto para downloads.\n")
        self.log_text.setFixedHeight(150)
        main_layout.addWidget(self.log_text)

        # Botões extras
        extra_buttons_box = QHBoxLayout()

        clear_log_btn = QPushButton("Limpar Log")
        clear_log_btn.clicked.connect(self.clear_log)

        open_folder_btn = QPushButton("Abrir Pasta")
        open_folder_btn.clicked.connect(self.open_downloads_folder)

        about_btn = QPushButton("Sobre")
        about_btn.clicked.connect(self.show_about)

        #config_btn = QPushButton("Configurações")
        #config_btn.clicked.connect(self.show_config)

        extra_buttons_box.addWidget(clear_log_btn)
        extra_buttons_box.addWidget(open_folder_btn)
        extra_buttons_box.addWidget(about_btn)
        # extra_buttons_box.addWidget(config_btn) Temporariamente desativado
        self.update_quality_options()
        main_layout.addLayout(extra_buttons_box)

    def load_config(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.downloads_path = Path(config.get('downloads_path', 'downloads'))
                    self.download_history = config.get('history', [])
        except Exception as e:
            logging.exception("Erro ao carregar configurações: %s", e)
            QMessageBox.critical(self, "Erro", f"Erro ao carregar configurações: {e}")

    def save_config(self):
        try:
            config = {
                'downloads_path': str(self.downloads_path),
                'history': self.download_history[-50:]
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.exception("Erro ao salvar configurações: %s", e)
            QMessageBox.critical(self, "Erro", f"Erro ao salvar configurações: {e}")

    def _update_status_ui(self, message, progress=None):
        self.status_label.setText(message)
        if progress is not None:
            self.progress_bar.setValue(progress)

    def _update_log_text(self, text):
        self.log_text.append(text.strip())
        # QTextEdit scrolls automatically to the end when append is used

    def _show_error_dialog(self, title, message):
        QMessageBox.critical(self, title, message)

    def _show_info_dialog(self, title, message):
        QMessageBox.information(self, title, message)

    def _update_video_info_label(self, info_text):
        self.status_label.setText(info_text)

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.signals.log_message.emit(f"[{timestamp}] {message}")

    def update_status(self, message, progress=None):
        self.signals.update_status.emit(message, progress)

    def _get_video_info_background(self, url):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Título não disponível')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Canal não disponível')
                view_count = info.get('view_count', 0)

                if duration:
                    minutes = duration // 60
                    seconds = duration % 60
                    duration_str = f"{minutes:02d}:{seconds:02d}"
                else:
                    duration_str = "Duração não disponível"

                info_text = f"Título: {title}\nCanal: {uploader}\nDuração: {duration_str}\nVisualizações: {view_count:,}"
                self.signals.video_info_updated.emit(info_text)
                self.signals.update_status.emit("Informações obtidas", self.progress_bar.value())

        except Exception as e:
            tb = traceback.format_exc()
            logging.exception("Erro ao obter informações do vídeo: %s", e)
            self.signals.error_dialog.emit("Erro", f"Erro ao obter informações: {str(e)}\n{tb}")
            self.signals.update_status.emit("Erro ao obter informações", self.progress_bar.value())

    def paste_url(self):
        try:
            import pyperclip
            clipboard_content = pyperclip.paste()
            self.url_input.setText(clipboard_content)
            self.log_message("URL colada da área de transferência")
        except ImportError:
            self.signals.info_dialog.emit("Erro", "pyperclip não instalado")
        except Exception as e:
            self.signals.error_dialog.emit("Erro", f"Erro ao colar: {str(e)}")

        self.update_status("Obtendo informações...")
        # Inicia a busca de informações em segundo plano
        threading.Thread(target=self._get_video_info_background, args=(self.url_input.text().strip(),)).start()

    def browse_folder(self):
        try:
            folder_path = QFileDialog.getExistingDirectory(
                self,
                "Escolher pasta de destino",
                self.folder_input.text()
            )
            if folder_path:
                self.folder_input.setText(folder_path)
                self.log_message(f"Pasta selecionada: {folder_path}")
        except Exception as e:
            self.signals.error_dialog.emit("Erro", f"Erro ao selecionar pasta: {str(e)}")

    def clear_log(self):
        self.log_text.setPlainText("Log limpo.\n")

    def open_downloads_folder(self):
        folder_path = self.folder_input.text()
        try:
            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":  # macOS
                os.system(f"open \"{folder_path}\"")
            else:  # Linux
                os.system(f"xdg-open \"{folder_path}\"")
            self.log_message(f"Pasta aberta: {folder_path}")
        except Exception as e:
            self.signals.error_dialog.emit("Erro", f"Erro ao abrir pasta: {str(e)}")

    def show_about(self):
        about_text = """YouTube Downloader\n\nVersão: Alpha\nDesenvolvido com: Python + PySide6 + yt-dlp\n\nFuncionalidades:\n• Download de vídeos em MP4/MKV\n• Download de áudio em MP3/M4A\n• Múltiplas qualidades\n• Interface nativa multiplataforma\n• Log detalhado de operações\n• Histórico de downloads\n\nBibliotecas utilizadas:\n• PySide6 - Interface gráfica nativa\n• yt-dlp - Download de vídeos\n• FFmpeg - Processamento de mídia"""
        self.signals.info_dialog.emit("Sobre", about_text)

    def show_config(self):
        config_text = f"""Configurações Atuais:\n\nPasta de downloads: {self.downloads_path}\nTotal de downloads no histórico: {len(self.download_history)}\n\nPara alterar as configurações, use os campos da interface principal."""
        self.signals.info_dialog.emit("Configurações", config_text)

    def show_history(self):
        if not self.download_history:
            self.signals.info_dialog.emit("Histórico", "Nenhum download realizado ainda.")
            return

        history_text = "Histórico de Downloads:\n\n"
        for item in reversed(self.download_history[-10:]):
            history_text += f"[{item['date']}] {item['title']} - {item['format']}\n"

        self.signals.info_dialog.emit("Histórico", history_text)

    def add_to_history(self, title, format_type):
        item = {
            'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'title': title,
            'format': format_type
        }
        self.download_history.append(item)
        self.save_config()

    def update_quality_options(self):
        download_type = self.download_type_selection.currentText()
        self.quality_selection.clear() # Limpa as opções atuais

        if "Vídeo" in download_type:
            # Opções para formatos de vídeo
            self.quality_selection.addItems(["Melhor", "Pior", "1080p", "720p", "480p", "360p", "240p"])
            self.quality_selection.setCurrentText("720p")
        elif "Áudio" in download_type:
            # Opções para formatos de áudio (bitrate)
            self.quality_selection.addItems(["Melhor (320k)", "Padrão (192k)", "Boa (128k)", "Pior (64k)"])
            self.quality_selection.setCurrentText("Padrão (192k)")

    def start_download(self):
        if self.download_thread and self.download_thread.is_alive():
            self.signals.error_dialog.emit("Erro", "Um download ainda está em andamento")
            return

        url = self.url_input.text().strip()
        if not url:
            self.signals.error_dialog.emit("Erro", "Por favor, insira uma URL do YouTube")
            return

        if self.is_downloading:
            self.signals.error_dialog.emit("Erro", "Download já em andamento")
            return

        self.download_btn.setEnabled(False)
        self.download_btn.setText("Baixando...")
        self.cancel_btn.setEnabled(True)
        self.is_downloading = True
        self.progress_bar.setValue(0)

        # Iniciar o download em uma thread separada
        self.cancel_event.clear()
        self.download_thread = threading.Thread(target=self._do_download, args=(url,))
        self.download_thread.start()

    def cancel_download(self):
        if self.is_downloading:
            self.cancel_event.set()
            self.log_message("Solicitação de cancelamento enviada.")
            self.update_status("Cancelando download...")

    def _do_download(self, url):
        # Esta função roda em uma thread separada
        try:
            self.log_message(f"Iniciando download de: {url}")
            self.update_status("Iniciando download...", 0)

            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': str(self.downloads_path / '%(title)s.%(ext)s'),
                'progress_hooks': [self._download_progress_hook],
                'merge_output_format': 'mkv',
                'postprocessors': [],
            }

            # ESTE É O NOVO BLOCO DE CÓDIGO PARA INSERIR NO LUGAR DO ANTIGO

            download_type = self.download_type_selection.currentText()
            quality = self.quality_selection.currentText()

            if download_type == "Áudio (MP3)":
                ydl_opts['format'] = 'bestaudio/best'
                # Extrai o bitrate da string de qualidade, ex: "Padrão (192k)" -> "192"
                audio_bitrate = quality.split('(')[-1].replace('k)', '') if '(' in quality else '192'
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': audio_bitrate,
                })
            elif download_type == "Áudio (M4A)":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                })
            elif download_type == "Vídeo (MP4)":
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                ydl_opts['merge_output_format'] = 'mp4'
            elif download_type == "Vídeo + Áudio (MKV)":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mkv'

            if quality not in ["Melhor", "Pior"] and "k)" not in quality: # Garante que só se aplica a vídeo
                if download_type.startswith("Vídeo"):
                    # A lógica para vídeo permanece a mesma, com a melhoria do <=
                    resolution = quality.replace('p', '')
                    ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]'
                # Não é necessário um 'else' aqui, pois a qualidade do áudio já foi tratada acima


            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'unknown_title')
                
                if self.cancel_event.is_set():
                    self.log_message("Download cancelado pelo usuário.")
                    self.update_status("Download cancelado.", 0)
                    return

                ydl.download([url])

            self.log_message(f"Download concluído: {title}")
            self.update_status("Download concluído!", 100)
            self.add_to_history(title, download_type)

        except yt_dlp.DownloadError as e:
            error_msg = f"Erro no download: {e}"
            logging.exception(error_msg)
            self.signals.error_dialog.emit("Erro de Download", error_msg)
            self.update_status("Erro no download.", 0)
        except Exception as e:
            tb = traceback.format_exc()
            error_msg = f"Ocorreu um erro inesperado: {e}"
            logging.exception(error_msg)
            self.signals.error_dialog.emit("Erro", f"{error_msg}\n{tb}")
            self.signals.update_status.emit("Erro inesperado.", 0)
        finally:
            self.is_downloading = False
            self.signals.update_status.emit("Pronto para download", 0)
            self.download_btn.setEnabled(True)
            self.download_btn.setText("Baixando")
            self.cancel_btn.setEnabled(False)
            self.cancel_event.clear()

    def _download_progress_hook(self, d):
        if self.cancel_event.is_set():
            raise yt_dlp.DownloadError("Download cancelado pelo usuário")

        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes')
            if total_bytes and downloaded_bytes:
                progress = int(downloaded_bytes / total_bytes * 100)
                self.signals.update_status.emit(f"Baixando: {d['_percent_str']} de {d['_total_bytes_str']} @ {d['_speed_str']}", progress)
            else:
                self.signals.update_status.emit(f"Baixando: {d['_percent_str']} @ {d['_speed_str']}", self.progress_bar.value())
        elif d['status'] == 'finished':
            self.signals.update_status.emit("Processando...", 100)
            self.log_message(f"Concluído: {d['filename']}")
        elif d['status'] == 'error':
            self.signals.update_status.emit("Erro no download.", 0)
            self.log_message(f"Erro: {d['filename']}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloaderQt()
    window.show()
    sys.exit(app.exec())

