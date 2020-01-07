from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import ctypes


class PersAdd(object):

    def __init__(self):
        # REUCUPERATION DE LA TAILLE DE LECRAN
        usr32 = ctypes.windll.user32
        largeurEcran = usr32.GetSystemMetrics(0)
        hauteurEcran = usr32.GetSystemMetrics(1)

        self.scaleFactor = float(int(largeurEcran)/1366)

    def show(self):
        print('PersAdd.show')

        self.persAddWindow = Toplevel()

        self.persAddWindow.title('Ajout de Personne')
        largeur = self.scaleFactor * 500
        hauteur = self.scaleFactor * 200
        decalLarg = self.scaleFactor * 80
        decalHaut = self.scaleFactor * 100
        self.persAddWindow.geometry('%dx%d+%d+%d' % (largeur, hauteur, decalLarg, decalHaut))
        self.persAddWindow['bg'] = 'light slate gray'

        # ACTIONS ---------------------------------------------------------------------------------------------
        # --------- Creation de la fenetre
        actionFrame = LabelFrame(self.persAddWindow, text='Action', labelanchor='nw', bd=5, bg='alice blue',
                                 borderwidth=2, width=int(self.scaleFactor*250), height=int(self.scaleFactor*70), highlightthickness=5,
                                 highlightbackground='alice blue', font='arial 9 italic', foreground='navy')
        actionFrame.pack_propagate(False)
        actionFrame.pack(side=TOP, padx=5, pady=5)

        # --------- Boutton SUPPRIMER
        actualiseButton = Button(actionFrame, text='AJOUTER ET QUITTER', state=NORMAL, font='arial 10 bold',
                                 foreground='chartreuse3', background='black', command=self.addPers)
        actualiseButton.pack(side=TOP, pady=5, padx=20)

        # FENETRE PRINCIPALE
        self.mainFrame = Frame(self.persAddWindow, bg='alice blue', width=int(self.scaleFactor*450), height=int(self.scaleFactor*500), highlightthickness=0)
        self.persInfoFrame = LabelFrame(self.mainFrame, text='Informations pour l ajout de personne - Nom et acronyme',
                                       labelanchor='nw', bd=5, bg='alice blue', borderwidth=2, width=int(self.scaleFactor*450), height=int(self.scaleFactor*400),
                                       highlightthickness=0, highlightbackground='alice blue', foreground='navy',
                                       font='arial 10 italic')
        self.mainFrame.pack(side=TOP, pady=10)

        # Fenetre de titre :
        self.persNameFrame = Frame(self.persInfoFrame, bg='alice blue', borderwidth=2, width=int(self.scaleFactor*430),
                                    height=int(self.scaleFactor*50), highlightthickness=0, highlightbackground='alice blue')
        self.persInfoFrame.pack(padx=5, pady=5)
        self.persNameFrame.pack_propagate(False)
        self.persNameFrame.pack(padx=2, pady=2)

        value = StringVar()
        self.persNameEntry = Entry(self.persNameFrame, textvariable=value, font='arial 9',
                                    highlightthickness=0, width=int(self.scaleFactor*40))
        self.persNameEntry.var = value
        self.persNameEntry.insert(0, 'prenom et nom')
        self.persNameEntry.pack(side=LEFT, padx=2, pady=2)

        value = StringVar()
        self.persAcroEntry = Entry(self.persNameFrame, textvariable=value, font='arial 9',
                                  highlightthickness=0, width=int(self.scaleFactor*20))
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
        largeur = self.scaleFactor * 300
        hauteur = self.scaleFactor * 120
        decalLarg = self.scaleFactor * 450
        decalHaut = self.scaleFactor * 300
        self.popup.geometry('%dx%d+%d+%d' % (largeur, hauteur, decalLarg, decalHaut))
        self.popup['bg'] = 'alice blue'

        msg = Message(self.popup, text='Nouvelle personne bien ajoutee', anchor=CENTER, bg='alice blue', width=int(self.scaleFactor*250),
                      font='arial 9 bold')
        msg.pack(side=TOP, pady=5)
        msg2 = Message(self.popup, anchor=CENTER, bg='alice blue', width=int(self.scaleFactor*250), font='arial 9',
                       text='La fenetre liée au menu va se fermée \nMerci d actualiser la fenetre principale')
        msg2.pack(side=TOP, pady=0)

        self.windowList = [self.popup, self.persAddWindow]

        but = Button(self.popup, text='OK', command=self.destroyWindow, state=NORMAL, width=int(self.scaleFactor*20),
                     font='arial 10 bold', foreground='black', bg='grey60')
        but.pack(side=TOP, pady=5)

    def destroyWindow(self):
        for window in self.windowList:
            window.destroy()