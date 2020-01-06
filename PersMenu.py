from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os


class PersMenu(object):

    def __init__(self, pers=None, docList=None):
        self.persSelec = pers
        self.docList = docList

        # Choper les noms entiers
        self.persListFil = sorted(os.listdir("PersList"))
        for pers in self.persListFil:
            if str(pers) == str(self.persSelec):
                fileToAnalyse = 'PersList\\' + pers
                firstLine = 0
                with open(fileToAnalyse, 'r') as readFile:
                    for line in readFile:
                        if firstLine == 0:
                            self.fullName = str(line)
                            firstLine += 1

    def show(self):

        # Creation du collecteur de data
        self.fullData = {}
        self.catList = ['REDACTION', 'RELECTURE', 'SIGNATURE', 'DIFFUSION']
        for cat in self.catList:
            self.fullData[cat] = []

        print("PersMenu.show")

        self.persWindow = Toplevel()

        self.persWindow.title(self.fullName + ' - Menu des actions')
        self.persWindow.geometry('600x500+80+100')
        self.persWindow['bg'] = 'light slate gray'

        # Recuperation des donnees
        for doc in self.docList:
            fileToAnalyse = 'DocList\\' + doc

            with open(fileToAnalyse, 'r') as readFile:

                for line in readFile:
                    if line.startswith('STATUTENCOURS'):
                        curStatut = int(line.split(' ')[1])

                readFile.close()

            with open(fileToAnalyse, 'r') as readFile:
                triggerCat = 0
                for line in readFile:

                    if curStatut == 1:
                        if line.startswith('REDACTION'):
                            triggerCat = 1
                        elif line.startswith('RELECTURE'):
                            triggerCat = 0
                        elif triggerCat == 1:
                            if line.startswith(self.persSelec):
                                if line.split(' ')[1] == 'NOK\n':
                                    self.fullData[self.catList[0]].append(doc)

                    elif curStatut == 2:
                        if line.startswith('RELECTURE'):
                            triggerCat = 1
                        elif line.startswith('SIGNATURE'):
                            triggerCat = 0
                        elif triggerCat == 1:
                            if line.startswith(self.persSelec):
                                if line.split(' ')[1] == 'NOK\n':
                                    self.fullData[self.catList[1]].append(doc)

                    elif curStatut == 3:
                        if line.startswith('SIGNATURE'):
                            triggerCat = 1
                        elif line.startswith('DIFFUSION'):
                            triggerCat = 0
                        elif triggerCat == 1:
                            if line.startswith(self.persSelec):
                                if line.split(' ')[1] == 'NOK\n':
                                    self.fullData[self.catList[2]].append(doc)

                    elif curStatut == 4:
                        if line.startswith('DIFFUSION'):
                            triggerCat = 1
                        elif line.startswith('STATUTENCOURS'):
                            triggerCat = 0
                        elif triggerCat == 1:
                            if line.startswith(self.persSelec):
                                if line.split(' ')[1] == 'NOK\n':
                                    self.fullData[self.catList[3]].append(doc)

        # Placement et remplissage des fenetres
        # ACTIONS ---------------------------------------------------------------------------------------------
        # --------- Creation de la fenetre
        actionFrame = LabelFrame(self.persWindow, text='Action', labelanchor='nw', bd=5, bg='alice blue',
                                 borderwidth=2, width=300, height=70, highlightthickness=5,
                                 highlightbackground='alice blue', font='arial 9 italic', foreground='navy')
        actionFrame.pack_propagate(False)
        actionFrame.pack(side=TOP, padx=2, pady=5)

        # --------- Boutton SAUVEGARDER
        actualiseButton = Button(actionFrame, text='SAUVEGARDER ET QUITTER',
                                 command=self.saveAndQuit, state=NORMAL, font='arial 10 bold',
                                 foreground='deep pink', background='black')
        actualiseButton.pack(side=TOP, pady=5, padx=20)

        # INFORMATIONS -------------------------------------------------------------------------------------------
        self.mainFrame = Frame(self.persWindow, bg='alice blue', width=550, height=500, highlightthickness=0, padx=5,
                               pady=5)
        self.mainFrame.pack(side=TOP, padx=5, pady=5)

        self.canvasContainer = Canvas(self.mainFrame, bg='alice blue', width=550, height=400, highlightthickness=0)
        self.defilY = Scrollbar(self.mainFrame, orient='vertical', command=self.canvasContainer.yview)

        self.mainDocPersFrame = LabelFrame(self.canvasContainer, foreground='navy', labelanchor='nw',
                                           text='Documents à traiter',
                                           bg='alice blue', width=510, height=430, font='arial 10 bold',
                                           borderwidth=2, highlightthickness=0, highlightbackground='alice blue',
                                           padx=5, pady=5)
        self.defilY.bind("<Configure>",
                         lambda e: self.canvasContainer.configure(scrollregion=self.canvasContainer.bbox("all")))
        self.canvasContainer.configure(yscrollcommand=self.defilY.set)
        self.canvasContainer.create_window((10, 10), window=self.mainDocPersFrame, anchor='nw')

        self.canvasContainer.pack(side=LEFT)
        self.defilY.pack(side=RIGHT, fill='y')

        # Creation des fenetres pour chaque categorie
        self.frameTitle = []
        self.data = {}
        j=0
        for cat in self.catList:
            if cat == 'REDACTION':
                text = 'a rediger'
            elif cat == 'RELECTURE':
                text = 'a relire'
            elif cat == 'SIGNATURE':
                text = 'a signer'
            elif cat == 'DIFFUSION':
                text = 'a diffuser'

            self.frameTitle.append(LabelFrame(self.mainDocPersFrame, foreground='grey20', labelanchor='nw', width=500,
                                              text=text, bd=5, bg='alice blue', font='arial 10 bold', borderwidth=1,
                                              highlightthickness=0, highlightbackground='alice blue', height=200))

            self.frameTitle[j].pack(side=TOP, padx=5, pady=5)

            i = 0
            self.data[j] = []
            if not self.fullData[cat]:
                self.labelForEmptyList = Label(self.frameTitle[j], text='Aucun document ' + text, bg='alice blue',
                                               font='arial 8 italic', width=77, anchor=NW)
                self.labelForEmptyList.pack(side=TOP, padx=20, pady=0)
            else:
                for doc in self.fullData[cat]:
                    checkValue = IntVar()
                    self.data[j].append(Checkbutton(self.frameTitle[j], text=doc, variable=checkValue, onvalue=1,
                                                    offvalue=0, bg='alice blue', width=63, font='arial 9', anchor=NW))

                    self.data[j][i].var = checkValue
                    self.data[j][i].pack(side=TOP, padx=20, pady=0)

                    i += 1
            j += 1

    def saveAndQuit(self):

        self.mainDic = {}

        j = 0
        k = 0
        trigger0 = 0

        for keys in self.fullData:

            if keys == 'REDACTION':
                state = 1
            elif keys == 'RELECTURE':
                state = 2
            elif keys == 'SIGNATURE':
                state = 3
            elif keys == 'DIFFUSION':
                state = 4

            i = 0
            for doc in self.fullData[keys]:
                done = self.data[j][i].var.get()
                self.mainDic[k] = {'title': doc,
                                   'state': state,
                                   'done': done}
                i += 1
                k += 1
            j += 1

        for i in range(0,len(self.mainDic)):
            if self.mainDic[i]['done'] == 1:

                trigger0 += 1

                if self.mainDic[i]['state'] == 1:
                    trigger1 = 'REDACTION'
                    trigger2 = 'RELECTURE'
                elif self.mainDic[i]['state'] == 2:
                    trigger1 = 'RELECTURE'
                    trigger2 = 'SIGNATURE'
                elif self.mainDic[i]['state'] == 3:
                    trigger1 = 'SIGNATURE'
                    trigger2 = 'DIFFUSION'
                elif self.mainDic[i]['state'] == 4:
                    trigger1 = 'DIFFUSION'
                    trigger2 = 'STATUTENCOURS'

                trigger3 = 0
                lineToReWrite = []
                fileToAnalyse = "DocList" + '\\' + self.mainDic[i]['title']
                with open(fileToAnalyse, 'r') as readFile:
                    for line in readFile:
                        if line.startswith(trigger1):
                            trigger3 = 1
                            lineToReWrite.append(line)
                        elif line.startswith(trigger2):
                            trigger3 = 0
                            lineToReWrite.append(line)
                        else:
                            if trigger3 == 0:
                                lineToReWrite.append(line)
                            else:
                                if line.startswith(self.persSelec):
                                    lineToReWrite.append(self.persSelec + ' OK\n')
                                else:
                                    lineToReWrite.append(line)

                readFile.close()

                fileToWrite = fileToAnalyse
                currentFile = open(fileToWrite, "w+")

                for line in lineToReWrite:
                    currentFile.write(line)

        # FENETRE POP UP AVEC CONSIGN UTILISATEUR
        self.popup = Toplevel()
        self.popup.title(self.fullName + ' - Modifications')
        self.popup.geometry('300x120+450+300')
        self.popup['bg'] = 'alice blue'

        if trigger0 == 0:
            text = 'Aucune Modifications prise en compte'
        else:
            text = 'Modifications bien prises en compte'

        msg = Message(self.popup, text=text, anchor=CENTER, bg='alice blue',
                      width=250,
                      font='arial 9 bold')
        msg.pack(side=TOP, pady=5)
        msg2 = Message(self.popup, anchor=CENTER, bg='alice blue', width=250, font='arial 9',
                       text='La fenetre liée au menu va se fermer \nMerci d actualiser la fenetre principale')
        msg2.pack(side=TOP, pady=0)

        self.windowList = [self.popup, self.persWindow]

        but = Button(self.popup, text='OK', command=self.destroyWindow, state=NORMAL, width=20,
                     font='arial 10 bold', foreground='black', bg='grey60')
        but.pack(side=TOP, pady=5)

    def destroyWindow(self):
        for window in self.windowList:
            window.destroy()