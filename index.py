from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget
from PyQt5.uic import loadUiType
import os
from os import path
import sys
import lackey
from keyboard import press

Main_Ui,_= loadUiType(path.join(path.dirname(__file__), 'main.ui'))
theCreator,_= loadUiType(path.join(path.dirname(__file__), 'creator app2.ui'))

class Creator(QWidget, theCreator):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setFixedSize(380, 550)
        # self.setWindowIcon(QIcon(path.join(path.dirname(__file__), 'Icon.ico')))
        self.App()
    
    def App(self):
        self.label.setPixmap(QPixmap(path.join(path.dirname(__file__), 'creator.jpg')))
        self.pushButton.clicked.connect(lambda: self.close())

class MainApp(QMainWindow, Main_Ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent=parent)
        self.setupUi(self)
        # Setup Variables
        self.location = path.dirname(path.realpath(__file__))
        self.binFilesPath = ""
        # Start Seting Up The Ui
        self.setFixedSize(311, 446)
        # self.setWindowIcon(QIcon(path.join(path.dirname(__file__), 'Icon.ico')))
        self.setupApp()

    def setupApp(self):
        self.status.setHtml('<p align="center"><span style=" font-size:11pt; font-weight:600; color:#ff0000;">Down</span></p>')
        self.statusPrepare.setHtml('')
        self.statusOperation.setHtml('')
        self.folderPath.setText(self.store_location(False))
        # self.fileNumber
        self.browseFile.clicked.connect(self.browse_file)
        self.prepareFiles.clicked.connect(self.get_fileName_ready)
        self.startOperation.clicked.connect(self.start_operation)
        self.actionCreator.triggered.connect(self.creator)
        self.folderPath.textChanged.connect(self.change_value)
    
    def start_operation(self):
        print("Operation Started")
        # Disable buttons
        self.startOperation.setEnabled(False)
        self.prepareFiles.setEnabled(False)
        # Change Word
        self.status.setHtml('<p align="center"><span style=" font-size:11pt; font-weight:600; color:#00aa00;">Up</span></p>')
        self.statusOperation.setHtml('<p align="center"><span style=" font-size:11pt; font-weight:600;">جاري التشغيل</span></p>')
        # Start automation
        try:
            self.start_testing()
        except:
            self.startOperation.setEnabled(True)
            self.prepareFiles.setEnabled(True)
            self.status.setHtml('<p align="center"><span style=" font-size:11pt; font-weight:600; color:#ff0000;">Down</span></p>')
            self.statusOperation.setHtml('<p align="center"><span style=" font-size:11pt; font-weight:600; color:#ff0000;">فشل في العملية</span></p>')
            return 0
        # Enable buttons again
        self.startOperation.setEnabled(True)
        self.prepareFiles.setEnabled(True)
        self.status.setHtml('<p align="center"><span style=" font-size:11pt; font-weight:600; color:#ff0000;">Down</span></p>')
        self.statusOperation.setHtml('<p align="center"><span style=" font-size:11pt; font-weight:600; color:#00aa00;">تمت العملية بنجاح</span></p>')
    
    def start_testing(self):
        for n in range(1,31):
            self.fileNumber.display(n)
            lackey.click(self.location + r"\src\browse.png")
            lackey.click(self.location + r"\src\name.png")
            lackey.type("%d.bin" % n)
            lackey.click(self.location + r"\src\open.png")
            lackey.click(self.location + r"\src\mode.png")
            press("u")
            press("enter")
            lackey.click(self.location + r"\src\next.png")
            if lackey.exists(self.location + r"\src\error.png", 8):
                lackey.click(self.location + r"\src\back.png")
            else:
                lackey.wait(self.location + r"\src\next2.png", 6)
                lackey.click(self.location + r"\src\next2.png")
                lackey.wait(self.location + r"\src\finish.png", 8)
                lackey.click(self.location + r"\src\finish.png")
                break

    def get_fileName_ready(self):
        if path.isdir(self.binFilesPath):
            # print(os.listdir(self.binFilesPath)[0][-3:].lower())
            if os.listdir(self.binFilesPath)[0][-3:].lower() == 'bin':
                Counter = 1
                for f in os.listdir(self.binFilesPath):
                    if f.isnumeric():
                        if not int(f[:-4]) in range(0, 31):
                            os.rename(path.join(self.binFilesPath, f), path.join(self.binFilesPath, str(Counter) + '.bin'))    
                    else:
                        os.rename(path.join(self.binFilesPath, f), path.join(self.binFilesPath, str(Counter) + '.bin'))

                    Counter += 1
                self.statusPrepare.setHtml('<p align="center"><span style=" font-size:11pt; font-weight:600; color:#00aa00;">تم</span></p>')
                return 0
        
        self.statusPrepare.setHtml('<p align="center"><span style=" font-size:11pt; font-weight:600; color:#ff0000;">خطأ في المكان</span></p>')

    def browse_file(self):
        fname = QFileDialog.getExistingDirectory(self, 'تحديد مكان ملفات القنوات', 'C:\\')
        # fname = QFileDialog.getOpenFileName(self, 'Open File', "C:\\")
        if fname:
            self.binFilesPath = fname
            self.folderPath.setText(self.binFilesPath)
            self.store_location()
    
    def change_value(self):
        self.binFilesPath = self.folderPath.text()
    
    def store_location(self, write=True):
        if not path.exists(path.join(path.dirname(__file__), 'location.txt')):
            f = open('location.txt', 'x')
            f.close()
        
        if write:
            with open('location.txt', 'wt') as f:
                f.writelines(self.binFilesPath)
                f.close()
        else: 
            with open('location.txt', 'rt') as f:
                self.binFilesPath = f.readline()
                f.close()
        return self.binFilesPath
    
    def creator(self):
        c = Creator()
        c.show()

def main():
    app = QApplication(sys.argv)
    mainWindow = MainApp()

    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()