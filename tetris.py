import random
from pynput import keyboard as kb
import time 
import multiprocessing
from multiprocessing import Process, Queue
import time
import asyncio
from pynput import keyboard
import threading
import tracemalloc

# Enable tracemalloc
tracemalloc.start()


n = 0
i = 0
score = 0


def ocupadac():
    ocu=[] 
    fila1=[]
    for i in range(9):
        fila1.append(False)
    for x in range(10):
        ocu.append(fila1[:])
    return ocu
ocupada=ocupadac()
def repres(piezas):
    global score
    mapa=mapac() 
    ocu1=ocupadac()
    for i, pieza in enumerate(piezas):
        if pieza.tipo==1 or pieza.tipo==3:
        
            for x in range(pieza.x):
            
                if pieza.origenPx-x>=0:
                    mapa[pieza.origenPx-x][pieza.origenPy]="□"
                    ocu1[pieza.origenPx-x][pieza.origenPy]=True
            for y in range(pieza.y):
                mapa[pieza.origenPx][pieza.origenPy+y]="□"
                ocu1[pieza.origenPx][pieza.origenPy+y]=True
        if pieza.tipo==2:
            for x in range(pieza.x):
                if pieza.origenPx-x>=0:
                    mapa[pieza.origenPx-x][pieza.origenPy]="□"
                    ocu1[pieza.origenPx-x][pieza.origenPy]=True
            for y in range(pieza.y):
                mapa[pieza.origenPx][pieza.origenPy+y]="□"
                ocu1[pieza.origenPx][pieza.origenPy+y]=True
            if pieza.origenPx-x>=0:
                mapa[pieza.origenPx-1][pieza.origenPy+1]="□"
                ocu1[pieza.origenPx-1][pieza.origenPy+1]=True
    for i in range(10):
            print(" ".join(mapa[i]))
    print("SCORE:"+ str(score))
    print("\n")
    
    return ocu1


def mapac():
    fila=[]
    mapa=[]
    for i in range(9):
        fila.append("■")
    for x in range(10):
        mapa.append(fila[:])
    return mapa

class pieza:
    origenPx=0
    origenPy=0
    x=0
    y=0
    tipo=0
    tope=False
    def __init__(self,tipo,origenPx,origenPy):
        self.origenPx=origenPx
        self.origenPy=origenPy
        self.tipo=tipo
        if self.tipo==1: 
            self.x=3
            self.y=2
        elif self.tipo==2:
            self.x=2
            self.y=2
        elif self.tipo==3:
            self.x=4
            self.y=0    

    def movimiento(self,m):
        global ocupada
        if m==0: #rotacion
            print("No implementado nene")
        elif m==1:#tipo abajo
            if (self.origenPx)<9 and (self.tipo==3):
                if ocupada[self.origenPx+1][self.origenPy]==False:
                    self.origenPx=self.origenPx+1
                elif ocupada[self.origenPx+1][self.origenPy]==True: 
                    self.tope=True
            elif (self.origenPx)<9 and (self.tipo==2 or self.tipo==1):
                if ocupada[self.origenPx+1][self.origenPy]==False and ocupada[self.origenPx+1][self.origenPy+1] == False:
                    self.origenPx=self.origenPx+1
                elif ocupada[self.origenPx+1][self.origenPy]==True or ocupada[self.origenPx+1][self.origenPy+1] ==True: 
                    self.tope=True
            elif (self.origenPx)==9:
                self.tope=True
        elif m==2: #tipo arriba
            if (self.origenPx>0):
                self.origenPx=self.origenPx-1
        elif m==3:#tipo izquierda
            if (self.origenPy>0):
                if ocupada[self.origenPx][self.origenPy-1]==False:
                    self.origenPy=self.origenPy-1

        elif m==4:#tipo derecha
            if (self.origenPy+self.y<8) and (self.tipo==3):    
                if ocupada[self.origenPx][self.origenPy+1]==False:
                    self.origenPy=self.origenPy+1
            elif (self.origenPy+self.y<9)and (self.tipo==1 or self.tipo==2):    
                if ocupada[self.origenPx][self.origenPy+2]==False:
                    self.origenPy=self.origenPy+1       
piezas=[pieza(random.randint(1, 3), 0, random.randint(0, 7))]

def pulsa(tecla):
    global n, i, piezas, ocupada
    if str(tecla)=="Key.up":
            piezas[n].movimiento(2)
            ocupada=repres(piezas)
    if str(tecla)=="Key.down":
            piezas[n].movimiento(1)
            ocupada=repres(piezas)
    if str(tecla)=="Key.left":
            piezas[n].movimiento(3)
            ocupada=repres(piezas)
    if str(tecla)=="Key.right":
            piezas[n].movimiento(4)
            ocupada=repres(piezas)
    
    if str(tecla)=="Key.space":
        piezas[n].movimiento(0)
        ocupada=repres(piezas)   



mapa=mapac()


def tarea1(piezas):
    global n, i, ocupada, score
    while True:
        time.sleep(1)
        piezas[n].movimiento(1)
        ocupada=repres(piezas)
        score=score+5
        if (i >= 10 and i % 10 == 0) or (piezas[n].tope==True):
            nueva_pieza = pieza(random.randint(1, 3), 0, random.randint(0, 7))
            piezas.append(nueva_pieza)
            n += 1
            ocupada=repres(piezas)
            i=10
        i += 1
        
def tarea2(piezas): 
    global n, i
    listener = keyboard.Listener(on_press=pulsa)
    listener.start()
    listener.join()
    
    

     

hilo_actualizacion = threading.Thread(target=tarea1, args=(piezas,))
hilo_entrada = threading.Thread(target=tarea2, args=(piezas,))    
   
hilo_actualizacion.start()
hilo_entrada.start()

hilo_actualizacion.join()
hilo_entrada.join() 