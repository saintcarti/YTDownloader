from tkinter import *
from pytube import YouTube
from tkinter import messagebox
from moviepy.editor import VideoFileClip
import os
import re

numero_audio = 0
numero_video = 0

root = Tk()
root.geometry('500x300')
root.resizable(0,0)
root.title('YT Downloader by:Xavier')
root.configure(bg='#AACDE2')

Label(root,text='Descarga tus videos ',
      font='arial 20 bold', bg='#AACDE2').place(x=90,y =30)

link = StringVar()
Label(root,text='Pega el link aqui:  ',
      font='arial 12', bg='#AACDE2').place(x=190,y =90)
link_enter=Entry(root,width=70,
                 textvariable=link).place(x=32, y =120)

def downloader_mp4():
    global numero_video
    download_video(merge_audio=False ,numero = numero_video)
    numero_video += 1

def downloader_mp3():
    global numero_audio
    download_video(merge_audio=True ,numero = numero_audio)
    numero_audio += 1

def clean_file(filename):
    cleaned_filename = re.sub(r'[\\/*?:<>|]','',filename)
    cleaned_filename = re.sub(r'\s+','_',cleaned_filename)
    return cleaned_filename


def download_video(merge_audio=False , numero= None):
    try:
        video_link = str(link.get()).strip()

        if not video_link:
            raise ValueError("No has ingresado ningun enlace.")
        
        url = YouTube(video_link)
        url.check_availability()
        video = url.streams.get_highest_resolution()

        user_home_dir = os.path.expanduser("~")

        folder_path = os.path.join(user_home_dir, "Desktop", "Videos_descargados")

        folder_path = os.path.normpath(folder_path)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        
        if merge_audio:
            audio_file_path = os.path.join(
                folder_path, f"audio{numero}.mp3")
            video.download(
                output_path=folder_path,filename="temp_video.mp4")
            video_path = os.path.join(
                folder_path, "temp_video.mp4")
            audio_path = os.path.join(
                folder_path, f"audio{numero}.mp3")
            convert_to_mp3(video_path, audio_path)
            os.remove(video_path)
            messagebox.showinfo('Hecho!!','Audio descargado con exito')
        else:
            file_name = os.path.join(
                folder_path, f"video{numero}.mp4")
            video.download(output_path=folder_path,
                            filename=f"video{numero}"+".mp4")
            messagebox.showinfo('Hecho ',
                            'El video ha sido descargado con exito')

        Label(root , text='Descargado', font='arial 13 bold',
            bg='#AACDE2',fg='#B57199').place(x=350,y=210)
    except Exception as e:
        messagebox.showerror('Error', str(e))

def convert_to_mp3(video_path,audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()
    video_clip.close()


def ExitProgram():
    root.quit()

Button(root, text='Descargar como MP4', font='arial 13 bold italic', bg='#B57199', padx=2, command=downloader_mp4).place(x=150, y=180)
Button(root, text='Descargar como MP3', font='arial 13 bold italic', bg='#B57199', padx=2, command=downloader_mp3).place(x=150, y=230)
Button(root, text='Salir', font='arial 13 bold italic', bg='#B57199', padx=2, command=ExitProgram).place(x=350, y=260)




root.mainloop()
