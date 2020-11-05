from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QPlainTextEdit, QSpinBox
from PyQt5.QtCore import Qt
import sys

class Styler(QtWidgets.QMainWindow):
    def __init__(self):
        super(Styler, self).__init__()
        self.setWindowTitle('I can grow my own banans!')
        self.setFixedSize(1024,768)
        self.lefttext = QPlainTextEdit(self)
        self.righttext = QPlainTextEdit(self)
        self.spinbox = QSpinBox(self)
        self.spinbox.setButtonSymbols(2)
        self.spinbox.setAlignment(Qt.AlignCenter)
        self.spinbox.setGeometry(int(self.width() * 0.5) - 30, self.height() - 65, 60, 30)
        self.spinbox.setValue(80)
        self.lefttext.setFixedSize(int(self.width() * 0.5) -20, self.height() - 10)
        self.righttext.setFixedSize(int(self.width() * 0.5) -20, self.height() - 10)
        self.lefttext.move(5,5)
        self.righttext.move(int(self.width() * 0.5) + 15, 5)
        self.lefttext.textChanged.connect(self.style_text)
        self.show()

    def style_text(self):
        s = self.lefttext.toPlainText()
        orgstring = s.replace('  ', ' ')
        orglist = orgstring.split('\n')
        for count in range(len(orglist)):
            orglist[count] = orglist[count].rstrip(',')

        mydict = {'from':[], 'import':[]}

        for eachkey in mydict.keys():
            for eachinput in orglist:
                if eachinput[0:len(eachkey)] == eachkey:
                    mydict[eachkey].append(eachinput)

        templist = []
        for i in mydict['import']:
            if i not in templist:
                templist.append(i)
        templist.sort()
        mydict['import'] = templist

        templist = []
        for eachfrom in mydict['from']:
            eachfrom = eachfrom.replace(',','')
            fromlist = eachfrom.split()
            for count in range(2,len(fromlist)):
                if fromlist[count] not in templist:
                    templist.append(fromlist[count])

        templist.sort()
        tempdict = {}
        dupelist = []
        for eachsingle in templist:
            for eachfrom in mydict['from']:
                eachfrom = eachfrom.replace(',','')
                fromlist = eachfrom.split()
                for count in range(2,len(fromlist)):
                    if fromlist[count] == eachsingle and eachsingle != 'import':
                        if fromlist[count] in dupelist:
                            continue
                        else: 
                            dupelist.append(fromlist[count])
                            thisfrom = f'{fromlist[0]} {fromlist[1]} {fromlist[2]}'
                            if thisfrom not in tempdict:
                                tempdict.update({thisfrom:[eachsingle]})
                            else:
                                tempdict[thisfrom].append(eachsingle)

        final = []
        for base in tempdict:
            longstring = f'{base} '
            longlist = []
            for count, eachimport in enumerate(tempdict[base]):
                if len(eachimport) + len(f'{base} ') > self.spinbox.value():
                    longlist.append(f'{base} {eachimport}')
                elif len(longstring) + len(f'{eachimport}, ') < self.spinbox.value()+1:
                    longstring += f'{eachimport}, '
                else:
                    longlist.append(longstring.strip())
                    longstring = f'{base} {eachimport}, '
                if count+1 == len(tempdict[base]):
                    longlist.append(longstring.strip())
            for i in longlist:
                final.append(i)
        for i in mydict['import']:
            final.append(i)
        final.sort()
        self.righttext.clear()
        for i in final:
            self.righttext.insertPlainText(f'{i.rstrip(",")}\n')

app = QtWidgets.QApplication(sys.argv)
window = Styler()
app.exec_()
