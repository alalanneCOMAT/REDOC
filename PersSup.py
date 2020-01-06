from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os


class PersSup(object):

    def __init__(self, persList=None):
        self.persList = persList

    def show(self):
        print('PersSupp.show')

        self.persSupWindow = Toplevel()

        self.persSupWindow.title('Personne - Menu suppression')
        self.persSupWindow.geometry('500x500+80+100')
        self.persSupWindow['bg'] = 'light slate gray'

        # ACTIONS ---------------------------------------------------------------------------------------------
        # --------- Creation de la fenetre
        actionFrame = LabelFrame(self.persSupWindow, text='Action', labelanchor='nw', bd=5, bg='alice blue',
                                 borderwidth=2, width=250, height=70, highlightthickness=5,
                                 highlightbackground='alice blue', font='arial 9 italic', foreground='navy')
        actionFrame.pack_propagate(False)
        actionFrame.pack(side=TOP, padx=2, pady=5)

        # --------- Boutton SUPPRIMER
        actualiseButton = Button(actionFrame, text='SUPPRIMER ET QUITTER',
                                 command=self.deletefile, state=NORMAL, font='arial 10 bold', foreground='red',
                                 background='black')
        actualiseButton.pack(side=TOP, pady=5, padx=20)

        # FENETRE PRINCIPALE
        self.mainFrame = Frame(self.persSupWindow, bg='alice blue', width=450, height=400)
        self.canvasContainer = Canvas(self.mainFrame, bg='alice blue', width=450, height=400)
        self.defilY = Scrollbar(self.mainFrame, orient='vertical', command=self.canvasContainer.yview)
        self.buttonFram = LabelFrame(self.canvasContainer, text='Liste des personnes', labelanchor='nw', bd=5,
                                     bg='alice blue', borderwidth=2, width=450, height=400, highlightthickness=5,
                                     highlightbackground='alice blue', font='arial 9 italic', foreground='navy')
        self.defilY.bind("<Configure>",
                         lambda e: self.canvasContainer.configure(scrollregion=self.canvasContainer.bbox("all")))

        self.canvasContainer.create_window((0, 0), window=self.buttonFram, anchor='nw')
        self.canvasContainer.configure(yscrollcommand=self.defilY.set)

        self.mainFrame.pack(side=TOP)
        self.canvasContainer.pack(side=LEFT)
        self.defilY.pack(side='right', fill='y')

        # Remplissage de la fenetre
        self.doc = []
        i = 0
        for persTitle in self.persList:
            checkValue = IntVar()
            self.doc.append(Checkbutton(self.buttonFram, text=persTitle, variable=checkValue, onvalue=1,
                                        offvalue=0, bg='alice blue', font='arial 9', width=52, anchor=W))

            self.doc[i].var = checkValue
            self.doc[i].pack(side=TOP, padx=20, pady=0, anchor=W)
            i += 1

    def deletefile(self):

        persState = []
        for p in self.doc:
            persState.append(p.var.get())

        indic = 0
        for i in range(0,len(self.persList)):
            if persState[i] == 1:
                fileToDestroy = 'PersList\\' + self.persList[i]
                os.remove(fileToDestroy)
                indic += 1

        print('PersSupp.deletePers ' + str(indic))

        # FENETRE POP UP AVEC CONSIGN UTILISATEUR
        self.popup = Toplevel()
        self.popup.title('Suppression terminee')
        self.popup.geometry('300x120+450+300')
        self.popup['bg'] = 'alice blue'

        # verification de la suppression d'au moins une personne
        trigersSelec = 0
        for state in persState:
            if state == 1:
                trigersSelec = 1

        if trigersSelec == 0:
            msgText = 'Aucune personne supprimee'
            msg2text = 'La fenetre liée au menu va se fermée'
        else:
            msgText = 'Personnes supprimees'
            msg2text = 'La fenetre liée au menu va se fermée \nMerci d actualiser la fenetre principale'

        msg = Message(self.popup, text=msgText, anchor=CENTER, bg ='alice blue', width=250, font='arial 9 bold')
        msg.pack(side=TOP, pady=5)
        msg2 = Message(self.popup, text=msg2text, anchor=CENTER, bg ='alice blue', width=250, font='arial 9')
        msg2.pack(side=TOP, pady=0)

        self.windowList = [self.popup, self.persSupWindow]

        but = Button(self.popup, text='OK', command=self.destroyWindow, state=NORMAL, width=20,
                     font='arial 10 bold', foreground='black', bg='grey60')
        but.pack(side=TOP, pady=5)

    def destroyWindow(self):
        for window in self.windowList:
            window.destroy()