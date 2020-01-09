
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import ctypes
import datetime


class DocMenu(object):
    def __init__(self, dico=None):
        # REUCUPERATION DE LA TAILLE DE LECRAN
        usr32 = ctypes.windll.user32
        largeurEcran = usr32.GetSystemMetrics(0)
        hauteurEcran = usr32.GetSystemMetrics(1)

        self.scaleFactor = float(int(largeurEcran)/1366)

        # RECUPERATION DU DICTIONNAIRE PRINCIPAL
        self.d = dico
        '''
        dico = {'docTitle': docTitle,
                    'curState': curState,
                    'curVer': curVer,
                    'oldDate': oldDate,
                    'listRedac': listRedac,
                    'listRelec': listRelec,
                    'listSign': listSign,
                    'listDiff': listDiff,
                    'commentaires': [commentaire1, commentaire2, commentaire3, commentaire4, commentaire5]}
        '''

        # DEFINITION DE PARAMETRES
        if self.d["curState"] == 1:
            self.docState = 'En redaction'
            self.PersListToTake = self.d["listRedac"]
            self.stateToComeText = 'En relecture'
        elif self.d["curState"] == 2:
            self.docState = 'En relecture'
            self.PersListToTake = self.d["listRelec"]
            self.stateToComeText = 'En Signature'
        elif self.d["curState"] == 3:
            self.docState = 'En signature'
            self.PersListToTake = self.d["listSign"]
            self.stateToComeText = 'En Diffusion'
        elif self.d["curState"] == 4:
            self.docState = 'En diffusion'
            self.PersListToTake = self.d["listDiff"]
            self.stateToComeText = 'Diffuser'
        elif self.d["curState"] == 5:
            self.docState = 'Rev ' + self.d["curVer"] + ' diffusée le ' + self.d["oldDate"][-1]
            self.PersListToTake = {}
            self.stateToComeText = 'Nouvelle Revision'

    def show(self):

        # Cette fonction permet d'ouvrir une fenêtre DocMenu et stock les checkbutton et les commentaires

        print("DocMenu.show")
        self.docWindow = Toplevel()

        self.docWindow.title(self.d['docTitle'])
        decalX = self.scaleFactor * 220
        decalY = self.scaleFactor * 110
        self.docWindow.geometry('+%d+%d' % (decalX, decalY))
        self.docWindow['bg'] = 'light slate gray'

        # ACTIONS ---------------------------------------------------------------------------------------------
        # --------- Creation de la fenetre
        actionFrame = LabelFrame(self.docWindow, text='Action', labelanchor='nw', bd=5, bg='alice blue',
                                 borderwidth=2, width=int(self.scaleFactor*300), height=int(self.scaleFactor*70), highlightthickness=5,
                                 highlightbackground='alice blue', font='arial 9 italic', foreground='navy')
        actionFrame.pack(side=TOP, padx=10, pady=5)

        # --------- Boutton SAUVEGARDER
        actualiseButton = Button(actionFrame, text='SAUVEGARDER ET QUITTER',
                                 command=self.saveAndQuit, state=NORMAL, font='arial 10 bold', foreground='deep pink',
                                 background='black')
        actualiseButton.pack(side=TOP, pady=10, padx=20)

        # AFFICHAGE DE LA NC
        # placement fenetre NC
        docFrame = LabelFrame(self.docWindow, text=self.d["docTitle"], labelanchor='nw', bd=5, bg='alice blue',
                              borderwidth=2, width=int(self.scaleFactor*950), height=int(self.scaleFactor*400), highlightthickness=5,
                              highlightbackground='alice blue', font='arial 10 bold', foreground='navy')
        #docFrame.pack_propagate(False)
        docFrame.pack(side=TOP, padx=10, pady=5)

        # Statut de la fenetre
        if self.d["curState"] == 5:
            # --------- Creation de la fenetre
            stateFrame = LabelFrame(docFrame, text='Statut en cours :', labelanchor='nw', bd=5, bg='alice blue',
                                    borderwidth=2, width=int(self.scaleFactor*400), height=int(self.scaleFactor*100), highlightthickness=2,
                                    highlightbackground='alice blue', font='arial 8 italic', relief=FLAT)
            # stateFrame.pack_propagate(False)
            stateFrame.pack(side=LEFT, pady=5, padx=10)

            # --------- Ecriture du statut
            frameState = Label(stateFrame, text=self.docState, bg='alice blue', font='arial 9 bold')
            frameState.pack(side=TOP, pady=5, padx=10)

            # --------- Supplement si state 5
            indicationForChange = Label(stateFrame, bg='alice blue', font='arial 7 italic',
                                        text='Merci de supprimer ce document une fois archivé dans la gestion de '
                                             'configuration\nPour créer une nouvelle revision, ajouter un nouveau '
                                             'document')
            indicationForChange.pack(side=TOP, pady=5, padx=10)

        else:
            # --------- Creation de la fenetre
            stateFrame = LabelFrame(docFrame, text='Statut en cours :', labelanchor='nw', bd=5, bg='alice blue',
                                    borderwidth=2, width=int(self.scaleFactor*150), height=int(self.scaleFactor*50), highlightthickness=2,
                                    highlightbackground='alice blue', font='arial 8 italic', relief=FLAT)
            stateFrame.pack_propagate(False)
            stateFrame.pack(side=LEFT, pady=5, padx=5)

            # --------- Ecriture du statut
            frameState = Label(stateFrame, text=self.docState, bg='alice blue', font='arial 9 bold')
            frameState.pack(side=TOP, pady=2, padx=10)

        if self.d["curState"] != 5:
            # Personne associees :
            # --------- Creation de la fenetre
            frameContainer = Frame(docFrame, bg='alice blue', width=int(150), height=int(self.scaleFactor*50))
            canvasContainer = Canvas(frameContainer, bg='alice blue', width=int(150), height=int(self.scaleFactor*130), highlightthickness=0)
            defilY = Scrollbar(frameContainer, orient='vertical', command=canvasContainer.yview)

            peopleText = 'Personnes concernees'
            peopleFrame = LabelFrame(frameContainer, text=peopleText, labelanchor='nw', bd=5, bg='alice blue',
                                     borderwidth=1, width=int(self.scaleFactor*150), height=int(self.scaleFactor*130), highlightthickness=2,
                                     highlightbackground='alice blue', font='arial 8 italic', relief=GROOVE)

            defilY.bind("<Configure>", lambda e: canvasContainer.configure(scrollregion=canvasContainer.bbox("all")))
            canvasContainer.configure(yscrollcommand=defilY.set)
            canvasContainer.create_window((10, 5), window=peopleFrame, anchor='nw')

            frameContainer.pack(side=LEFT)
            canvasContainer.pack(side=LEFT)
            defilY.pack(side='right', fill='y')

            # --------- Ligne pour les personnes
            self.peoples = []
            i = 0

            for cle in self.PersListToTake.keys():
                peopleName = self.PersListToTake[cle]['name']
                checkValue = IntVar()
                if self.PersListToTake[cle]['statut'] == 'OK\n':
                    checkValue.set(1)
                    self.peoples.append(Checkbutton(peopleFrame, text=peopleName, variable=checkValue, onvalue=1,
                                                    offvalue=0, bg='alice blue', command=self.triggerNewRev))
                    self.peoples[i].select()

                else:
                    self.peoples.append(Checkbutton(peopleFrame, text=peopleName, variable=checkValue, onvalue=1,
                                                    offvalue=0, bg='alice blue', command=self.triggerNewRev))
                    self.peoples[i].deselect()

                self.peoples[i].var = checkValue
                self.peoples[i].pack(side=TOP, padx=20, pady=0, anchor=W)
                i += 1

            # Statut a venir
            # --------- Creation de la fenetre
            if self.d["curState"] == 4:
                stateToComeFrame = LabelFrame(docFrame, text='Date de diffusion : \n(format dd/mm/aaaa)', labelanchor='n', bd=5, bg='alice blue',
                                              borderwidth=2, width=int(self.scaleFactor*150), height=int(self.scaleFactor*100), highlightthickness=2,
                                              highlightbackground='alice blue', font='arial 8 italic', relief=FLAT)

            else:
                stateToComeFrame = LabelFrame(docFrame, text='Changer de statut :', labelanchor='nw', bd=5, bg='alice blue',
                                              borderwidth=2, width=int(self.scaleFactor*150), height=int(self.scaleFactor*50), highlightthickness=2,
                                              highlightbackground='alice blue', font='arial 8 italic', relief=FLAT)
            stateToComeFrame.pack_propagate(False)
            stateToComeFrame.pack(side=LEFT, pady=5, padx=10)

            # --------- Boutton du changement de statut
            verifRev = 1
            for cle in self.PersListToTake.keys():
                peopleStatut = self.PersListToTake[cle]['statut']
                if peopleStatut == 'NOK\n':
                    verifRev = 0

            if self.d["curState"] == 4:
                value = StringVar()
                self.changeStateEntry = Entry(stateToComeFrame, textvariable=value, font='arial 7',
                                                highlightthickness=0)
                self.changeStateEntry.var = value
                self.changeStateEntry.pack_propagate(False)
                self.changeStateEntry.pack(pady=5, padx=10)

            if verifRev == 0:
                self.changeStateButton = Button(stateToComeFrame, text=self.stateToComeText, state=DISABLED,
                                                command=self.changeState, font='arial 9')
            else:
                self.changeStateButton = Button(stateToComeFrame, text=self.stateToComeText, command=self.changeState,
                                                font='arial 9')

            self.changeStateButton.pack_propagate(False)
            self.changeStateButton.pack(pady=5, padx=10)

        # Espace commentaire
        # --------- Creation de la fenetre
        CommentaryFrame = LabelFrame(docFrame, text='Commentaires', labelanchor='nw', bd=5, bg='alice blue',
                                     borderwidth=1, width=int(self.scaleFactor*500), height=int(110), highlightthickness=2,
                                     highlightbackground='alice blue', font='arial 8 italic', relief=GROOVE)
        CommentaryFrame.pack_propagate(False)
        CommentaryFrame.pack(side=LEFT, pady=5, padx=10)

        # --------- Zones de saisie
        self.CommentaryArea = []

        for i in range(5):
            value = StringVar()
            self.CommentaryArea.append(Entry(CommentaryFrame, textvariable=value, font='arial 7',
                                             highlightthickness=0))

            self.CommentaryArea[i].var = value
            self.CommentaryArea[i].insert(0, self.d["commentaires"][i])
            self.CommentaryArea[i].pack(fill='x')
        # END openDocMenu
        
    def saveAndQuit(self):

        print("DocMenu.saveAndQuit")

        if self.d["curState"] != 5:
            peopleState = []
            for p in self.peoples:
                peopleState.append(p.var.get())

        commentList = []
        for c in self.CommentaryArea:
            commentList.append(c.var.get())

        docTitle = self.d["docTitle"]
        fileToAnalyse = 'DocList\\' + docTitle

        lineToWrite = []
        triggerReWrite = 0
        incrPeopleState = 0

        with open(fileToAnalyse, 'r') as readFile:
            for line in readFile:

                if self.d["curState"] == 1:
                    if line.startswith('REDACTION'):
                        triggerReWrite = 1
                        lineToWrite.append(line)
                    elif line.startswith('RELECTURE'):
                        triggerReWrite = 0
                        lineToWrite.append(line)
                    elif line.startswith('COMMENTAIRE1'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[0] + '\n')
                    elif line.startswith('COMMENTAIRE2'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[1] + '\n')
                    elif line.startswith('COMMENTAIRE3'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[2] + '\n')
                    elif line.startswith('COMMENTAIRE4'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[3] + '\n')
                    elif line.startswith('COMMENTAIRE5'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[4] + '\n')

                    else:
                        if triggerReWrite == 0:
                            lineToWrite.append(line)
                        else:
                            NameToReWrite = str(line.split(' ')[0])
                            if peopleState[incrPeopleState] == 1:
                                lineToWrite.append(NameToReWrite + ' OK\n')
                            else:
                                lineToWrite.append(NameToReWrite + ' NOK\n')
                            incrPeopleState += 1

                elif self.d["curState"] == 2:
                    if line.startswith('RELECTURE'):
                        triggerReWrite = 1
                        lineToWrite.append(line)
                    elif line.startswith('SIGNATURE'):
                        triggerReWrite = 0
                        lineToWrite.append(line)
                    elif line.startswith('COMMENTAIRE1'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[0] + '\n')
                    elif line.startswith('COMMENTAIRE2'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[1] + '\n')
                    elif line.startswith('COMMENTAIRE3'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[2] + '\n')
                    elif line.startswith('COMMENTAIRE4'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[3] + '\n')
                    elif line.startswith('COMMENTAIRE5'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[4] + '\n')
                    else:
                        if triggerReWrite == 0:
                            lineToWrite.append(line)
                        else:
                            NameToReWrite = str(line.split(' ')[0])
                            if peopleState[incrPeopleState] == 1:
                                lineToWrite.append(NameToReWrite + ' OK\n')
                            else:
                                lineToWrite.append(NameToReWrite + ' NOK\n')
                            incrPeopleState += 1

                elif self.d["curState"] == 3:
                    if line.startswith('SIGNATURE'):
                        triggerReWrite = 1
                        lineToWrite.append(line)
                    elif line.startswith('DIFFUSION'):
                        triggerReWrite = 0
                        lineToWrite.append(line)
                    elif line.startswith('COMMENTAIRE1'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[0] + '\n')
                    elif line.startswith('COMMENTAIRE2'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[1] + '\n')
                    elif line.startswith('COMMENTAIRE3'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[2] + '\n')
                    elif line.startswith('COMMENTAIRE4'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[3] + '\n')
                    elif line.startswith('COMMENTAIRE5'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[4] + '\n')
                    else:
                        if triggerReWrite == 0:
                            lineToWrite.append(line)
                        else:
                            NameToReWrite = str(line.split(' ')[0])
                            if peopleState[incrPeopleState] == 1:
                                lineToWrite.append(NameToReWrite + ' OK\n')
                            else:
                                lineToWrite.append(NameToReWrite + ' NOK\n')
                            incrPeopleState += 1

                elif self.d["curState"] == 4:
                    if line.startswith('DIFFUSION'):
                        triggerReWrite = 1
                        lineToWrite.append(line)
                    elif line.startswith('STATUTENCOURS'):
                        triggerReWrite = 0
                        lineToWrite.append(line)
                    elif line.startswith('COMMENTAIRE1'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[0] + '\n')
                    elif line.startswith('COMMENTAIRE2'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[1] + '\n')
                    elif line.startswith('COMMENTAIRE3'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[2] + '\n')
                    elif line.startswith('COMMENTAIRE4'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[3] + '\n')
                    elif line.startswith('COMMENTAIRE5'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[4] + '\n')
                    else:
                        if triggerReWrite == 0:
                            lineToWrite.append(line)
                        else:
                            NameToReWrite = str(line.split(' ')[0])
                            if peopleState[incrPeopleState] == 1:
                                lineToWrite.append(NameToReWrite + ' OK\n')
                            else:
                                lineToWrite.append(NameToReWrite + ' NOK\n')
                            incrPeopleState += 1

                else:
                    if line.startswith('COMMENTAIRE1'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[0] + '\n')
                    elif line.startswith('COMMENTAIRE2'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[1] + '\n')
                    elif line.startswith('COMMENTAIRE3'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[2] + '\n')
                    elif line.startswith('COMMENTAIRE4'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[3] + '\n')
                    elif line.startswith('COMMENTAIRE5'):
                        StartToReWrite = str(line.split(' ')[0])
                        lineToWrite.append(StartToReWrite + ' ' + commentList[4] + '\n')
                    else:
                        lineToWrite.append(line)

        readFile.close()

        fileToWrite = fileToAnalyse
        currentFile = open(fileToWrite, "w+")

        for i in range(0, len(lineToWrite)):
            currentFile.write(lineToWrite[i])

        currentFile.close()

        self.docWindow.destroy()

        # END saveAndQuit

    def changeState(self):

        print('DocMenu.changeState')

        # RECUPERATION DE LA DATE :
        actualDate = str(str(datetime.datetime.now().day) + '/' + str(datetime.datetime.now().month) + '/' +
                         str(datetime.datetime.now().year))

        docTitle = self.d["docTitle"]
        fileToAnalyse = 'DocList\\' + docTitle

        lineToWrite = []

        with open(fileToAnalyse, 'r') as readFile:
            for line in readFile:
                if self.d['curState'] == 4:
                    if line.startswith('STATUTENCOURS'):
                        lineToWrite.append('STATUTENCOURS ' + str(int(line.split(' ')[1])+1) + '\n')
                    elif line.startswith('DATEDEDIFFUSIONREVPREC'):
                        lineToWrite.append(line.replace('\n', '') + ' ' + str(self.changeStateEntry.var.get()) + '\n')
                    else:
                        lineToWrite.append(line)
                elif self.d['curState'] == 1:
                    if line.startswith('STATUTENCOURS'):
                        lineToWrite.append('STATUTENCOURS ' + str(int(line.split(' ')[1])+1) + '\n')
                    elif line.startswith('DATEDEDIFFUSIONREVPREC'):
                        lineToWrite.append('DATEDEDIFFUSIONREVPREC ' + actualDate + '\n')
                    else:
                        lineToWrite.append(line)
                else:
                    if line.startswith('STATUTENCOURS'):
                        lineToWrite.append('STATUTENCOURS ' + str(int(line.split(' ')[1])+1) + '\n')
                    elif line.startswith('DATEDEDIFFUSIONREVPREC'):
                        lineToWrite.append(line.replace('\n', '') + ' ' + actualDate + '\n')
                    else:
                        lineToWrite.append(line)


        readFile.close()

        fileToWrite = fileToAnalyse
        currentFile = open(fileToWrite, "w+")

        for i in range(0, len(lineToWrite)):
            currentFile.write(lineToWrite[i])

        # FENETRE POP UP AVEC CONSIGN UTILISATEUR
        self.popup = Toplevel(padx=10, pady=10)
        self.popup.title('Changement de statut')
        decalX = self.scaleFactor * 350
        decalY = self.scaleFactor * 200
        self.popup.geometry('+%d+%d' % (decalX, decalY))
        self.popup['bg'] = 'alice blue'

        msg = Message(self.popup, text='Changement de statut bien pris en compte', anchor=CENTER, bg ='alice blue',
                      width=int(self.scaleFactor*250), font='arial 9 bold')
        msg.pack(side=TOP, pady=5)
        msg2 = Message(self.popup,
                       text='La fenetre liée au menu va se fermée \nMerci d actualiser la fenetre principale',
                       anchor=CENTER, bg ='alice blue', width=int(self.scaleFactor*250), font='arial 9')
        msg2.pack(side=TOP, pady=0)

        self.windowList = [self.popup, self.docWindow]

        but = Button(self.popup, text='OK', command=self.destroyWindow, state=NORMAL, width=int(self.scaleFactor*20),
                     font='arial 10 bold', foreground='black', bg='grey60')
        but.pack(side=TOP, pady=5)

    def triggerNewRev(self):

        print('DocMenu.triggerNewRev')

        self.triggerValue = 1
        for p in self.peoples:
            if p.var.get() == 0:
                self.triggerValue = 0

        if self.triggerValue == 1:
            self.changeStateButton.config(state=NORMAL)
        else:
            self.changeStateButton.config(state=DISABLED)

    def destroyWindow(self):
        for window in self.windowList:
            window.destroy()