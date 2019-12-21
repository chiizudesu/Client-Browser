import os
import sys
import textwrap
import time
import configparser

from datetime import datetime

import qdarkstyle
import xlwings as xw
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QBasicTimer, QCoreApplication, QPoint
from PyQt5.QtGui import QFont, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QCompleter,
                             QDesktopWidget, QDialog, QFileDialog, QFrame,
                             QGridLayout, QLabel, QLineEdit, QMainWindow,
                             QMenu, QMenuBar, QMessageBox, QProgressBar,
                             QPushButton, QStatusBar, QTextEdit, QToolBar,
                             QToolTip, QVBoxLayout, QWidget, qApp,
                             QDesktopWidget)

from ui import main, settings

configpath = f'{os.environ["USERPROFILE"]}\\Client Browser'
configfile = f'{configpath}\\config.txt'
configparam = ['clientdir', 'autocomplete', 'yearprefix']


class Window(main.Ui_MainWindow, QMainWindow, ApplicationContext):
    def __init__(self):
        """Window Object"""
        super(Window, self).__init__()

        self.setupUi(self) # Inherit from UI file
        self.variables() #Default variables
        self.load_settings() # Load settings
        self.init_widgets() # Initialize widgets
        self.show() #Initiate the window

    class Folder(object):
        """folder object to store folder properties"""
        def __init__(self, folder):
            """Object for getting folder properties"""
            self.yearpref = exit_code.yearpref
            self.path = folder
            self.parts = self.path.split('\\')
            self.level = len(self.parts)
            if self.level >= 2:
                self.parent = os.path.dirname(self.path)
            else:
                self.parent = None
            if self.level >= 3:
                self.clientname = self.parts[2]
                self.clientfolder = '\\'.join(self.parts[0:3])
            else:
                self.clientname = None
            if self.level >= 4:
                if self.yearpref in self.parts[3]:
                    self.year = self.parts[3].lstrip(self.yearpref)
                else:
                    self.year = None
            else:
                self.year = None

    # TODO: Error message on tree view if no folder found         // ETA: 30 Minutes
    # TODO: Extract information from latest workpapers            // ETA: 4 Hours
    # TODO: For future update > Add XPM Links                     // ETA: 10 Hours
    # TODO: Context Menu > Add New  > Workpapers / Folder         // ETA: 30 Minutes
    # TODO: Add double click event to open files in tree view     // ETA: 50 Minutes
    # TODO: Back/Button implement

    def variables(self):
        self.configpath = configpath
        self.configparam = configparam
        self.configfile = configfile
        self.wpfolder = 'Annual Workpapers'
        self.prevpath = []
        self.prevclient = ''
        self.listyear = []
        self.clientname = ''
        self.count = 0
        self.counter = 0
        self.oldPos = self.pos()
        self.settingsbox = Settings()
        self.flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.dimensions = QApplication.desktop().screenGeometry()
        self.screenwidth = self.dimensions.width()
        self.screenheight = self.dimensions.height()
        self.pic = QPixmap(":/img/ui/images/icon.png")
        self.busycursor = QtGui.QCursor(QtCore.Qt.BusyCursor)
        self.arrowcursor = QtGui.QCursor(QtCore.Qt.ArrowCursor)
        self.statusBar = QStatusBar()

    def init_widgets(self):
        self.populate()
        self.client_names()
        self.actions()
        self.toggle_year(False)
        self.lineEdit.hide()
        self.yearline.setText('-')
        self.treeView.setRootIndex(self.model.index(self.clientdir))
        self.setWindowFlags(self.flags) # Set Flags (Frameless)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.backbutton.setEnabled(False)
        self.label_4.setPixmap(self.pic)
        self.setStatusBar(self.statusBar)
        self.infolabels.hide()
        self.cornerwidget = QPushButton()
        self.cornerwidget.setStyleSheet('background-color: rgb(28, 41, 54)')
        self.cornerwidget.setText('+')
        self.cornerwidget.setMinimumSize(20,20)
        self.cornerwidget.setMaximumSize(20,20)
        self.browsertab.setCornerWidget(self.cornerwidget, corner=QtCore.Qt.TopLeftCorner)

    def load_settings(self):
        """Load settings from config file"""
        # Read config file
        configuration = open(self.configfile, 'r')
        self.settings = {}
        for lines in configuration.readlines():
            line = lines.strip('\n').split('=')
            self.settings[line[0]] = line[1]

        # Declaring variables from config file
        if self.settings['clientdir']:
            self.clientdir = self.settings['clientdir']
        else:
            self.clientdir = f'{os.environ["USERPROFILE"]}'

        self.path = self.clientdir
        self.completer_pref = int(self.settings['autocomplete'])
        self.yearpref = self.settings['yearprefix']
        self.year = str(datetime.now().year)
        self.diryear = f'{self.yearpref}{self.year}'

        #DONT READ TWICE

    def select_client(self, event):
        """Hide label and show line edit - activated by label click"""
        self.clientlabel.hide()
        self.lineEdit.show()
        self.lineEdit.setFocus()

    def hide_client(self):
        self.lineEdit.setText('')
        self.lineEdit.hide()
        self.clientlabel.show()

    def client_selected(self):
        """Show label, hide line edit and update label"""
        self.lineEdit.hide()
        self.clientlabel.show()
        self.clientname = self.lineEdit.text()
        self.folder(opt='selected')

    def folder(self, opt=None):
        """Folder navigation function"""
        #Folder instance for prev folder
        self.treeView.viewport().setProperty("cursor", self.busycursor)
        self.prevfolder = self.Folder(self.path)
        self.prevpath.append(self.prevfolder.path)

        if self.prevfolder.clientname:
            self.prevclient = self.prevfolder.clientname

        # Detect how folder function is initialized
        if opt == 'selected':
            self.clientname = self.lineEdit.text()
            self.path = '\\'.join([self.clientdir, self.clientname,
                                   self.diryear])
        elif opt == 'back':
            print(self.prevpath)
        elif opt == 'manual':
            self.path = self.openpath
        elif opt == 'up':
            self.path = self.prevfolder.parent
        elif opt == 'switch':
            self.path = self.prevfolder.path.replace(self.oldyear,
                                                     self.newyear)
        elif opt == 'addressed':
            self.path = self.addressbar.text()

        #Folder instance for current folder
        self.currfolder = self.Folder(self.path)

        #Run Folder
        self.model.setRootPath(self.path)
        self.treeView.setRootIndex(self.model.index(self.path))
        self.treeView.viewport().setProperty("cursor", self.arrowcursor)

    def addressed(self):
        self.addressbar.clearFocus()
        self.folder(opt='addressed')

    def update_folder(self, *event):
        #Detect year and declare year variables
        if self.currfolder.year:
            self.yearline.setText(self.currfolder.year)
            self.toggle_year(True)
        else:
            self.yearline.setText('-')
            self.toggle_year(False)
        #Detect if current index is inside client
        if self.path == self.clientdir:
            self.clientlabel.setText('Select a client...')
            self.hide_client()
        elif self.currfolder.clientname:  # Detect if on second level
            self.clientname = self.currfolder.clientname
            self.labeltext = textwrap.shorten(self.clientname,65,
                                              placeholder='...')
            self.clientlabel.setText(self.labeltext)
            self.lineEdit.setText(self.clientname)
            self.lineEdit.hide()
            self.clientlabel.show()
            if self.prevclient != self.clientname:
                self.years(self.currfolder.clientfolder, clear=True)
        self.windowspath = self.path.replace('/', '\\')
        self.addressbar.setText(self.windowspath)
        self.backbutton.setEnabled(True)

    def years(self, yearfolder, clear=None):
        """Create a list of years from folder structure"""
        if clear:
            self.listyear = []
            self.index = 0

        folders = os.listdir(yearfolder)
        for folder in folders:
            if self.yearpref in folder:
                year = folder.lstrip(self.yearpref)
                self.listyear.append(year)

    def goback(self):
        self.folder(opt='back')

    def go_up(self):
        self.folder(opt='up')

    def toggle_year(self, boolean):
        self.rightarrow.setEnabled(boolean)
        self.leftarrow.setEnabled(boolean)
        self.yearline.setEnabled(boolean)

    def prevyear(self, *event):
        """Switch prev year on yearline"""
        self.index = self.listyear.index(self.currfolder.year)
        self.oldyear = self.listyear[self.index]
        if not self.index:
            self.index = len(self.listyear) - 1
        else:
            self.index -= 1
        self.newyear = self.listyear[self.index]
        self.yearline.setText(self.newyear)
        self.folder(opt='switch')

    def nextyear(self, *event):
        """Switch next year on yearline"""
        self.index = self.listyear.index(self.currfolder.year)
        self.oldyear = self.listyear[self.index]
        if self.index == len(self.listyear) - 1:
            self.index = 0
        else:
            self.index += 1
        self.newyear = self.listyear[self.index]
        self.yearline.setText(self.newyear)
        self.folder(opt='switch')

    def actions(self):
        """All actions for buttons"""
        self.closebutton.clicked.connect(self.close)
        self.minimizebutton.clicked.connect(self.showMinimized)
        self.completer.activated.connect(self.client_selected)
        self.settingsbutton.clicked.connect(self.open_settings)
        self.rightarrow.mousePressEvent = self.nextyear
        self.leftarrow.mousePressEvent = self.prevyear
        self.leftarrow.mouseMoveEvent = self.empty
        self.rightarrow.mouseMoveEvent = self.empty
        self.clientlabel.mousePressEvent = self.select_client
        self.backbutton.clicked.connect(self.goback)
        self.settingsbox.buttonBox.accepted.connect(self.save_settings)
        self.treeView.mouseDoubleClickEvent = self.open_file
        self.upper.clicked.connect(self.go_up)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.lineEdit.returnPressed.connect(self.client_selected)
        self.resizebutton.clicked.connect(self.resize_window)
        self.titlebar.mouseDoubleClickEvent = self.resize_window
        self.model.rootPathChanged.connect(self.update_folder)
        self.hide_unhide_info.clicked.connect(self.hide_unhide_)
        self.titlebar.mouseMoveEvent = self.drag
        self.addressbar.returnPressed.connect(self.addressed)
        self.titlebar.mousePressEvent = self.title_pressed
        self.File.clicked.connect(self.addtab)

    def addtab(self):
        label = QLabel('Test')
        self.browsertab.addTab(label,'Test')

    def hide_unhide_(self):
        if self.infoarea.isHidden():
            self.infoarea.show()
            self.infolabels.hide()
            self.hide_unhide_info.setText('⯇')
        else:
            self.infoarea.hide()
            self.infolabels.show()
            self.hide_unhide_info.setText('⯈')

    def resized(self):
        if not self.isMaximized():
            self.resizebutton.setText('')
        else:
            self.resizebutton.setText('')

    def resize_window(self, *event):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        self.resized()

    def save_settings(self):
        self.settingsbox.writer()
        self.load_settings()
        self.setEnabled(True)
        self.client_names()
        self.actions()

    def open_settings(self):
        """Open settings dialog box"""
        self.settingsbox.show()
        self.settingsbox.exec_()

    def populate(self):
        """Load file browser model on tree view"""
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        # print(QtCore.QDir.rootPath())
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 350)
        self.treeView.setSortingEnabled(1)

    def client_names(self):
        """Auto complete list of entries"""
        self.clients = os.listdir(self.clientdir)
        self.completer = QCompleter(self.clients)
        self.completer.setCaseSensitivity(0)
        self.completer.setMaxVisibleItems(10)
        self.completer.setCompletionMode(self.completer_pref)
        self.lineEdit.setCompleter(self.completer)

    def context_menu(self):
        """Right Click Menu: [OPEN]"""
        menu = QtWidgets.QMenu()

        # Actions
        open = menu.addAction('Open')
        open.triggered.connect(self.open_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self, *event):
        """Open Function"""
        index = self.treeView.currentIndex()
        self.openpath = self.model.filePath(index)
        self.openpath = self.openpath.replace('/', '\\')
        if os.path.isdir(self.openpath):
            self.folder(opt='manual')
        else:
            os.startfile(self.file_path)

    """ Event Handling """

    def keyPressEvent(self, event):
        """Key press events"""
        #if Esc is pressed while on line edit
        if self.lineEdit.hasFocus() and event.key() == 16777216:
            self.hide_client()
        elif self.addressbar.hasFocus() and event.key() == 16777216:
            self.addressbar.clearFocus()

        if event.key() == QtCore.Qt.Key_Backspace:  # Go back on previous folder
            self.folder(opt='back')


    def mousePressEvent(self, event):
        """Record the position when mouse is pressed"""
        if self.clientlabel.isHidden():
            self.hide_client()
        if self.addressbar.hasFocus():
            self.addressbar.clearFocus()

    def empty(self, event):
        pass

    def title_pressed(self, event):
        self.oldPos = event.globalPos()

    def drag(self, event):
        """Updating positions as we drag"""
        delta = QPoint(event.globalPos() - self.oldPos)
        if not self.isMaximized():
            self.move(self.x() + delta.x(), self.y() + delta.y())
        elif delta.y():
            self.showNormal()
            self.move(self.oldPos)
        self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        xresize = [0,1919,1918,1920,1917,3839,3840]
        if event.globalPos().x() in xresize:
            self.showMaximized()
        elif not event.globalPos().y():
            self.showMaximized()
        self.resized()


class Settings(settings.Ui_Dialog, QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.setupUi(self)

        self.variables()
        self.init_widgets()
        self.actions()
        self.reader()  # Read config file

    def variables(self):
        self.configpath = configpath
        self.configfile = configfile
        self.configparam = configparam
        self.cmodes = ['Popup', 'Unfiltered Popup', 'Inline']

    def actions(self):
        self.browse_button.clicked.connect(self.getClientpath)

    def init_widgets(self):
        self.autocomplete.addItems(self.cmodes)

    def reader(self):
        # Config File
        if not os.path.exists(self.configpath):
            os.mkdir(self.configpath)
        if not os.path.exists(self.configfile):
            with open(self.configfile, 'w+') as f:
                separator = '=\n'
                f.write(separator.join(self.configparam) + '=')
                f.close

        self.settings = {}
        configuration = open(self.configfile, 'r')
        for lines in configuration.readlines():
            line = lines.strip('\n').split('=')
            self.settings[line[0]] = line[1]
        if self.settings['clientdir']:
            self.clientdir = self.settings['clientdir']
        else:
            self.clientdir = f'{os.environ["USERPROFILE"]}'

        self.clientpath.setText(self.clientdir)
        if self.settings['autocomplete'] == '':
            self.autocomplete.setCurrentIndex(0)
        else:
            index = int(self.settings['autocomplete'])
            self.autocomplete.setCurrentIndex(index)
        self.yearprefix.setText(self.settings['yearprefix'])

    def writer(self):
        self.config = {'clientdir': '', 'autocomplete': '', 'yearprefix': ''}
        self.config['clientdir'] = self.clientpath.text()
        self.config['yearprefix'] = self.yearprefix.text()
        item_index = int(self.autocomplete.currentIndex())
        self.config['autocomplete'] = item_index
        textdump = ''

        for keys in self.config:
            textdump += f'{keys}={self.config[keys]}\n'

        with open(self.configfile, 'w+') as f:
            f.write(textdump)
            f.close

    def getClientpath(self):
        filedialog = QFileDialog()
        filedialog.setFileMode(QFileDialog.DirectoryOnly)
        filename = filedialog.getExistingDirectory(self, 'Select Directory')
        filename = filename.replace('/', '\\')
        self.clientpath.setText(filename)


if __name__ == '__main__':
    my_app = ApplicationContext()
    my_app.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())  # Dark Theme
    exit_code = Window()
    my_app.app.exec_()

# if __name__ == '__main__':
#     my_app = QApplication(sys.argv)
#     my_app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())  # Dark Theme
#     exit_code = Window()
#     my_app.exec_()
