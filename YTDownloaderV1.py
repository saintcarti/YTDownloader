from tkinter import *
from pytube import YouTube
from tkinter import messagebox
from moviepy.editor import VideoFileClip
import os
import re

def clean_file(filename):
    cleaned_filename = re.sub(r'[\\/*?:<>|]', '', filename)
    cleaned_filename = re.sub(r'\s+', '_', cleaned_filename)
    return cleaned_filename

def download_video(merge_audio=False, numero=None):
    try:
        video_link = str(link.get()).strip()

        if not video_link:
            messagebox.showwarning('Advertencia', 'No has ingresado ningún enlace.')
            return
            
        url = YouTube(video_link)
        url.check_availability()
        video = url.streams.get_highest_resolution()

        if video is None:
            raise ValueError("No se encontró una resolución máxima para el video.")

        user_home_dir = os.path.expanduser("~")
        folder_path = os.path.join(user_home_dir, "Desktop", "Videos_descargados")
        folder_path = os.path.normpath(folder_path)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        base_name = "audio" if merge_audio else "video"
        if numero is None:
            numero = 0
            while True:
                filename = f"{base_name}{numero}.mp4" if merge_audio else f"{base_name}{numero}.mp4"
                full_file_path = os.path.join(folder_path, filename)
                if not os.path.exists(full_file_path):
                    break
                numero += 1

        filename = f"{base_name}{numero}.mp4" if merge_audio else f"{base_name}{numero}.mp4"
        full_file_path = os.path.join(folder_path, filename)

        video.download(output_path=folder_path, filename=filename)

        if merge_audio:
            convert_to_wav(full_file_path)
            os.remove(full_file_path)

        messagebox.showinfo('Hecho', f'El {"audio" if merge_audio else "video"} ha sido descargado con éxito.')
        Label(root, text='Descargado', font='arial 13 bold', bg='#AACDE2', fg='#B57199').place(x=350, y=210)

    except Exception as e:
        messagebox.showerror('Error', str(e))


def downloader_mp4():
    global numero_video
    download_video(merge_audio=False, numero=numero_video)
    numero_video += 1

def downloader_wav():
    global numero_audio
    download_video(merge_audio=True, numero=numero_audio)
    numero_audio += 1

def convert_to_wav(video_path):
    try:
        video_base_name, video_extension =os.path.splitext(video_path)
        audio_path = video_base_name + ".wav"
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)

        audio_clip.close()
        video_clip.close()
        messagebox.showinfo('Hecho','El audio ha sido convertido a wav con exito')
    except Exception as e:
        messagebox.showerror('Error',f'Error al convertir el audio a WAV')
        
def ExitProgram():
    root.quit()

numero_audio = 0
numero_video = 0

root = Tk()
root.geometry('500x300')
root.resizable(0, 0)
root.title('YT Downloader by:Xavier')
root.configure(bg='#AACDE2')

Label(root, text='Descarga tus videos ', font='arial 20 bold', bg='#AACDE2').place(x=90, y=30)

link = StringVar()
Label(root, text='Pega el link aquí:  ', font='arial 12', bg='#AACDE2').place(x=190, y=90)
link_enter = Entry(root, width=70, textvariable=link).place(x=32, y=120)

Button(root, text='Descargar como MP4', font='arial 13 bold italic', bg='#B57199', padx=2, command=downloader_mp4).place(x=150, y=180)
Button(root, text='Descargar como WAV', font='arial 13 bold italic', bg='#B57199', padx=2, command=downloader_wav).place(x=150, y=230)
Button(root, text='Salir', font='arial 13 bold italic', bg='#B57199', padx=2, command=ExitProgram).place(x=350, y=260)

root.mainloop()
