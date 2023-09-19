import ast
import os
import copy
from random import randint
from tkinter import *
from tkinter import ttk
import tkinter.messagebox

a=0 ##player 1 ou player 2
b=0 ##numero de jogadas
c=0 ##jogo contra bot
d=0 ##dificuldade
bu={} ##dicionario de butoes
safeplay = {} ##guardar jogadas seguras
safeboard= {} ##guardar mesas de jogadas seguras

def restartbutton():
    global a,b,c
    a=randint(1,2)
    print("rand inicial "+ str(a))
    b=0
    changeplayer()
    for i in range(3):
        for j in range(4):
            bu[i][j]['state']='normal'
            bu[i][j]['image']=''
    if a ==2 and c==1:
        bot_jogada()
        return
    
def disableButton():
    for i in range(3):
        for j in range(4):
            bu[i][j]['state']='disabled'

def ButtonClick(id):
    if a == 1:
        player_jogada(id)
    elif a == 2:
        player_jogada(id)
    if a==2 and c == 1:
        bot_jogada()
        return

def changeplayer():
    global a,c
    if c==0:
        if a==1:
            a=2
            playerturn['text']="   Player 2 turn!   "
            return
        else:
            a=1
            playerturn['text']="   Player 1 turn!   "
            return
    else:
        
        if a==1:
            a=2
            playerturn['text']="   BOT turn!   "
            return
        else:
            a=1
            playerturn['text']="   Player turn!   "
            return

def player_jogada(id):
    global a,b,c,tri_img,cir_img,sqr_img,bu
    b+=1
    playerdetails["text"] = "       Jogadas: " + str(b)
    if str(id).replace(".!button","") == "":
        buttonid="1"
    else:
        buttonid=str(id).replace(".!button","")
    #print do player e do estado do butao antes da mudança
    print("Player:" + str(a) +"\n")
    print("Button "+ buttonid + " State:" + str(id['state'])+'->')
    #mudança de estado
    if id['state']=='normal':
        id['image']=tri_img
        id['state']='1'
    elif id['state']=='1': 
        id['image']=cir_img
        id['state']='2'
    elif id['state']=='2':
        id['image']=sqr_img
        id['state']='disabled'
    #print depois da mudan�a
    print(str(id['state']))
    #verificar se alguem ganhou
    printboard()
    if check_win():
        disableButton()
        tkinter.messagebox.showinfo(title="Vitoria", message="O Player " + str(a) + " ganhou após " +str(b)+" jogadas")
        return
    changeplayer() 

def bot_jogada():
    #defenir jogada bot
    global a,b,bu
    if d == 1:
        cords=dificuldade1(copy_states())
    elif d == 2:
        cords=dificuldade2(copy_states())
    elif d == 3:
        cords=dificuldade3(copy_states())
    id=bu[cords[0]][cords[1]]
    if id['state']!='disabled':
        if id['state']=='normal':
            id['image']=tri_img
            id['state']='1'
        elif id['state']=='1': 
            id['image']=cir_img
            id['state']='2'
        elif id['state']=='2':
            id['image']=sqr_img
            id['state']='disabled'
    else:
        bot_jogada()
        return
    b+=1
    if check_win():
        disableButton()
        tkinter.messagebox.showinfo(title="Derrota", message="O BOT " + str(a) + " ganhou após " +str(b)+" jogadas")
        return
    changeplayer()
    return

def dificuldade1(states):
    for i in range(3):
        for j in range(4):
            temp=copy.deepcopy(states)       
            if temp[i][j]!='disabled':
                if temp[i][j]=='normal':
                    temp[i][j]='1'
                elif temp[i][j]=='1':
                    temp[i][j]='2'
                elif temp[i][j]=='2':
                    temp[i][j]='disabled'
                if check_win_bot(temp):
                    return (i,j,1) #o bot tem a certeza que ganha na proxima jogada
    i=randint(0,2)
    j=randint(0,3)
    return (i,j,0) # indeterminado

def dificuldade2(state):
    global safeplay,safeboard
    vic=dificuldade1(copy.deepcopy(state))
    if vic[2]==1:
        return vic#o bot tem a certeza que ganha na proxima jogada
    x=0
    for i in range(3):
        for j in range(4):
            temp=copy.deepcopy(state)
            if temp[i][j]!='disabled':
                if temp[i][j]=='normal':
                    temp[i][j]='1'
                elif temp[i][j]=='1':
                    temp[i][j]='2'
                elif temp[i][j]=='2':
                    temp[i][j]='disabled'
                vic=dificuldade1(temp)
                if vic[2]==0:
                    safeplay[x]=(i,j,1) #o bot tem a certeza que nao perde na proxima jogada
                    safeboard[x]=temp 
                    x+=1
    if x>0:
        return safeplay[randint(0,x-1)]
    i=randint(0,2)
    j=randint(0,3)
    return (i,j,0) # indeterminado

def dificuldade3(state):  #não funciona
    global safeplay,safeboard
    vic=dificuldade1(copy.deepcopy(state))
    if vic[2]==1:
        return vic #o bot tem a certeza que ganha na proxima jogada
    dificuldade2(state)
    if not safeboard:
        i=randint(0,2)
        j=randint(0,3)
        print("Não tenho encontrei jogadas seguras")
        return (i,j,0) # indeterminado
    else:
        print("tenho " + str(range(len(safeboard))) +"jogadas safe")
        for k in range(len(safeboard)):
            for i in range(3):
                for j in range(4):
                    for k in range (3):
                        for l in range (4):
                            temp=copy.deepcopy(state)       
                            if temp[i][j]!='disabled' and temp[k][l]!='disabled':
                                if temp[i][j]=='normal':
                                    temp[i][j]='1'
                                elif temp[i][j]=='1':
                                    temp[i][j]='2'
                                elif temp[i][j]=='2':
                                    temp[i][j]='disabled'
                                if temp[k][l]=='normal':
                                    temp[k][l]='1'
                                elif temp[k][l]=='1':
                                    temp[k][l]='2'
                                elif temp[k][l]=='2':
                                    temp[k][l]='disabled'
                                vic=dificuldade1(temp)
                                if vic[2]==0:
                                    safeplay[k]=(safeplay[k][0],safeplay[k][1],0)
            if safeplay[k][2]==1:
                return safeplay[k]
        return safeplay[randint(0,k-1)]

def copy_states():
    global bu
    states=[['','','',''],['','','',''],['','','','']]
    for i in range(3):
        for j in range(4):
            bt=bu[i][j]['state']
            temp=copy.deepcopy(str(bt))
            states[i][j]=temp
    return states

def check_win_bot(bu):
    x=0
    for y in range(0,4):
        if bu[x][y]!='normal' and bu[x][y]==bu[x+1][y]==bu[x+2][y]:
            return True    
    #check horizontal
    for y in range(0,2):
        for x in range(0,3):
            if bu[x][y]!='normal' and bu[x][y]==bu[x][y+1]==bu[x][y+2]:
                return True
    #check diagonal descendente
    x=0
    for y in range(0,2):
        if bu[x][y]!='normal' and bu[x][y]==bu[x+1][y+1]==bu[x+2][y+2]:
            return True
    #check diagonal ascendente
    x=2
    for y in range(0,2):
        if bu[x][y]!='normal' and bu[x][y]==bu[x-1][y+1]==bu[x-2][y+2]:
            return True
    return False

def printboard():
    for x in range(0,3):
        print('\n')
        for y in range(0,4):
            if bu[x][y]['state']=='normal':
                print(0, end=' ')
            else:
                print(bu[x][y]['state'], end=' ')

def check_win():
    #se bot for igual a 0 é uma verficação de vitoria para calculo do bot
    #check vertical 
    global bu
    x=0
    temp = copy_states() #nao funciona sem isto nao sei porque WTF --> pergunta ao prof
    for y in range(0,4):
        if bu[x][y]['state']!='normal' and bu[x][y]['state']==bu[x+1][y]['state']==bu[x+2][y]['state']:
            bu[x][y]['image']=star_img
            bu[x+1][y]['image']=star_img
            bu[x+2][y]['image']=star_img
            #print("GG")
            return True    
    #check horizontal
    for y in range(0,2):
        for x in range(0,3):
            if bu[x][y]['state']!='normal' and bu[x][y]['state']==bu[x][y+1]['state']==bu[x][y+2]['state']:
                bu[x][y]['image']=star_img
                bu[x][y+1]['image']=star_img
                bu[x][y+2]['image']=star_img
                #print("GG")
                return True
    #check diagonal descendente
    x=0
    for y in range(0,2):
        if bu[x][y]['state']!='normal' and bu[x][y]['state']==bu[x+1][y+1]['state']==bu[x+2][y+2]['state']:
            bu[x][y]['image']=star_img
            bu[x+1][y+1]['image']=star_img
            bu[x+2][y+2]['image']=star_img
            #print("GG")
            return True
    #check diagonal ascendente
    x=2
    for y in range(0,2):
        if bu[x][y]['state']!='normal' and bu[x][y]['state']==bu[x-1][y+1]['state']==bu[x-2][y+2]['state']:
            bu[x][y]['image']=star_img
            bu[x-1][y+1]['image']=star_img
            bu[x-2][y+2]['image']=star_img
            #print("GG")
            return True
    return False

def jogar(bot,dif):
    global c,d
    home.withdraw()
    c=bot
    d=dif
    root.deiconify()
    return

def save_game():
    global a,b,c,d
    estado=copy_states()
    #open file for writing
    file=open("savefile.txt","w")
    #write to file
    file.write(str(a)+'\n')
    file.write(str(b)+'\n')
    file.write(str(c)+'\n')
    file.write(str(d)+'\n')
    file.write(str(estado)+'\n')
    root.withdraw()
    restartbutton()
    home.deiconify()
    file.close()
    return

def load_game():
    global a,b,c,d,bu,root,home,tri_img,cir_img,sqr_img
    root.deiconify()
    #open file for reading
    file=open("savefile.txt","r")
    #read from file
    a=int(file.readline())
    b=int(file.readline())
    c=int(file.readline())
    d=int(file.readline())
    estado = file.readline()
    estado=ast.literal_eval(estado)
    for i in range(3):
        for j in range(4):
            bu[i][j]['state']=estado[i][j]
    for i in range(3):
        for j in range(4):
            if bu[i][j]['state']=='1':
                bu[i][j]['image']=tri_img
            elif bu[i][j]['state']=='2': 
                bu[i][j]['image']=cir_img
            elif bu[i][j]['state']=='disabled':
                bu[i][j]['image']=sqr_img
    file.close()
    playerturn["text"] = "Player "+str(a)+" turn"
    playerdetails["text"] = "Jogada: "+str(b)
    home.withdraw()

root=Tk()
root.withdraw()
root.title("Semáforo")
tri_img=PhotoImage(file="triangle.png")
cir_img=PhotoImage(file="circle.png")
sqr_img=PhotoImage(file="square.png")
star_img=PhotoImage(file="star.png")

#add Buttons
bu1=ttk.Button(root)
bu1.grid(row=0,column=0,sticky='snew',ipadx=40,ipady=40)
bu1.config(command=lambda: ButtonClick(bu1))

bu2=ttk.Button(root)
bu2.grid(row=0,column=1,sticky='snew',ipadx=40,ipady=40)
bu2.config(command=lambda: ButtonClick(bu2))

bu3=ttk.Button(root)
bu3.grid(row=0,column=2,sticky='snew',ipadx=40,ipady=40)
bu3.config(command=lambda: ButtonClick(bu3))

bu4=ttk.Button(root)
bu4.grid(row=0,column=3,sticky='snew',ipadx=40,ipady=40)
bu4.config(command=lambda: ButtonClick(bu4))

bu5=ttk.Button(root)
bu5.grid(row=1,column=0,sticky='snew',ipadx=40,ipady=40)
bu5.config(command=lambda: ButtonClick(bu5))

bu6=ttk.Button(root)
bu6.grid(row=1,column=1,sticky='snew',ipadx=40,ipady=40)
bu6.config(command=lambda: ButtonClick(bu6))

bu7=ttk.Button(root)
bu7.grid(row=1,column=2,sticky='snew',ipadx=40,ipady=40)
bu7.config(command=lambda: ButtonClick(bu7))

bu8=ttk.Button(root)
bu8.grid(row=1,column=3,sticky='snew',ipadx=40,ipady=40)
bu8.config(command=lambda: ButtonClick(bu8))

bu9=ttk.Button(root)
bu9.grid(row=2,column=0,sticky='snew',ipadx=40,ipady=40)
bu9.config(command=lambda: ButtonClick(bu9))

bu10=ttk.Button(root)
bu10.grid(row=2,column=1,sticky='snew',ipadx=40,ipady=40)
bu10.config(command=lambda: ButtonClick(bu10))

bu11=ttk.Button(root)
bu11.grid(row=2, column=2,sticky='snew',ipadx=40,ipady=40)
bu11.config(command=lambda: ButtonClick(bu11))

bu12=ttk.Button(root)
bu12.grid(row=2,column=3,sticky='snew',ipadx=40,ipady=40)
bu12.config(command=lambda: ButtonClick(bu12))

bu=[[bu1,bu2,bu3,bu4],[bu5,bu6,bu7,bu8],[bu9,bu10,bu11,bu12]]

playerturn=ttk.Label(root,text="   Player 1 turn!  ")
playerturn.grid(row=3,column=0,sticky='snew',ipadx=40,ipady=40)

playerdetails=ttk.Label(root,text="Jogada: 0")
playerdetails.grid(row=3,column=3,sticky='snew',ipadx=40,ipady=40)

res=ttk.Button(root,text='Restart')
res.grid(row=3,column=1,sticky='snew',ipadx=40,ipady=40)
res.config(command=lambda: restartbutton())

save=ttk.Button(root,text='Save game')
save.grid(row=3,column=2,sticky='snew',ipadx=40,ipady=40)
save.config(command=lambda: save_game())

home=Tk()
home.title("Semáforo")
bt=ttk.Button(home,text="Jogador vs Jogador")
bt.grid(row=0,column=0,sticky='snew',ipadx=60,ipady=60)
bt.config(command=lambda: jogar(0,0))

bt1=ttk.Button(home,text="Jogador vs Bot Nível 1")
bt1.grid(row=0,column=1,sticky='snew',ipadx=60,ipady=60)
bt1.config(command=lambda: jogar(1,1))

bt2=ttk.Button(home,text="Jogador vs Bot Nível 2")
bt2.grid(row=1,column=1,sticky='snew',ipadx=60,ipady=60)
bt2.config(command=lambda: jogar(1,2))

bt3=ttk.Button(home,text="Jogador vs Bot Nível 3")
bt3.grid(row=2,column=1,sticky='snew',ipadx=60,ipady=60)
bt3.config(command=lambda: jogar(1,3))

bt4=ttk.Button(home,text="Load")
bt4.grid(row=2,column=0,sticky='snew',ipadx=60,ipady=60)
bt4.config(command=lambda: load_game())
if os.path.getsize("savefile.txt") == 0:
    bt4.state(['disabled'])
else:
    bt4.state(['!disabled'])

restartbutton()
home.mainloop() # loop infinito para a janela do menu
root.mainloop() # loop infinito para a janela do jogo