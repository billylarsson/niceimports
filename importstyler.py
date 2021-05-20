from PyQt5               import QtWidgets
from PyQt5.QtCore        import Qt
from PyQt5.QtWidgets     import QLabel, QPlainTextEdit, QPushButton, QSpinBox
from PyQt5.QtWidgets     import QTextEdit
from pygments            import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers     import get_lexer_by_name
import copy
import sys

cutvalue = 80

class StairWarLabel(QtWidgets.QLabel):
    def __init__(self, place, main):
        super().__init__(place)
        self.setStyleSheet('background-color: rgba(50,50,150,175);color: rgba(255, 212, 42, 255)')
        self.main = main
        self.mode = 1
        self.show()

    def change_mode(self):
        if self.mode + 1 in self.modedict:
            self.mode += 1
        else:
            self.mode = 1

    def process_stairs(self):
        lefttext = self.main.lefttext.toPlainText()
        if len(lefttext) == 0:
            return


        self.modedict = {1: "", 2: "", 3: "", 4: "", 5: "", 6: ""}
        tmpdict = {}
        longest = -1
        heads = []
        contents = lefttext.split('\n')

        for i in contents:
            if i.find('=') == -1:
                continue
            while i.find('  ') > -1:
                i = i.replace('  ', ' ')

            i = i.replace('\t', "")

            i = self.main.string_stripper(i)
            minilist = i.split('=')
            if len(minilist) != 2:
                return

            minilist[0] = self.main.string_stripper(minilist[0])
            minilist[1] = self.main.string_stripper(minilist[1])

            if len(minilist[0]) > longest:
                longest = len(minilist[0])

            heads.append(minilist[0])
            tmpdict.update({minilist[0]: minilist[1]})

        heads.sort(key=str.casefold)
        lenheads = copy.copy(heads)
        reverse_lenheads = copy.copy(heads)
        lenheads.sort(key=len)
        reverse_lenheads.sort(key=len, reverse=True)
        for count, i in enumerate(heads):
            self.modedict[1] += f'{i} = {tmpdict[i]}\n'
            self.modedict[2] += f'{i}{" " * (longest - len(i))} = {tmpdict[i]}\n'

            ii = lenheads[count]
            self.modedict[3] += f'{ii}{" " * (longest - len(ii))} = {tmpdict[ii]}\n'
            self.modedict[4] += f'{ii} = {tmpdict[ii]}\n'

            iii = reverse_lenheads[count]
            self.modedict[5] += f'{iii}{" " * (longest - len(iii))} = {tmpdict[iii]}\n'
            self.modedict[6] += f'{iii} = {tmpdict[iii]}\n'

        self.change_mode()
        self.main.righttext.setText(self.main.format_text(self.modedict[self.mode]))
        if self.mode == 1:
            self.main.setWindowTitle("Alphabetically sorted")
        elif self.mode == 2:
            self.main.setWindowTitle("Alphabetically sorted extra space")
        elif self.mode == 3:
            self.main.setWindowTitle("String lengths")
        elif self.mode == 4:
            self.main.setWindowTitle("String lengths extra space")
        elif self.mode == 5:
            self.main.setWindowTitle("String lengths reversed")
        elif self.mode == 6:
            self.main.setWindowTitle("String lengths extra space reversed")

    def mousePressEvent(self, ev):
        self.main.u_turn = True
        if ev.button() == 1:
            self.process_stairs()

        self.main.u_turn = False

class SortLabel(StairWarLabel):
    def sort_only(self):
        lefttext = self.main.lefttext.toPlainText()
        contents = lefttext.split('\n')

        self.modedict = {1: "", 2: "", 3: "", 4: ""}

        finallist = []
        for i in contents:

            while i.find('  ') > -1:
                i = i.replace('  ', ' ')

            i = i.replace('\t', "")

            i = self.main.string_stripper(i)
            finallist.append(i)

        self.change_mode()

        if self.mode == 1:
            finallist.sort()
            self.main.setWindowTitle("Alphabetically sorted")
        elif self.mode == 2:
            finallist.sort(reverse=True)
            self.main.setWindowTitle("Alphabetically reversed")
        elif self.mode == 3:
            finallist.sort(key=len)
            self.main.setWindowTitle("Alphabetically string lengts")
        elif self.mode == 4:
            finallist.sort(key=len, reverse=True)
            self.main.setWindowTitle("Alphabetically string lengts reversed")

        self.modedict[self.mode] = '\n'.join(finallist)
        self.main.righttext.setText(self.main.format_text(self.modedict[self.mode]))

    def mousePressEvent(self, ev):
        self.main.u_turn = True
        if ev.button() == 1:
            self.sort_only()
        self.main.u_turn = False

class CompareLabel(QtWidgets.QLabel):
    def __init__(self, place, main):
        super().__init__(place)
        self.setStyleSheet('background-color: rgba(50,150,50,175);color: rgba(255, 212, 42, 255)')
        self.main = main
        self.show()

    def mousePressEvent(self, ev):
        if ev.button() == 1:
            if self.main.lines == True:
                self.main.lines = False
                self.main.u_turn = True
                self.main.lefttext.setText(self.main.format_text(self.main.backup_left))
                self.main.righttext.setText(self.main.format_text(self.main.backup_right))
                self.main.u_turn = False
            else:
                self.main.lines = True
                self.main.compare_sides()

class Styler(QtWidgets.QMainWindow):
    def __init__(self):
        super(Styler, self).__init__()
        self.setWindowTitle('I can grow my own banans!')
        self.setFixedSize(1920,1080)
        self.setStyleSheet('background-color: gray;color: white')
        self.move(800,300)
        self.lefttext = QTextEdit(self)
        self.righttext = QTextEdit(self)

        self.lefttext_scrollbar = self.lefttext.verticalScrollBar()
        self.righttext_scrollbar = self.righttext.verticalScrollBar()
        self.lefttext_scrollbar.hide()
        self.righttext_scrollbar.hide()

        self.spinbox = QSpinBox(self)

        self.lefttext.setStyleSheet('background-color: rgba(36, 30, 37, 255);color: rgba(255, 212, 42, 255)')
        self.righttext.setStyleSheet('background-color: rgba(26, 20, 27, 255);color: rgba(255, 212, 42, 255)')
        self.spinbox.setStyleSheet('background-color: brown;color: rgba(255, 212, 42, 255)')

        self.spinbox.setButtonSymbols(2)
        self.spinbox.setAlignment(Qt.AlignCenter)
        self.spinbox.setGeometry(int(self.width() * 0.5) - 30, self.height() - 65, 60, 30)
        self.spinbox.setValue(cutvalue)

        self.comparelabel = CompareLabel(self, self)
        self.comparelabel.setGeometry(int(self.width() * 0.5) - 30, self.spinbox.geometry().top() - 40, 60, 30)

        self.stairwaylabel = StairWarLabel(self, self)
        self.stairwaylabel.setGeometry(int(self.width() * 0.5) - 30, self.comparelabel.geometry().top() - 40, 60, 30)

        self.sortonlylabel = SortLabel(self, self)
        self.sortonlylabel.setStyleSheet('background-color: rgba(150,50,50,175);color: rgba(255, 212, 42, 255)')
        self.sortonlylabel.setGeometry(int(self.width() * 0.5) - 30, self.stairwaylabel.geometry().top() - 40, 60, 30)

        self.lefttext.setFixedSize(int(self.width() * 0.5) -20, self.height() - 10)
        self.righttext.setFixedSize(int(self.width() * 0.5) -20, self.height() - 10)
        self.lefttext.move(5,5)
        self.righttext.move(int(self.width() * 0.5) + 15, 5)
        self.lefttext.textChanged.connect(self.style_text)
        self.lines = False

        self.show()

    def style_text(self):
        if 'u_turn' in dir(self) and self.u_turn == True:
            return

        self.lines = False
        self.final = ""
        self.sort_dict = {}

        text = self.lefttext.toPlainText()
        new_text = self.format_text(text)
        self.u_turn = True
        self.lefttext.setText(new_text)
        self.u_turn = False

        text_list = text.split('\n')

        caught = self.add_possible_strings(text_list)
        caught = self.sort_imports_accordingly(caught)
        self.sort_froms_accordingly(caught)
        self.put_together()
        formated_text = self.format_text(self.final)
        self.righttext.setText(formated_text)

    def compare_sides(self):
        def count_errors(list_one, list_two):
            list_one = list_one.split()
            list_two = list_two.split()
            rows_of_errors = []
            for count in range(len(list_one)):
                if count+1 > len(list_two):
                    break
                if list_one[count] != list_two[count]:
                    rows_of_errors.append(count-3)
            return rows_of_errors

        def do_this(text, rows_of_errors):
            splitlist = text.split('\n')
            for c in range(len(splitlist) - 1, -1, -1):
                if c not in rows_of_errors:
                    splitlist[c] = '\t' + splitlist[c]
                else:
                    splitlist[c] = '->\t' + splitlist[c]

            splitlist.insert(0, ' ')
            splitlist.insert(0, ' ')
            splitlist.insert(0, f'I find {len(rows_of_errors)} unaligned rows!')
            rv = '\n'.join(splitlist)
            return rv

        self.backup_left = self.lefttext.toPlainText()
        self.backup_right = self.righttext.toPlainText()

        left = copy.copy(self.backup_left)
        right = copy.copy(self.backup_right)

        rows_of_errors = count_errors(left, right)

        left = do_this(left, rows_of_errors)
        right = do_this(right, rows_of_errors)

        self.u_turn = True
        self.lefttext.setText(self.format_text(left))
        self.righttext.setText(self.format_text(right))
        self.u_turn = False

    def format_text(self, orgstring):
        lexer = get_lexer_by_name("python", stripall=True)
        formatter = HtmlFormatter(cssclass="source", full=True, linenos=self.lines)
        new_text = highlight(orgstring, lexer, formatter)

        return new_text

    def add_possible_strings(self, text_list):
        caught = []
        self.top = []
        self.bottom = []

        primary_work_done = False
        for count, i in enumerate(text_list):
            i = i.strip()
            if len(i) > len('import ') and i[0:len('import ')] == 'import ' or i[0:len('from ')] == 'from ':
                caught.append(i)
            else:
                if len(i) > 2 and i[0:3] == '"""':
                    pass
                elif len(i) > 2 and i[0:3] == "'''":
                    pass
                elif len(i) > 0 and i[0] == '#':
                    pass
                else:
                    primary_work_done = True

                if primary_work_done == True:
                    self.bottom.append(text_list[count].rstrip('\n').rstrip())
                else:
                    self.top.append(text_list[count].rstrip('\n').rstrip())

        return caught

    def put_together(self):
        self.final += '\n'.join(self.top)

        if 'from' in self.sort_dict:
            x = self.sort_dict['from']
            froms = {k: v for k, v in sorted(x.items(), key=lambda item: item[0])}

            max = -1
            for i in froms:
                if len(i) >= max:
                    max = len(i)+1

            for eachfrom in froms:
                string = 'from ' + eachfrom + (" " * (max - len(eachfrom)))
                for count, imports in enumerate(froms[eachfrom]):
                    if count == 0:
                        string += f'import {imports}, '
                    else:
                        if len(string) + len(imports) > self.spinbox.value():
                            self.final += string.rstrip(', ') + '\n'
                            string = 'from ' + eachfrom + (" " * (max - len(eachfrom))) + 'import '

                        string += imports + ', '

                    if count+1 == len(froms[eachfrom]):
                        self.final += string.rstrip(', ') + '\n'


        if 'import' in self.sort_dict:
            for i in self.sort_dict['import']:
                self.final += f'import {i}\n'

        self.final += '\n'.join(self.bottom)

    def string_stripper(self, string):
        string = string.strip()
        string = string.rstrip('\n')
        return string

    def sort_froms_accordingly(self, list_with_strings):
        for c in range(len(list_with_strings)-1,-1,-1):
            if list_with_strings[c][0:len('from ')] == 'from ':
                if 'from' not in self.sort_dict:
                    self.sort_dict.update({'from': { }})

                string = list_with_strings[c][len('from '):]
                wrong_froms = string.split()
                froms = []

                for i in wrong_froms:
                    tmp = i.split(',')
                    for ii in tmp:
                        froms.append(ii)

                current = froms[0]
                current = self.string_stripper(current)

                froms.pop(0) # pops 'current'
                froms.pop(0) # pops 'import'

                if current not in self.sort_dict['from']:
                    self.sort_dict['from'].update({current: []})

                for eachstring in froms:
                    eachstring = self.string_stripper(eachstring)
                    if eachstring not in self.sort_dict['from'][current] and eachstring != "":
                        self.sort_dict['from'][current].append(eachstring)

                self.sort_dict['from'][current].sort()
                list_with_strings.pop(c)

        return list_with_strings


    def sort_imports_accordingly(self, list_with_strings):
        for c in range(len(list_with_strings)-1,-1,-1):
            if list_with_strings[c][0:len('import ')] == 'import ':
                if 'import' not in self.sort_dict:
                    self.sort_dict.update({'import': []})

                string = list_with_strings[c][len('import '):]
                imports = string.split(',')

                for eachstring in imports:
                    eachstring = self.string_stripper(eachstring)
                    if eachstring not in self.sort_dict['import'] and eachstring != "":
                        self.sort_dict['import'].append(eachstring)

                list_with_strings.pop(c)

        if 'import' in self.sort_dict:
            self.sort_dict['import'].sort()

        return list_with_strings


app = QtWidgets.QApplication(sys.argv)
window = Styler()
app.exec_()
