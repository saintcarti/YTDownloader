from tkinter import *
from pytube import YouTube
from tkinter import messagebox
import os
from pydub import AudioSegment


AudioSegment.ffmpeg = "C:\\Users\\Xavier\\Desktop\\ffmg\\ffmpeg-6.1.1"
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
    download_video(merge_audio=False)

def downloader_mp3():
    download_video(merge_audio=True)
    
def download_video(merge_audio=False):
    try:
        video_link = str(link.get()).strip()

        if not video_link:
            raise ValueError("No has ingresado ningun enlace.")
        
        url = YouTube(video_link)
        url.check_availability()
        video = url.streams.get_by_resolution(resolution=1080)

        user_home_dir = os.path.expanduser("~")

        folder_path = os.path.join(user_home_dir, "Desktop", "Videos_descargados")

        folder_path = os.path.normpath(folder_path)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        
        if merge_audio:
            audio_file_path = os.path.join(folder_path, f"{url.title}.mp3")
            video.download(output_path=folder_path,filename="temp_video.mp4")
            video_path = os.path.join(folder_path, "temp_video.mp4")
            audio_path = os.path.join(folder_path, f"{url.title}.mp3")
            convert_to_mp3(video_path, audio_path)
            os.remove(video_path)
        else:
            file_name = os.path.join(folder_path, f"{url.title}.mp4")
            video.download(output_path=folder_path, filename=url.title+".mp4")
        messagebox.showinfo('Hecho ','El video ha sido descargado con exito')

        Label(root , text='Descargado', font='arial 13 bold',
            bg='#AACDE2',fg='#B57199').place(x=350,y=210)
    except Exception as e:
        messagebox.showerror('Error', str(e))

def convert_to_mp3(video_path,audio_path):
    video = AudioSegment.from_file(video_path,"mp4")
    video.export(audio_path, format="mp3")


def ExitProgram():
    root.quit()

Button(root, text='Descargar como MP4', font='arial 13 bold italic', bg='#B57199', padx=2, command=downloader_mp4).place(x=150, y=180)
Button(root, text='Descargar como MP3', font='arial 13 bold italic', bg='#B57199', padx=2, command=downloader_mp3).place(x=150, y=230)
Button(root, text='Salir', font='arial 13 bold italic', bg='#B57199', padx=2, command=ExitProgram).place(x=350, y=260)




root.mainloop()
