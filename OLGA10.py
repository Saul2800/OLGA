#OLGA 10.0
#ASISTENTE VIRTUAL REALIZADO EN PYTHON Y TKINTER
#OCTUBRE 2021 DICIEMBRE 2021

#Instalar por cmd las siguientes librerias:
#pip3 install pywhatkit
#pip3 install wikipedia
#pip3 install PyAudio    
#pip3 install pyttsx3 
#pip3 install SpeechRecognition
#pip3 install scipy

#Si hace falta alguna agregela de la misma forma que las anteriores

#Importar __________________________________________________________________________________________________
import struct
import tkinter
from pyttsx3 import engine
import pywhatkit
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import matplotlib
import matplotlib.pyplot as plt
import pyaudio as pa 
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import scipy.fftpack as fourier

#Hablar _________________________________________________________________________________________________________
def talk(text):
    
    #engine.say(text)
    print(" "+text)

    #engine.runAndWait()

#Escuchar _________________________________________________________________________________________________________
def listen(para):
    
    p.terminate() #En caso de que pyaudio siga abierto lo cerramos

    #Creamos un try
    while para:
        try:
            with sr.Microphone() as source:
                print("Escuchando...")  #Imprime en consola
                voice = listener.listen(source)
                rec = listener.recognize_google(voice, language='es-ES')  #Reconocimiento de voz
                rec = rec.lower()
            if name in rec:         #Si "OLGA" esta en el audio se borra
                rec = rec.replace(name, '')
                para=run(rec)     #Y nos manda a run() con rec
            else:
                talk("Vuelve a intentarlo, no reconozco: " + rec)
        except:
            pass
    return para

#ACCIONES ______________________________________________________________________________________________________
def run(rec):
  #Aqui todas las cosas que el asistente podra hacer

  #Reproducir un video de youtube
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)

  #La hora
    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)

  #BUscar en wikipedia
    elif 'busca' in rec:
        talk("Buscando")
        order = rec.replace('busca', '')
        wikipedia.set_lang("es")
        info = wikipedia.summary(order, 1)
        talk(info)

    #Enviar mensaje wtsup
    elif 'mensaje' in rec:
        talk("Enviando")
        #pywhatkit.sendwhatmsg("+5213861036554","Hola Miguel",3,0) 
        print("Envio Exitoso!") 

    #onda
    elif 'onda' in rec:
        talk("Abriendo...")
        para=senial(1)

    #saludar
    elif 'saluda' in rec:
        talk("Buen dia humanos")

    #Presentar
    elif 'presenta' in rec:
        talk("Mi nombre es olga")
        
    #desea
    elif 'deseas' in rec:
        music = rec.replace('reproduce', '')
        talk("Solo esto...")
        pywhatkit.playonyt("https://www.youtube.com/watch?v=SDTZ7iX4vTQ")

    #Salir del programa
    elif 'adiós' in rec:
        talk("Saliendo...")
        para=finalizar()

    #En caso de que no se encuentre
    else:
        talk("Vuelve a intentarlo, no reconozco: " + rec)

    return para

def senial(para):
    #para=1

    FRAMES = 1024*8                                   # Tamaño del paquete a procesar
    FORMAT = pa.paInt16                               # Formato de lectura INT 16 bits
    CHANNELS = 1                                      #Canales
    Fs = 44100                                        #FS
    fig, (ax,ax1) = plt.subplots(2)                     #Se crean 2 graficos

    x_audio = np.arange(0,FRAMES,1)                     #Psamos los datos
    x_fft = np.linspace(0, Fs, FRAMES)

    line, = ax.plot(x_audio, np.random.rand(FRAMES),'r')    #Para ax 
    line_fft, = ax1.semilogx(x_fft, np.random.rand(FRAMES), 'b')    #Para ax1

    ax.set_ylim(-4500,4500)                               #Entre 4500
    ax.ser_xlim = (0,FRAMES)

    Fmin = 1
    Fmax = 5000
    ax1.set_xlim(Fmin,Fmax)                             #Para axq entre 1 y 5000
    F = (Fs/FRAMES)*np.arange(0,FRAMES//2)  # Creamos el vector de frecuencia para encontrar la frecuencia dominante

    canvas = FigureCanvasTkAgg(fig, master=ventana)  # CREAR AREA DE DIBUJO DE TKINTER.
    canvas.get_tk_widget().grid(column=1,row=2)

    boton2=tkinter.Button(ventana, text="Volver",padx=50,pady=50, command = lambda: senial(0),bg="red",fg="blue")
    boton2.grid(row=2,column=0) #Boton para regresar al comando de voces

    while para:

        stream = p.open(                # Abrimos el canal de audio con los parámeteros de configuración
        format = FORMAT,
        channels = CHANNELS,
        rate = Fs,
        input=True,
        output=True,
        frames_per_buffer=FRAMES
        )

        data = stream.read(FRAMES)                         # Leemos paquetes de longitud FRAMES
        dataInt = struct.unpack(str(FRAMES) + 'h', data)   # Convertimos los datos que se encuentran empaquetados en bytes
        
        line.set_ydata(dataInt)                            # Asignamos los datos a la curva de la variación temporal
        
        M_gk = abs(fourier.fft(dataInt)/FRAMES)            # Calculamos la FFT y la Magnitud de la FFT del paqute de datos

        
        ax1.set_ylim(0,np.max(M_gk+10)) 
        line_fft.set_ydata(M_gk)                           # Asigmanos la Magnitud de la FFT a la curva del espectro 
        
        M_gk = M_gk[0:FRAMES//2]                           # Tomamos la mitad del espectro para encontrar la Frecuencia Dominante
        Posm = np.where(M_gk == np.max(M_gk))
        F_fund = F[Posm]      
             
        canvas.draw()
        fig.canvas.flush_events()



    para=listen(1)
    return para


#Finalizar _________________________________________________________________________________________________________
def finalizar():
        talk("Adios")
        ventana.destroy()
        para=0
        return para

#InicializandoSistema____________________________________________________________________________________________
# Nombre del asistente 
name = 'olga'

listener=sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

# Editamos la configuracion
engine. setProperty('rate', 178)
engine.setProperty('volume', 0.7)

p = pa.PyAudio() #pyaudio

#Bienvenida________________________________________________________________________________________________
talk ("Bienvenido")

#PropiedadesVentana _____________________________________________________________________________________________
ventana=tkinter.Tk()
ventana.geometry("700x500")
ventana.title("OLGA")
ventana.configure(bg="#0059b3")

#TITULO ______________________________________________________________________________________________________
bienvenidaEtiqueda=tkinter.Label(ventana,text="Asistente OLGA", bg="green")
bienvenidaEtiqueda.grid(row=0,column=0)

#Partes de la ventana __________________________________________________________________________________________
boton1=tkinter.Button(ventana, text="Comenzar",padx=50,pady=50, command = lambda: listen(1),bg="red",fg="blue")
boton1.grid(row=1,column=0)
#Ventana______________________________________________________________________________________________________
ventana.mainloop()


print("Fin programa")