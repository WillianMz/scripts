import yt_dlp

def baixar_audio(url):
    opcoes = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    link = input("Cole o link do vídeo do YouTube: ")
    baixar_audio(link)
