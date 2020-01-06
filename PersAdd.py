from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os


class PersAdd(object):

    def __init__(self):
        tbc = 0

    def show(self):
        print('PersAdd.show')

        self.persAddWindow = Toplevel()

        self.persAddWindow.title('Ajout de Personne')
        self.persAddWindow.geometry('500x200+80+100')
        self.persAddWindow['bg'] = 'light slate gray'

        # ACTIONS ---------------------------------------------------------------------------------------------
        # --------- Creation de la fenetre
        actionFrame = LabelFrame(self.persAddWindow, text='Action', labelanchor='nw', bd=5, bg='alice blue',
                                 borderwidth=2, width=250, height=70, highlightthickness=5,
                                 highlightbackground='alice blue', font='arial 9 italic', foreground='navy')
        actionFrame.pack_propagate(False)
        actionFrame.pack(side=TOP, padx=5, pady=5)

        # --------- Boutton SUPPRIMER
        actualiseButton = Button(actionFrame, text='AJOUTER ET QUITTER', state=NORMAL, font='arial 10 bold',
                                 foreground='chartreuse3', background='black', command=self.addPers)
        actualiseButton.pack(side=TOP, pady=5, padx=20)

        # FENETRE PRINCIPALE
        self.mainFrame = Frame(self.persAddWindow, bg='alice blue', width=450, height=500, highlightthickness=0)
        self.persInfoFrame = LabelFrame(self.mainFrame, text='Informations pour l ajout de personne - Nom et acronyme',
                                       labelanchor='nw', bd=5, bg='alice blue', borderwidth=2, width=450, height=400,
                                       highlightthickness=0, highlightbackground='alice blue', foreground='navy',
                                       font='arial 10 italic')
        self.mainFrame.pack(side=TOP, pady=10)

        # Fenetre de titre :
        self.persNameFrame = Frame(self.persInfoFrame, bg='alice blue', borderwidth=2, width=430,
                                    height=50, highlightthickness=0, highlightbackground='alice blue')
        self.persInfoFrame.pack(padx=5, pady=5)
        self.persNameFrame.pack_propagate(False)
        self.persNameFrame.pack(padx=2, pady=2)

        value = StringVar()
        self.persNameEntry = Entry(self.persNameFrame, textvariable=value, font='arial 9',
                                    highlightthickness=0, width=40)
        self.persNameEntry.var = value
        self.persNameEntry.insert(0, 'prenom et nom')
        self.persNameEntry.pack(side=LEFT, padx=2, pady=2)

        value = StringVar()
        self.persAcroEntry = Entry(self.persNameFrame, textvariable=value, font='arial 9',
                                  highlightthickness=0, width=20)
        self.persAcroEntry.var = value
        self.persAcroEntry.insert(0, 'acronyme')
        self.persAcroEntry.pack(side=RIGHT, padx=2, pady=2)

    def addPers(self):

        print('PersAdd.addPers')

        # Acquisition titre et Acro
        self.persName = self.persNameEntry.var.get()
        self.persAcro = self.persAcroEntry.var.get()

        # Ouverture nouveau fichier
        fileToWrite = 'PersList\\' + self.persAcro
        fileToCreate = open(fileToWrite, "w+")

        fileToCreate.write(self.persName)

        fileToCreate.close()

        # FENETRE POP UP AVEC CONSIGN UTILISATEUR
        self.popup = Toplevel()
        self.popup.title('Ajout terminee')
        self.popup.geometry('300x120+450+300')
        self.popup['bg'] = 'alice blue'

        msg = Message(self.popup, text='Nouvelle personne bien ajoutee', anchor=CENTER, bg='alice blue', width=250,
                      font='arial 9 bold')
        msg.pack(side=TOP, pady=5)
        msg2 = Message(self.popup, anchor=CENTER, bg='alice blue', width=250, font='arial 9',
                       text='La fenetre liée au menu va se fermée \nMerci d actualiser la fenetre principale')
        msg2.pack(side=TOP, pady=0)

        self.windowList = [self.popup, self.persAddWindow]

        but = Button(self.popup, text='OK', command=self.destroyWindow, state=NORMAL, width=20,
                     font='arial 10 bold', foreground='black', bg='grey60')
        but.pack(side=TOP, pady=5)

    def destroyWindow(self):
        for window in self.windowList:
            window.destroy()