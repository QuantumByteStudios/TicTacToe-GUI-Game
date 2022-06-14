# importing required libraries
import ctypes
from pydoc import importfile
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys
import applicationUI

# Global Variables
appName = "TicTacToe"
guiFileName = "main"
path = os.path.abspath(f"Py-HTML/src/{guiFileName}.html")
path = path.replace('\\', '/')
fileName = path
filePathForEngine = "file:///"+path
print(f"Located GUI File at: {filePathForEngine}")
# print(applicationUI.mainUI)


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
# print(w)


class MainWindow(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):

        f = open(fileName, 'w')
        # Create GUI File
        f.write(applicationUI.mainUI)
        f.close()

        super(MainWindow, self).__init__(*args, **kwargs)

        self.setGeometry(int(w/5), 200, 900, 600)

        # creating a QWebEngineView
        self.thisApplication = QWebEngineView()

        # Set Initial Path of Main Page
        self.thisApplication.setUrl(QUrl(filePathForEngine))

        # adding action when url get changed
        self.thisApplication.urlChanged.connect(self.updateUrlBar)

        # set as central widget or main window
        self.setCentralWidget(self.thisApplication)

        # creating QToolBar for navigation
        navtb = QToolBar("Navigation")
        # similarly for reload action
        reload_btn = QAction("Reload", self)
        # creating a line edit for the url
        self.urlbar = QLineEdit()
        # adding action when return key is pressed
        self.urlbar.returnPressed.connect(self.navigateToUrl)

        # D E V E L O P E R    O N L Y  !!!

        # adding this to the tool bar
        # UnComment only if you are Developer
        # self.addToolBar(navtb)
        # navtb.addWidget(self.urlbar)

        # showing all the components
        self.show()

    # method for updating the title of the window

    def updateTitle(self):
        self.setWindowTitle(appName)

    # method called by the home action

    def navigateToMain(self):
        self.thisApplication.setUrl(QUrl(filePathForEngine))

    # method called by the line edit when return key is pressed
    def navigateToUrl(self):

        # getting url and converting it to QUrl object
        q = QUrl(self.urlbar.text())

        # set the url to the thisApplication
        self.thisApplication.setUrl(q)

    # method for updating url
    # this method is called by the QWebEngineView object

    def updateUrlBar(self, q):

        # setting text to the url bar
        self.urlbar.setText(q.toString())

        # setting cursor position of the url bar
        self.urlbar.setCursorPosition(0)

        url = q.toString()

        functionStartIndex = url.find('?')
        functionToCall = url[functionStartIndex+1:]

        print(f"Function Invoke: {functionToCall}")

        if(functionToCall == 'exit()'):
            exit()


# creating a pyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName(appName)

# creating a main window object
window = MainWindow()

# loop
app.exec_()
