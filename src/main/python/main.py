import os
import sys
import textwrap
import time
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
                             QToolTip, QVBoxLayout, QWidget, qApp)

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
            else:
                self.clientname = None
            if self.level >= 4:
                if self.yearpref in self.parts[3]:
                    self.year = self.parts[3].strip(self.yearpref)
                else:
                    self.year = None
            else:
                self.year = None

    # TODO: Error message on tree view if no folder found         // ETA: 30 Minutes
    # TODO: Extract information from latest workpapers            // ETA: 4 Hours
    # TODO: For future update > Add XPM Links                     // ETA: 10 Hours
    # TODO: Context Menu > Add New  > Workpapers / Folder         // ETA: 30 Minutes
    # TODO: Add double click event to open files in tree view     // ETA: 50 Minutes
    # TODO: Add images for close and minimize button              // ETA: 20 Minutes

    def variables(self):
        self.configpath = configpath
        self.configparam = configparam
        self.configfile = configfile
        self.wpfolder = 'Annual Workpapers'
        self.prevpath = []
        self.listyear = []
        self.clientname = ''
        self.count = 0
        self.counter = 0
        self.oldPos = self.pos()
        self.settingsbox = Settings()
        self.flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)

    def init_widgets(self):
        self.populate()
        self.client_names()
        self.actions()
        self.toggle_year(False)
        self.lineEdit.hide()
        self.yearline.setText(self.year)
        self.treeView.setRootIndex(self.model.index(self.clientdir))
        self.setWindowFlags(self.flags) # Set Flags (Frameless)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.backbutton.setEnabled(False)

    def load_settings(self):
        """Load settings from config file"""

        # Settings File
        if not os.path.exists(self.configpath):
            os.mkdir(self.configpath)
        if not os.path.exists(self.configfile):
            with open(self.configfile, 'w+') as f:
                separator = '=\n'
                f.write(separator.join(self.configparam) + '=')
                f.close

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

    def select_client(self, event):
        """Hide label and show line edit"""
        self.clientlabel.hide()
        self.lineEdit.show()

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
        """Changing folder function, all of them passed here"""
        #Folder instance for prev folder
        self.prevfolder = self.Folder(self.path)
        self.prevpath.append(self.prevfolder.path)
        if self.prevfolder.clientname:
            self.prevclient = s
        # Detect how folder function is initialized
        if opt == 'selected':
            self.clientname = self.lineEdit.text()
            self.path = '\\'.join([self.clientdir,self.clientname,self.year])
        # elif opt == 'back':
        #     pass

        elif opt == 'manual':
            self.path = self.openpath
        # elif opt == 'up':
        # elif opt == 'switch':

        #Folder instance for current folder
        self.currfolder = self.Folder(self.path)
        self.treeView.setRootIndex(self.model.index(self.path)) #Run folder

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
            self.labeltext = textwrap.shorten(self.clientname,
                                                65,placeholder='...')
            self.clientlabel.setText(self.labeltext)
            self.lineEdit.setText(self.clientname)
            self.lineEdit.hide()
            self.clientlabel.show()
            if self.prevclient != self.clientname:
                self.years(self.clientfolder, clear=True)
                print(self.listyear)
        # Storing paths to a list

        # Toggle year widget if current index contains year pref
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
        # self.folder(opt='back')
        pass

    def go_up(self):
        self.folder(opt='up')

    def toggle_year(self, boolean):
        self.rightarrow.setEnabled(boolean)
        self.leftarrow.setEnabled(boolean)
        self.yearline.setEnabled(boolean)

    def switchyear(self, event):
        """Switch one year on yearline"""
        print(event)
        currfolder = os.path.basename(self.path)
        self.curryear = currfolder.strip(self.yearpref)
        self.index = self.listyear.index(self.curryear)
        # if event.key():
        #     self.index += 1
        # else:
        #     self.index -= 1
        self.newyear = self.listyear[self.index]
        self.yearline.setText(self.newyear)
        self.folder(opt='switch')

    def actions(self):
        """All actions for buttons"""
        self.closebutton.clicked.connect(self.close)
        self.minimizebutton.clicked.connect(self.showMinimized)
        self.completer.activated.connect(self.client_selected)
        self.settingsbutton.clicked.connect(self.open_settings)
        self.rightarrow.mousePressEvent = self.switchyear
        self.leftarrow.mousePressEvent = self.switchyear
        self.clientlabel.mousePressEvent = self.select_client
        self.backbutton.clicked.connect(self.goback)
        self.settingsbox.buttonBox.accepted.connect(self.save_settings)
        self.treeView.mouseDoubleClickEvent = self.open_file
        self.upper.clicked.connect(self.go_up)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.lineEdit.returnPressed.connect(self.client_selected)

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
        if self.clientlabel.isHidden() and event.key() == 16777216:
            self.hide_client()

        if event.key() == QtCore.Qt.Key_Backspace:  # Go back on previous folder
            self.folder(opt='back')

        print(event.key())

    def mousePressEvent(self, event):
        """Record the position when mouse is pressed"""
        self.oldPos = event.globalPos()
        if self.clientlabel.isHidden():
            self.hide_client()

    def mouseMoveEvent(self, event):
        """Updating positions as we drag"""
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


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
        self.cmodes = ['Popup', 'Unfiltered Popup', 'Inline']

    def actions(self):
        self.browse_button.clicked.connect(self.getClientpath)

    def init_widgets(self):
        self.autocomplete.addItems(self.cmodes)

    def reader(self):
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
