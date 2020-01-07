import os
import re
import shutil
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import ctypes

# IMPORT PERSO
from DocMenu import DocMenu
from DocSup import DocSup
from DocAdd import DocAdd

from PersAdd import PersAdd
from PersSup import PersSup
from PersMenu import PersMenu


class MainWindow(object):

    def __init__(self):

        # REUCUPERATION DE LA TAILLE DE LECRAN
        usr32 = ctypes.windll.user32
        largeurEcran = usr32.GetSystemMetrics(0)
        hauteurEcran = usr32.GetSystemMetrics(1)

        self.scaleFactor = float(int(largeurEcran)/1366)

        # CREATION DE LA FENETRE PRINCIPALE --------------------------------------------------------------------------
        self.mainWindow = Tk()

        self.mainWindow.title('REDOC - Logiciel de relecture de document')
        self.mainWindow['bg'] = 'light slate gray'

        # GESTION OUVERTURE -----------------------------------------------------------------
        fileToAnalyse = "UseFile" + '\\' + 'IndicOuverture'

        with open(fileToAnalyse, 'r') as readFile:

            for line in readFile:
                indicOuverture = int(str(line))
        # -----------------------------------------------------------------------------------

        if indicOuverture == 1:
            print('MainWindow.AccessOFF')

            largeur = self.scaleFactor*100
            hauteur = self.scaleFactor*100
            decalLarg = self.scaleFactor*10
            decalHaut = self.scaleFactor*10
            self.mainWindow.geometry('%dx%d+%d+%d' % (largeur, hauteur, decalLarg, decalHaut))

            self.popup = Toplevel()
            self.popup.title('ACCES IMPOSSIBLE')
            largeur = self.scaleFactor*300
            hauteur = self.scaleFactor*120
            decalLarg = self.scaleFactor * 400
            decalHaut = self.scaleFactor * 250
            self.popup.geometry('%dx%d+%d+%d' % (largeur, hauteur, decalLarg, decalHaut))
            self.popup['bg'] = 'alice blue'

            msgText = 'REDOC deja en cours d utilisation'
            msg2text = 'La fenetre va se fermer \nAppuyer sur OK'

            msg = Message(self.popup, text=msgText, anchor=CENTER, bg='alice blue', width=int(self.scaleFactor*250), font='arial 9 bold')
            msg.pack(side=TOP, pady=5)
            msg2 = Message(self.popup, text=msg2text, anchor=CENTER, bg='alice blue', width=int(self.scaleFactor*250), font='arial 9')
            msg2.pack(side=TOP, pady=0)

            self.windowList = [self.popup, self.mainWindow]

            but = Button(self.popup, text='OK', command=self.destroyWindow, state=NORMAL, width=int(self.scaleFactor*20),
                         font='arial 10 bold', foreground='black', bg='grey60')
            but.pack(side=TOP, pady=5)

        else:

            print('MainWindow.AccessON')

            # GESTION OUVERTURE -----------------------------------------------------------------
            fileToWrite = 'UseFile\\' + 'indicOuverture'
            fileToCreate = open(fileToWrite, "w+")

            fileToCreate.write('1')
            fileToCreate.close()
            # -----------------------------------------------------------------------------------

            largeur = self.scaleFactor*1100
            hauteur = self.scaleFactor*650
            decalLarg = self.scaleFactor*10
            decalHaut = self.scaleFactor*10
            self.mainWindow.geometry('%dx%d+%d+%d' % (largeur, hauteur, decalLarg, decalHaut))

            print("MainWindow.__init__")

            # ACTIONS PERMANENTES -------------------------------------------------------------------------------------
            # Creation de la fenetre
            actionFrame = LabelFrame(self.mainWindow, text='Action permanente', labelanchor='nw', bd=5, bg='alice blue',
                                     borderwidth=2, width=int(self.scaleFactor*150), height=int(self.scaleFactor*635), highlightthickness=5,
                                     highlightbackground='alice blue', font='arial 9 italic', foreground='navy')
            actionFrame.pack_propagate(False)
            actionFrame.pack(side=LEFT, padx=5, pady=5)

            # Boutton ACTUALISER
            actualiseButton = Button(actionFrame, text='ACTUALISER', command=self.actualiseEnvironement,
                                     state=NORMAL, font='arial 10 bold', foreground='DarkGoldenrod1', background='black')
            actualiseButton.pack(side=TOP, pady=10, padx=5)

            # BLOC DE RESPONSABILITE
            # --------- Creation de la fenetre
            frameContainer = Frame(actionFrame, bg='alice blue', width=int(self.scaleFactor*150), height=int(self.scaleFactor*100))
            canvasContainer = Canvas(frameContainer, bg='alice blue', width=int(self.scaleFactor*100), height=int(self.scaleFactor*110), highlightthickness=0)
            defilY = Scrollbar(frameContainer, orient='vertical', command=canvasContainer.yview)

            peopleText = 'Responsabilite'
            peopleFrame = LabelFrame(frameContainer, text=peopleText, labelanchor='nw', bd=5, bg='alice blue',
                                     borderwidth=1, width=int(self.scaleFactor*80), height=int(self.scaleFactor*50), highlightthickness=2,
                                     highlightbackground='alice blue', font='arial 7', relief=GROOVE)

            defilY.bind("<Configure>", lambda e: canvasContainer.configure(scrollregion=canvasContainer.bbox("all")))
            canvasContainer.configure(yscrollcommand=defilY.set)
            canvasContainer.create_window((2, 2), window=peopleFrame, anchor='nw')

            frameContainer.pack(side=TOP)
            canvasContainer.pack(side=LEFT)
            defilY.pack(side='right', fill='y')

            # ------------------- Personnes en cours sur le projets - liste complète
            self.persListFilBrut = sorted(os.listdir("PersList"))
            self.persListFil = []
            for pers in self.persListFilBrut:
                self.persListFil.append(pers.split('.')[0])

            # --------------------- Ajout des noms dans la fenetre deja tous coché
            self.peoples = []
            i = 0
            for cle in self.persListFil:
                peopleName = cle
                checkValue = IntVar()
                checkValue.set(1)
                self.peoples.append(Checkbutton(peopleFrame, text=peopleName, variable=checkValue, onvalue=1,
                                                offvalue=0, font='arial 7', bg='alice blue'))
                self.peoples[i].select()
                self.peoples[i].var = checkValue
                self.peoples[i].pack(side=TOP, padx=20, pady=0, anchor=W)
                i += 1

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.mainWindow.mainloop()

    def actualiseEnvironement(self):
        print("MainWindow.actualiseEnvironement")

        self.docListFil = sorted(os.listdir("DocList"))
        self.persListFil = sorted(os.listdir("PersList"))
        self.sub_windows = []

        self.defineMenuBar()

        try:
            self.mainFrame.destroy()
        except:
            None

        # FENETRE PRINCIPALE ----------------------------------------------------------------------------------------
        # Creation de la fenetre contenant la scrooll bar et canvas contenant lui meme le tableau
        self.defineMainFrame()

        # Titres des colonnes
        # ---------- frame en-tete tableau
        self.enTeteFrame = Frame(self.tableFrame, bd=1, bg='light slate gray', width=int(self.scaleFactor*880), height=int(self.scaleFactor*30),
                                 highlightthickness=1, highlightbackground='navy')
        self.enTeteFrame.pack_propagate(False)
        self.enTeteFrame.pack(side=TOP, padx=0, pady=0)
        # ---------- en-têtes
        entete_confs = [{"name": "Titre", "w": 410},
                        {"name": "Rev", "w": 50},
                        {"name": "Redaction", "w": 100},
                        {"name": "Relecture", "w": 100},
                        {"name": "Signature", "w": 100},
                        {"name": "Diffusion", "w": 100}]

        for d in entete_confs:
            titreFrame = Frame(self.enTeteFrame, bd=1, bg='light slate gray', width=d["w"], height=int(self.scaleFactor*20),
                               highlightthickness=0, highlightbackground='navy')
            titreFrame.pack_propagate(False)
            titreFrame.pack(side=LEFT, padx=0, pady=0)
            titreLabel = Label(titreFrame, text=d["name"], foreground='navy', bg='light slate gray',
                               font='arial 9 bold')
            titreLabel.pack()

        # SUPPRIME TOUS LES DOCS EXISTANTS
        d = self.tableFrame.children.copy()
        for widget_n in d:
            if self.tableFrame.children[widget_n] != self.enTeteFrame:
                self.tableFrame.children[widget_n].destroy()

        # CHARGE LA NOUVELLE LISTE DE DOCUMENTS
        # -------------------- Examen des parametres exterieurs
        # ----------------------------- Responsabilite
        activeResp = []
        peopleState = []
        i = 0
        for p in self.peoples:
                if p.var.get() == 1:
                    activeResp.append(self.persListFil[i])
                i += 1

        # ------------------- Chargement complets
        j = 0
        for i in range(0, len(self.docListFil)):
            docTitle = self.docListFil[i].split('.')[0]

            # CHARGEMENT DES PARAMETRES VARIABLES
            fileToAnalyse = "DocList" + '\\' + self.docListFil[i]

            activateRedac = 0
            listRedac = {}
            activateRelec = 0
            listRelec = {}
            activateSign = 0
            listSign = {}
            activateDiff = 0
            listDiff = {}

            # RECUPERATION DE TOUTE LES DATAS UTILES ANS LES .TXT
            with open(fileToAnalyse, 'r') as readFile:
                for line in readFile:
                    if line.startswith('STATUTENCOURS'):
                        curState = int(line.split(' ')[1].replace('\n', ''))
                    elif line.startswith('VERSIONENCOURS'):
                        curVer = line.split(' ')[1].replace('\n', '')
                    elif line.startswith('DATEDEDIFFUSIONREVPREC'):
                        oldDate = line.split(' ')[1].replace('\n', '')
                    elif line.startswith('COMMENTAIRE1'):
                        commentaire1 = line.replace('COMMENTAIRE1 ', '').replace('\n', '')
                    elif line.startswith('COMMENTAIRE2'):
                        commentaire2 = line.replace('COMMENTAIRE2 ', '').replace('\n', '')
                    elif line.startswith('COMMENTAIRE3'):
                        commentaire3 = line.replace('COMMENTAIRE3 ', '').replace('\n', '')
                    elif line.startswith('COMMENTAIRE4'):
                        commentaire4 = line.replace('COMMENTAIRE4 ', '').replace('\n', '')
                    elif line.startswith('COMMENTAIRE5'):
                        commentaire5 = line.replace('COMMENTAIRE5 ', '').replace('\n', '')
                    elif line.startswith('REDACTION'):
                        activateRedac = 1
                        activateRelec = 0
                        activateSign = 0
                        activateDiff = 0
                    elif line.startswith('RELECTURE'):
                        activateRedac = 0
                        activateRelec = 1
                        activateSign = 0
                        activateDiff = 0
                    elif line.startswith('SIGNATURE'):
                        activateRedac = 0
                        activateRelec = 0
                        activateSign = 1
                        activateDiff = 0
                    elif line.startswith('DIFFUSION'):
                        activateRedac = 0
                        activateRelec = 0
                        activateSign = 0
                        activateDiff = 1
                    elif activateRedac == 1:
                        splitLine = line.split(' ')
                        listRedac[splitLine[0]] = {'name': splitLine[0], 'statut': splitLine[1]}
                    elif activateRelec == 1:
                        splitLine = line.split(' ')
                        listRelec[splitLine[0]] = {'name': splitLine[0], 'statut': splitLine[1]}
                    elif activateSign == 1:
                        splitLine = line.split(' ')
                        listSign[splitLine[0]] = {'name': splitLine[0], 'statut': splitLine[1]}
                    elif activateDiff == 1:
                        splitLine = line.split(' ')
                        listDiff[splitLine[0]] = {'name': splitLine[0], 'statut': splitLine[1]}

            # UTILISATION DES DATAS ET DEFINITION DES OBJETS DE LA CLASSE
            dico = {'docTitle': docTitle,
                    'curState': curState,
                    'curVer': curVer,
                    'oldDate': oldDate,
                    'listRedac': listRedac,
                    'listRelec': listRelec,
                    'listSign': listSign,
                    'listDiff': listDiff,
                    'commentaires': [commentaire1, commentaire2, commentaire3, commentaire4, commentaire5]}

            trigerActiveResp = 0
            for people in dico['listRedac']:
                if people in activeResp:
                    trigerActiveResp = 1

            if trigerActiveResp == 1:
                # PLACEMENT DE LA NC DANS LE TABLEAU
                # Creation de la fenetre
                docMainWindow = Frame(self.tableFrame, bd=1, bg='alice blue', width=int(self.scaleFactor*880), height=int(self.scaleFactor*30), highlightthickness=1,
                                      highlightbackground='navy')
                docMainWindow.pack_propagate(False)
                docMainWindow.pack(side=TOP, padx=0, pady=0)
                # ------------- Bouton du titre
                titleButton = Button(docMainWindow, text=docTitle, width=int(self.scaleFactor*57), height=int(self.scaleFactor*30), state=NORMAL,
                                     font='arial 9 bold', foreground='gray10', anchor=W)
                o = DocMenu(dico)
                self.sub_windows.append(o)
                titleButton.config(command=self.sub_windows[j].show)
                titleButton.pack_propagate(False)
                titleButton.pack(side=LEFT, pady=0, padx=0)
                # ------------- Revision
                revFrame = Frame(docMainWindow, bd=1, bg='alice blue', width=int(self.scaleFactor*55), height=int(self.scaleFactor*20), highlightthickness=0,
                                 highlightbackground='navy')
                revFrame.pack_propagate(False)
                revFrame.pack(side=LEFT, padx=0, pady=0)
                revLabel = Label(revFrame, text=curVer, foreground='gray10', bg='alice blue', font='arial 9 bold')
                revLabel.pack()
                # ------------ Redaction
                redacFrame = Frame(docMainWindow, bd=1, width=int(self.scaleFactor*96), height=int(self.scaleFactor*20), highlightthickness=0)
                if curState <= 1:
                    redacFrame.config(bg='red3')
                else:
                    redacFrame.config(bg='lawn green')
                redacFrame.pack_propagate(False)
                redacFrame.pack(side=LEFT, padx=2, pady=0)
                # ------------ Relecture
                relecFrame = Frame(docMainWindow, bd=1, width=int(self.scaleFactor*96), height=int(self.scaleFactor*20), highlightthickness=0)
                if curState <= 2:
                    relecFrame.config(bg='red3')
                else:
                    relecFrame.config(bg='lawn green')
                relecFrame.pack_propagate(False)
                relecFrame.pack(side=LEFT, padx=2, pady=0)
                # ------------ Signature
                signFrame = Frame(docMainWindow, bd=1, width=int(self.scaleFactor*96), height=int(self.scaleFactor*20), highlightthickness=0)
                if curState <= 3:
                    signFrame.config(bg='red3')
                else:
                    signFrame.config(bg='lawn green')
                signFrame.pack_propagate(False)
                signFrame.pack(side=LEFT, padx=2, pady=0)
                # ------------ diffusion
                diffFrame = Frame(docMainWindow, bd=1, width=int(self.scaleFactor*96), height=int(self.scaleFactor*20), highlightthickness=0)
                if curState <= 4:
                    diffFrame.config(bg='red3')
                else:
                    diffFrame.config(bg='lawn green')
                diffFrame.pack_propagate(False)
                diffFrame.pack(side=LEFT, padx=2, pady=0)
                j += 1

    def defineMainFrame(self):

        # CREATION DE LA FENETRE CONTENANT DU CANVAS DU TABLEAU RESUME ET DE LA SCROLL BAR ASSOCIEE

        self.mainFrame = Frame(self.mainWindow, bg='alice blue', width=int(self.scaleFactor*930), height=int(self.scaleFactor*630))
        self.canvasContainer = Canvas(self.mainFrame, bg='alice blue', width=int(self.scaleFactor*900), height=int(self.scaleFactor*630))
        self.defilY = Scrollbar(self.mainFrame, orient='vertical', command=self.canvasContainer.yview)
        self.tableFrame = LabelFrame(self.canvasContainer, text='Tableau Resume', labelanchor='nw', bd=5,
                                     bg='alice blue', borderwidth=2, width=int(self.scaleFactor*900), height=int(self.scaleFactor*630), highlightthickness=5,
                                     highlightbackground='alice blue', font='arial 9 italic', foreground='navy')

        self.defilY.bind("<Configure>",
                         lambda e: self.canvasContainer.configure(scrollregion=self.canvasContainer.bbox("all")))

        self.canvasContainer.create_window((0, 0), window=self.tableFrame, anchor='nw')
        self.canvasContainer.configure(yscrollcommand=self.defilY.set)

        self.mainFrame.pack(side=LEFT, padx=10)
        self.canvasContainer.pack(side=LEFT)
        self.defilY.pack(side='right', fill='y')

    def defineMenuBar(self):
        # ---------Menu
        menuBar = Menu(self.mainWindow)
        self.mainWindow.config(menu=menuBar)

        menuDoc = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Document', menu=menuDoc)
        menuDoc.add_command(label='Ajouter', command=DocAdd().show)
        menuDoc.add_command(label='Supprimer', command=DocSup(self.docListFil).show)

        menuPers = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Personne', menu=menuPers)
        menuPers.add_command(label='Ajouter', command=PersAdd().show)
        menuPers.add_command(label='Supprimer', command=PersSup(self.persListFil).show)
        menuPers.add_separator()

        for i in range(0, len(self.persListFil)):
            title = self.persListFil[i].split('.')[0]
            menuPers.add_command(label=title, command=PersMenu(title, self.docListFil).show)

    def destroyWindow(self):
        for window in self.windowList:
            window.destroy()

    def onClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):

            fileToWrite = 'UseFile\\' + 'indicOuverture'
            fileToCreate = open(fileToWrite, "w+")

            fileToCreate.write('0')
            fileToCreate.close()

            self.mainWindow.destroy()


if __name__ == "__main__":
    #
    # ---------------------------------------------------------------------------------------------------------------
    # OPEN THE MAIN WINDOW AND COLLECT STATUS
    my_main_window = MainWindow()
    #
    # ----------------------------------------------------------------------------------------------------------------