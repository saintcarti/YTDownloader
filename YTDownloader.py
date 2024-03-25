from tkinter import *
from pytube import YouTube
from tkinter import messagebox

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

def Downloader():
    try:
        url = YouTube(str(link.get()))
        url.check_availability()
        video = url.streams.get_highest_resolution()
        video.download()
        messagebox.showinfo('Hecho ','el video ha sido descargado con exito')
        Label(root , text='Descargado', font='arial 13 bold',
            bg='#AACDE2',fg='#B57199').place(x=180,y=240)
    except Exception as e:
        messagebox.showerror('Error', str(e))

def ExitProgram():
    root.quit()

Button(root,text='Descargar', font='arial 13 bold italic',
       bg='#B57199',padx=2,
       command=Downloader).place(x=180,y=180)

Button(root,text='Salir', font='arial 13 bold italic',
       bg='#B57199',padx=2,
       command=ExitProgram).place(x=350,y=180)




root.mainloop()