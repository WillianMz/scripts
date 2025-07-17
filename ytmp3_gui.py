import tkinter as tk
from tkinter import messagebox
import yt_dlp

def baixar_audio():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Cole um link do YouTube.")
        return

    opcoes = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        messagebox.showinfo("Sucesso", "Download concluído!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")

# Interface gráfica
janela = tk.Tk()
janela.title("YouTube MP3 Downloader")
janela.geometry("400x150")
janela.resizable(False, False)

tk.Label(janela, text="Cole o link do vídeo do YouTube:").pack(pady=10)
entrada_url = tk.Entry(janela, width=50)
entrada_url.pack(pady=5)

botao_baixar = tk.Button(janela, text="Baixar MP3", command=baixar_audio)
botao_baixar.pack(pady=10)

janela.mainloop()
