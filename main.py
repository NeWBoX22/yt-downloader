import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import os
import threading
from pathlib import Path

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Criar pasta downloads se não existir
        self.downloads_path = Path("downloads")
        self.downloads_path.mkdir(exist_ok=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="YouTube Video Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL do vídeo
        ttk.Label(main_frame, text="URL do YouTube:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        self.url_entry.bind("<Control-v>", self.paste_from_clipboard)
        self.url_entry.bind("<Control-c>", self.copy_to_clipboard)
        self.url_entry.bind("<Control-x>", self.cut_to_clipboard)
        
        # Botão de colar URL
        paste_btn = ttk.Button(main_frame, text="Colar", command=self.paste_url)
        paste_btn.grid(row=1, column=2, padx=(10, 0), pady=5)
        
        # Pasta de destino
        ttk.Label(main_frame, text="Pasta de destino:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.folder_var = tk.StringVar(value=str(self.downloads_path.absolute()))
        self.folder_entry = ttk.Entry(main_frame, textvariable=self.folder_var, width=50)
        self.folder_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        self.folder_entry.bind("<Control-v>", self.paste_from_clipboard)
        self.folder_entry.bind("<Control-c>", self.copy_to_clipboard)
        self.folder_entry.bind("<Control-x>", self.cut_to_clipboard)
        
        # Botão para escolher pasta
        browse_btn = ttk.Button(main_frame, text="Procurar", command=self.browse_folder)
        browse_btn.grid(row=2, column=2, padx=(10, 0), pady=5)
        
        # Qualidade do vídeo
        ttk.Label(main_frame, text="Qualidade:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="Melhor")
        quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                   values=["Melhor", "Pior", "720p", "480p", "360p"], 
                                   state="readonly", width=20)
        quality_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Botão de download
        self.download_btn = ttk.Button(main_frame, text="Baixar Vídeo", 
                                     command=self.start_download, style="Accent.TButton")
        self.download_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para download")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                    foreground="blue")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Área de log
        ttk.Label(main_frame, text="Log:").grid(row=7, column=0, sticky=(tk.W, tk.N), pady=(10, 5))
        
        # Frame para o log com scrollbar
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar redimensionamento
        main_frame.rowconfigure(8, weight=0) # Log não redimensiona verticalmente
        main_frame.columnconfigure(1, weight=1) # Permite redimensionamento horizontal
        
    def paste_from_clipboard(self, event):
        try:
            widget = event.widget
            clipboard_content = self.root.clipboard_get()
            widget.delete("sel.first", "sel.last")
            widget.insert(tk.INSERT, clipboard_content)
        except tk.TclError:
            pass
        return "break"

    def copy_to_clipboard(self, event):
        try:
            widget = event.widget
            selected_text = widget.get("sel.first", "sel.last")
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
        except tk.TclError:
            pass
        return "break"

    def cut_to_clipboard(self, event):
        try:
            widget = event.widget
            selected_text = widget.get("sel.first", "sel.last")
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
            widget.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        return "break"
            
    def paste_url(self):
        """Cola URL da área de transferência"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_var.set(clipboard_content)
        except tk.TclError:
            pass
            
    def browse_folder(self):
        """Abre diálogo para escolher pasta de destino"""
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)
            
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message, color="blue"):
        """Atualiza o status"""
        self.status_var.set(message)
        self.status_label.configure(foreground=color)
        
    def progress_hook(self, d):
        """Hook para atualizar progresso do download"""
        if d["status"] == "downloading":
            if "total_bytes" in d and d["total_bytes"]:
                percent = (d["downloaded_bytes"] / d["total_bytes"]) * 100
                self.progress_var.set(percent)
                self.update_status(f"Baixando... {percent:.1f}%")
            elif "_percent_str" in d:
                percent_str = d["_percent_str"].strip("%")
                try:
                    percent = float(percent_str)
                    self.progress_var.set(percent)
                    self.update_status(f"Baixando... {percent:.1f}%")
                except ValueError:
                    pass
        elif d["status"] == "finished":
            self.progress_var.set(100)
            self.update_status("Download concluído!", "green")
            self.log_message(f"Arquivo salvo: {d['filename']}")
            
    def start_download(self):
        """Inicia o download em uma thread separada"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL do YouTube")
            return
            
        # Desabilitar botão durante download
        self.download_btn.configure(state="disabled")
        self.progress_var.set(0)
        self.log_message(f"Iniciando download de: {url}")
        
        # Executar download em thread separada
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()
        
    def download_video(self, url):
        """Baixa o vídeo usando yt-dlp"""
        try:
            output_path = self.folder_var.get()
            
            # Configurações do yt-dlp
            ydl_opts = {
                "format": "best[ext=mp4]/best",  # Preferir MP4
                "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
                "progress_hooks": [self.progress_hook],
                "postprocessors": [{
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }],
                "postprocessor_args": [
                    "-c:v", "libx264",  # Codec de vídeo
                    "-c:a", "aac",      # Codec de áudio AAC
                    "-b:a", "128k",     # Bitrate do áudio
                ],
            }
            
            # Ajustar qualidade se especificada
            quality = self.quality_var.get()
            if quality == "Melhor":
                ydl_opts["format"] = "best[ext=mp4]/best"
            elif quality == "Pior":
                ydl_opts["format"] = "worst[ext=mp4]/worst"
            elif quality.endswith("p"):
                height = quality[:-1]
                ydl_opts["format"] = f"best[height<={height}][ext=mp4]/best[height<={height}]/best[ext=mp4]/best"
                
            self.update_status("Obtendo informações do vídeo...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Obter informações do vídeo
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "Vídeo sem título")
                duration = info.get("duration", 0)
                
                self.log_message(f"Título: {title}")
                if duration:
                    minutes = duration // 60
                    seconds = duration % 60
                    self.log_message(f"Duração: {minutes:02d}:{seconds:02d}")
                
                # Fazer o download
                self.update_status("Baixando vídeo...")
                ydl.download([url])
                
        except Exception as e:
            self.log_message(f"Erro durante o download: {str(e)}")
            self.update_status("Erro no download", "red")
            messagebox.showerror("Erro", f"Falha no download:\n{str(e)}")
        finally:
            # Reabilitar botão
            self.download_btn.configure(state="normal")
            
def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()

