from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os


class DocAdd(object):

    def __init__(self):
        tbc = 0

    def show(self):
        print('DocAdd.show')

        self.docAddWindow = Toplevel()

        self.docAddWindow.title('Ajout de document')
        self.docAddWindow.geometry('500x500+80+100')
        self.docAddWindow['bg'] = 'light slate gray'

        # ACTIONS ---------------------------------------------------------------------------------------------
        # --------- Creation de la fenetre
        actionFrame = LabelFrame(self.docAddWindow, text='Action', labelanchor='nw', bd=5, bg='alice blue',
                                 borderwidth=2, width=250, height=70, highlightthickness=5,
                                 highlightbackground='alice blue', font='arial 9 italic', foreground='navy')
        actionFrame.pack_propagate(False)
        actionFrame.pack(side=TOP, padx=5, pady=5)

        # --------- Boutton SUPPRIMER
        actualiseButton = Button(actionFrame, text='AJOUTER ET QUITTER', state=NORMAL, font='arial 10 bold',
                                 foreground='chartreuse3', background='black', command=self.addFile)
        actualiseButton.pack(side=TOP, pady=5, padx=20)

        # FENETRE PRINCIPALE
        self.mainFrame = Frame(self.docAddWindow, bg='alice blue', width=450, height=500, highlightthickness=0)
        self.docInfoFrame = LabelFrame(self.mainFrame, text='Informations pour la création du document',
                                       labelanchor='nw', bd=5, bg='alice blue', borderwidth=2, width=450, height=400,
                                       highlightthickness=0, highlightbackground='alice blue', foreground='navy',
                                       font='arial 9 italic bold')
        self.mainFrame.pack(side=TOP, pady=10)
        self.docInfoFrame.pack(padx=5, pady=5)

        # Fenetre de titre :
        self.docTitleFrame = LabelFrame(self.docInfoFrame, text='Titre du document et revision', labelanchor='nw', bd=5,
                                        bg='alice blue', borderwidth=2, width=430, height=50, highlightthickness=0,
                                        highlightbackground='alice blue', font='arial 9 italic', foreground='navy')

        self.docTitleFrame.pack_propagate(False)
        self.docTitleFrame.pack(padx=2, pady=2)

        # TITRE
        value = StringVar()
        self.docTitleEntry = Entry(self.docTitleFrame, textvariable=value, font='arial 8',
                                   highlightthickness=0, width=55)
        self.docTitleEntry.var = value
        self.docTitleEntry.insert(0, 'titre')
        self.docTitleEntry.pack(side=LEFT, padx=2, pady=2)

        # REV
        value = StringVar()
        self.docRevEntry = Entry(self.docTitleFrame, textvariable=value, font='arial 8',
                                 highlightthickness=0, width=10)
        self.docRevEntry.var = value
        self.docRevEntry.insert(0, 'rev')
        self.docRevEntry.pack(side=RIGHT, padx=2, pady=2)

        # Fenetre Personne
        self.canvasContainer = Canvas(self.docInfoFrame, bg='alice blue', width=450, height=400, highlightthickness=0)
        self.defilY = Scrollbar(self.docInfoFrame, orient='vertical', command=self.canvasContainer.yview)

        self.mainDocPersFrame = LabelFrame(self.canvasContainer, foreground='navy', labelanchor='nw',
                                           text='Personnes concernées - cocher chacune des categories',
                                           bg='alice blue',  width=430, height=430, font='arial 9 italic',
                                           borderwidth=2, highlightthickness=0, highlightbackground='alice blue')
        self.defilY.bind("<Configure>",
                         lambda e: self.canvasContainer.configure(scrollregion=self.canvasContainer.bbox("all")))
        self.canvasContainer.configure(yscrollcommand=self.defilY.set)
        self.canvasContainer.create_window((20, 5), window=self.mainDocPersFrame, anchor='nw')

        self.canvasContainer.pack(side=LEFT)
        self.defilY.pack(side=RIGHT, fill='y')

        # ------------------- Personnes en cours sur le projets - liste complète
        self.persListFilBrut = sorted(os.listdir("PersList"))
        self.persListFil = []
        for pers in self.persListFilBrut:
            self.persListFil.append(pers.split('.')[0])

        # -------------- Redacteur
        self.frameTitleList = ['Redacteur',
                               'Relecteur',
                               'Signataire',
                               'Diffuseur']

        self.frameTitle = []
        self.doc = {}
        j=0
        for title in self.frameTitleList:
            self.frameTitle.append(LabelFrame(self.mainDocPersFrame, foreground='grey20', labelanchor='nw',
                                              text=title, bd=5, bg='alice blue', font='arial 10 bold', borderwidth=0,
                                              highlightthickness=0, highlightbackground='alice blue'))
            i = 0
            self.doc[j] = []

            for pers in self.persListFil:
                checkValue = IntVar()
                self.doc[j].append(Checkbutton(self.frameTitle[j], text=pers, variable=checkValue, onvalue=1,
                                            offvalue=0, bg='alice blue', font='arial 9', width=20, anchor=W))

                self.doc[j][i].var = checkValue
                self.doc[j][i].pack(side=TOP, padx=20, pady=0)
                i += 1
            j += 1

        self.frameTitle[0].grid(row=0, column=0, padx=5, pady=5)
        self.frameTitle[1].grid(row=1, column=0, padx=5, pady=5)
        self.frameTitle[2].grid(row=0, column=1, padx=5, pady=5)
        self.frameTitle[3].grid(row=1, column=1, padx=5, pady=5)

    def addFile(self):
        print('DocAdd.addFile')

        # Acquisition titre et rev
        self.docTitle = self.docTitleEntry.var.get()
        self.docRev = self.docRevEntry.var.get()

        # Acquisition personnes concernees
        self.persListSelec = {}
        j=0

        for cat in self.frameTitleList:
            self.persListSelec[j] = []
            i=0

            for pers in self.persListFil:
                if self.doc[j][i].var.get() == 1:

                    self.persListSelec[j].append(self.persListFil[i])

                i += 1
            j += 1

        # Ouverture nouveau fichier
        fileToWrite = 'DocList\\' + self.docTitle
        fileToCreate = open(fileToWrite, "w+")

        fileToCreate.write('REDACTION\n')
        for pers in self.persListSelec[0]:
            fileToCreate.write(pers + ' NOK\n')
        fileToCreate.write('RELECTURE\n')
        for pers in self.persListSelec[1]:
            fileToCreate.write(pers + ' NOK\n')
        fileToCreate.write('SIGNATURE\n')
        for pers in self.persListSelec[2]:
            fileToCreate.write(pers + ' NOK\n')
        fileToCreate.write('DIFFUSION\n')
        for pers in self.persListSelec[3]:
            fileToCreate.write(pers + ' NOK\n')
        fileToCreate.write('STATUTENCOURS 1\n')
        fileToCreate.write('VERSIONENCOURS ' + self.docRev + '\n')
        fileToCreate.write('DATEDEDIFFUSIONREVPREC 000000\n')
        fileToCreate.write('COMMENTAIRE1 \n')
        fileToCreate.write('COMMENTAIRE2 \n')
        fileToCreate.write('COMMENTAIRE3 \n')
        fileToCreate.write('COMMENTAIRE4 \n')
        fileToCreate.write('COMMENTAIRE5 \n')

        fileToCreate.close()

        # FENETRE POP UP AVEC CONSIGN UTILISATEUR
        self.popup = Toplevel()
        self.popup.title('Ajout terminee')
        self.popup.geometry('300x120+450+300')
        self.popup['bg'] = 'alice blue'

        msg = Message(self.popup, text='Nouveau document bien ajoute', anchor=CENTER, bg='alice blue', width=250,
                      font='arial 9 bold')
        msg.pack(side=TOP, pady=5)
        msg2 = Message(self.popup, anchor=CENTER, bg='alice blue', width=250, font='arial 9',
                       text='La fenetre liée au menu va se fermée \nMerci d actualiser la fenetre principale')
        msg2.pack(side=TOP, pady=0)

        self.windowList = [self.popup, self.docAddWindow]

        but = Button(self.popup, text='OK', command=self.destroyWindow, state=NORMAL, width=20,
                     font='arial 10 bold', foreground='black', bg='grey60')
        but.pack(side=TOP, pady=5)

    def destroyWindow(self):
        for window in self.windowList:
            window.destroy()
