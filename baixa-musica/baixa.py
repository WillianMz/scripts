import sys
import os
import threading
import yt_dlp
import tkinter as tk
from tkinter import ttk, messagebox

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

ffmpeg_path = os.path.join(base_path, "ffmpeg", "bin")

def format_tempo(segundos):
    if segundos is None:
        return "??:??"
    m, s = divmod(int(segundos), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:d}h{m:02d}m{s:02d}s"
    else:
        return f"{m:02d}m{s:02d}s"

def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded_bytes = d.get('downloaded_bytes', 0)
        speed = d.get('speed') or 0
        eta = d.get('eta')

        if total_bytes > 0:
            porcentagem = downloaded_bytes / total_bytes * 100
            progress_var.set(porcentagem)
            velocidade_str = f"{speed / 1024:.1f} KiB/s" if speed else "Calculando..."
            eta_str = format_tempo(eta)
            status_label.config(text=f"Baixando... {porcentagem:.1f}%  {velocidade_str}  ETA: {eta_str}")
    elif d['status'] == 'finished':
        progress_var.set(100)
        status_label.config(text="Download concluído, convertendo...")

def baixar_audio_thread(url):
    opcoes = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': False,
        'progress_hooks': [progress_hook],
    }
    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        status_label.config(text="Download e conversão concluídos com sucesso!")
        messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
    except Exception as e:
        status_label.config(text="Erro durante o download.")
        messagebox.showerror("Erro", f"Erro durante o download:\n{e}")
    finally:
        botao.config(state=tk.NORMAL)  # Reabilita o botão quando termina

def iniciar_download():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Cole um link do YouTube.")
        return
    progress_var.set(0)
    status_label.config(text="Iniciando download...")
    botao.config(state=tk.DISABLED)  # Desabilita o botão no início
    thread = threading.Thread(target=baixar_audio_thread, args=(url,), daemon=True)
    thread.start()

# GUI
janela = tk.Tk()
janela.title("YouTube MP3 Downloader")
janela.geometry("470x240")
janela.resizable(False, False)

tk.Label(janela, text="Cole o link do vídeo ou playlist do YouTube:").pack(pady=10)
entrada_url = tk.Entry(janela, width=65)
entrada_url.pack(pady=5)

botao = tk.Button(janela, text="Baixar MP3", command=iniciar_download)
botao.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(janela, length=430, variable=progress_var, maximum=100)
progress_bar.pack(pady=5)

status_label = tk.Label(janela, text="", font=("Arial", 10))
status_label.pack(pady=5)

janela.mainloop()
