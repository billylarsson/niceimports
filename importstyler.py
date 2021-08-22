#!/usr/bin/env python3

from PyQt5               import QtGui, QtWidgets
from PyQt5.QtCore        import QPoint, Qt
from pygments            import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers     import get_lexer_by_name
import sys
import copy

class tech:
    def __init__(self):
        self.techdict = {}
    def pos(widget=None,
            new=None,
            margin=0,
            inside=None,
            coat=None,
            size=None, add=0,
            width=None, height=None,
            left=None, right=None,
            below=None, above=None,
            leftof=None, rightof=None,
            move=None,
            x_margin=0, y_margin=0,
            background=None,
            ):
        """
        :param widget: changing widget
        :param inside: one widget lives inside another   -> setGeometry()
        :param coat: both widgets lives inside the same -> setGeometry()
        :param size: tuple (w,h) or another widget       -> resize()
        :param add: int usable with resize for exapnd or contract
        :param left/right: another widget
        :param width/height: int or another widget
        :param below/above: another widget
        :param left/right: another widget
        :param move: tuple (-24, +16) in relation to current.geometry()
        :param background: string/object sets background color (or entire objects stylesheet)
        :param x_margin/y_margin: int space between (above,below,left,right only)
        """

        def geochange(x, y, w, h):
            widget.setGeometry(int(x), int(y), int(w), int(h))

        def geosize(w, h):
            widget.resize(int(w), int(h))

        if new != None:
            widget = QtWidgets.QLabel(new)
        # -------------------[INSIDE/COAT]
        if inside != None:  # one widget lives inside the other
            x = margin
            y = margin
            w = inside.width() - margin * 2
            h = inside.height() - margin * 2
            geochange(x, y, w, h)
        elif coat != None:  # reside in same widget
            x = coat.geometry().left() + margin
            y = coat.geometry().top() + margin
            w = coat.width() - margin * 2
            h = coat.height() - margin * 2
            geochange(x, y, w, h)
        # -------------------[WIDTH]
        if type(width) in {int, float}:
            geosize(width + add, widget.height())
        elif width != None:
            geosize(width.width() + add, widget.height())
        # -------------------[HEIGHT]
        if type(height) in {int, float}:
            geosize(widget.width(), height + add)
        elif height != None:
            geosize(widget.width(), height.height() + add)
        # -------------------[SIZE]
        if type(size) == tuple or type(size) == list:
            geosize(size[0] + add, size[1] + add)
        elif size != None:
            geosize(size.width() + add, size.height() + add)
        # -------------------[LEFT/RIGHT]
        if left != None:
            if type(left) in {int, float}:
                x = left + x_margin
            else:
                x = left.geometry().left() + x_margin
            if not right:
                geochange(x, widget.geometry().top(), widget.width(), widget.height())
            else:
                if type(right) in {int, float}:
                    w = right - x_margin
                else:
                    w = right.geometry().right() - x_margin * 2
                geochange(x, widget.geometry().top(), w - x, widget.height())
        elif right != None:
            if type(right) in {int, float}:
                x = right - widget.width() - x_margin
            else:
                x = right.geometry().right() - widget.width() - x_margin
            geochange(x, widget.geometry().top(), widget.width(), widget.height())
        # -------------------[ABOVE/BELOW]
        if above != None:
            if type(above) in {int, float}:
                y = above + y_margin
            else:
                y = above.geometry().top() - widget.height() - y_margin - 1  # else same pixel
            geochange(widget.geometry().left(), y, widget.width(), widget.height())
        elif below != None:
            if type(below) in {int, float}:
                y = below + y_margin
            else:
                y = below.geometry().bottom() + y_margin + 1  # else same pixel
            geochange(widget.geometry().left(), y, widget.width(), widget.height())
        # -------------------[LEFTOF/RIGHTOF]
        if leftof != None:
            x = leftof.geometry().left() - widget.width() - x_margin
            y = leftof.geometry().top()
            geochange(x, y, widget.width(), widget.height())
        elif rightof != None:
            x = rightof.geometry().right() + x_margin + 1
            y = rightof.geometry().top()
            geochange(x, y, widget.width(), widget.height())
        # -------------------[MOVE]
        if move and len(move) == 2:
            x = widget.geometry().left() + move[0]
            y = widget.geometry().top() + move[1]
            w = widget.width()
            h = widget.height()
            geochange(x, y, w, h)
        # -------------------[MOVE]
        if background != None:
            if type(background) == str:
                widget.setStyleSheet('background-color:' + background)
            else:
                widget.setStyleSheet(background.styleSheet())

        if new != None:
            widget.show()
            return widget

    def style(widget, set=True, save=False, name=None, background=None, color=None, font=None, delete=False):
        """
        if save is True, the set part wont happen
        if name is given, will request, save or set 'stylesheet_name'
        if name isnt given looks into widget.type and requests 'stylesheet_type'
        if any background,color,font thoes are set but not saved: background='green' font='8pt'
        :param widget: object
        :param set: bool
        :param save: bool
        :param name: string
        :return: bool or string.styleSheet()
        """
        def make_stylesheet():
            if widget.styleSheet():
                stylelist = widget.styleSheet().split(';')
            else:
                stylelist = []

            dlist = [
                dict(find='background-color:', replace=background),
                dict(find='color:', replace=color),
                dict(find='font:', replace=font),
            ]

            new = []
            for d in dlist:
                find = d['find']
                replace = d['replace']

                if not stylelist and replace:
                    new.append(find + replace)

                for rangecount in range(2):
                    for count, i in enumerate(stylelist):

                        if rangecount == 0:
                            if i.find(find) > -1 and replace:
                                new.append(find + replace)
                                stylelist.pop(count)
                                break

                        elif rangecount == 1:
                            if i.find(find) > -1:
                                new.append(i)
                                stylelist.pop(count)
                                break

            new = ';'.join(new)
            return new

        if not name:
            if 'type' in dir(widget) and type(widget.type) == str:
                name = widget.type

        if delete and name:
            tech.save_config(name, None, delete, stylesheet=True)

        elif save:
            stylesheet = widget.styleSheet()
            if not stylesheet:
                stylesheet = make_stylesheet()

            if name and stylesheet:
                tech.save_config(name, stylesheet, stylesheet=True)
                return True
            else:
                return False
        elif set:
            if background or color or font:
                new = make_stylesheet()
                widget.setStyleSheet(new)
                return new

            if name:
                stylesheet = tech.config(name, stylesheet=True)
                if stylesheet:
                    widget.setStyleSheet(stylesheet)
                    return stylesheet
                else:
                    return False

class CLICKER(QtWidgets.QLabel):
    def __init__(self, place, main=None):
        super().__init__(place)
        self.parent = place
        if main:
            self.main = main
        else:
            self.main = place

        self.show()

    def toggle_connection(self, forceconnect=False, forcedisconnect=False):
        if forcedisconnect or self.main.connected and not forceconnect:
            self.main.lefttext.disconnect()
            self.main.connection_label.setText('                              D I S C O N N E C T E D')
            tech.style(self.main.connection_label, background='red', color='white')
            self.main.connected = False
        else:
            self.main.lefttext.textChanged.connect(self.main.style_text)
            self.main.connection_label.setText('                                C O N N E C T E D')
            tech.style(self.main.connection_label, background='rgb(0,90,0)', color='white')
            self.main.connected = True

class Alphabetially(CLICKER):
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.main.old_position = ev.globalPos()
        if ev.button() == 1:
            self.toggle_connection(forceconnect=True)
            text = self.main.lefttext.toPlainText()
            text = text.split('\n')
            text.sort()
            text = '\n'.join(text)
            text = self.main.format_text(text)
            self.main.righttext.setText(text)

class AlphabetiallyReversed(CLICKER):
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.main.old_position = ev.globalPos()
        if ev.button() == 1:
            self.toggle_connection(forceconnect=True)
            text = self.main.lefttext.toPlainText()
            text = text.split('\n')
            text.sort()
            text.reverse()
            text = '\n'.join(text)
            text = self.main.format_text(text)
            self.main.righttext.setText(text)

class Disconnect(CLICKER):
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.main.old_position = ev.globalPos()
        self.toggle_connection()

class SameSpace(CLICKER):

    def draw(self):
        self.modedict = {1: "", 2: "", 3: "", 4: "", 5: "", 6: ""}
        text = self.main.lefttext.toPlainText()
        contents = text.split('\n')
        tmpdict = {}
        longest = -1
        heads = []

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

        self.main.righttext.setText(self.main.format_text(self.modedict[self.mode]))

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.main.old_position = ev.globalPos()
        if 'mode' not in dir(self):
            self.mode = 3

        self.toggle_connection(forceconnect=True)
        self.draw()

        if ev.button() == 1:
            self.mode += 1
            if self.mode > len(self.modedict):
                self.mode = 1

        elif ev.button() == 2:
            self.mode -= 1
            if self.mode < 1:
                self.mode = 1


class QUIT(CLICKER):
    def mouseReleaseEvent(self, ev) -> None:
        sys.exit()
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        pass

class ImportStylerV2(QtWidgets.QMainWindow):
    def __init__(self):
        super(ImportStylerV2, self).__init__()
        self.connected = True
        self.resize(1920,1080)
        tech.style(self, background='rgb(130,130,130)', color='white')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.draw_stuff()
        self.show()

    def draw_stuff(self):
        self.connection_label = Disconnect(self)
        self.connection_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        tech.pos(self.connection_label, move=[3,3], size=[100,30])

        alpha = Alphabetially(self)
        alpha.setText(' ALPHABETIC')
        tech.pos(alpha, coat=self.connection_label, below=self.connection_label, y_margin=1)
        tech.style(alpha, background='rgb(0,0,150)', color='rgb(200,200,200)')

        rev = AlphabetiallyReversed(self)
        rev.setText(' REVERSED')
        tech.pos(rev, coat=alpha, below=alpha, y_margin=1)
        tech.style(rev, background='rgb(0,0,120)', color='rgb(200,200,200)')

        samespace = SameSpace(self)
        samespace.setText(' SAME SPACE')
        tech.pos(samespace, coat=alpha, below=rev, y_margin=1)
        tech.style(samespace, background='rgb(0,0,100)', color='rgb(200,200,200)')

        self.lefttext = QtWidgets.QTextEdit(self)
        self.lefttext.textChanged.connect(self.style_text)
        self.lefttext.setStyleSheet('background-color: rgba(36, 30, 37, 255);color: rgba(255, 212, 42, 255)')
        w = (self.width() - alpha.geometry().right() - 6) * 0.5
        tech.pos(self.lefttext, rightof=alpha, x_margin=3, y_margin=3, height=self.height() - 36, width=w)

        self.righttext = QtWidgets.QTextEdit(self)
        self.righttext.setStyleSheet('background-color: rgba(26, 20, 27, 255);color: rgba(255, 212, 42, 255)')
        tech.pos(self.righttext, coat=self.lefttext, left=self.lefttext.geometry().right(), right=self.width()-3)

        quit = QUIT(self)
        quit.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        quit.setText('QUIT')
        tech.pos(quit, coat=alpha, above=self.geometry().bottom() - 3 - 30)
        tech.style(quit, background='darkGray', color='black', font='14pt')

        self.spinbox = QtWidgets.QSpinBox(self)
        self.spinbox.setButtonSymbols(2)
        self.spinbox.setAlignment(Qt.AlignCenter)
        self.spinbox.setValue(80)
        tech.pos(self.spinbox, coat=alpha, above=quit, y_margin=-1)
        tech.style(self.spinbox, background='darkGray', color='black')

        self.connection_label.toggle_connection(forceconnect=True)
        tech.pos(self.connection_label, width=self.width() - 6)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.button() == 1:
            self.old_position = ev.globalPos()

    def mouseMoveEvent(self, event):
        if event.button() == 2 or 'old_position' not in dir(self):
            return

        delta = QPoint(event.globalPos() - self.old_position)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_position = event.globalPos()

    def format_text(self, orgstring):
        if not orgstring:
            return ""

        lexer = get_lexer_by_name("python", stripall=True)
        formatter = HtmlFormatter(cssclass="source", full=True, linenos=self.lines, nobackground=True)
        new_text = highlight(orgstring, lexer, formatter)

        return new_text

    def style_text(self):
        if not self.lefttext.toPlainText():
            return

        if not self.connected:
            return

        self.connection_label.toggle_connection(forcedisconnect=True)

        self.lines = False
        self.final = ""
        self.sort_dict = {}

        text = self.lefttext.toPlainText()
        new_text = self.format_text(text)
        self.lefttext.setText(new_text)

        text_list = text.split('\n')

        caught = self.add_possible_strings(text_list)
        caught = self.sort_imports_accordingly(caught)
        self.sort_froms_accordingly(caught)
        self.put_together()
        formated_text = self.format_text(self.final)
        self.righttext.setText(formated_text)

        self.connection_label.toggle_connection(forceconnect=True)

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
                        if len(froms) > 1 and froms[-1] == 'as':
                            froms[-2] = froms[-2] + ' ' + froms[-1] + ' ' + ii
                            froms.pop(-1)
                        else:
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImportStylerV2()
    app.exec_()
