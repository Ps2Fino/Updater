# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updater_qt\updater.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui, uic

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Updater(object):
    def setupUi(self, Updater):
        Updater.setObjectName(_fromUtf8("Updater"))
        Updater.resize(1600, 1200)
        self.centralWidget = QtGui.QWidget(Updater)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.pushButton = QtGui.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 120, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        Updater.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(Updater)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        Updater.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(Updater)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        Updater.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(Updater)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        Updater.setStatusBar(self.statusBar)
        self.actionGenerate = QtGui.QAction(Updater)
        self.actionGenerate.setObjectName(_fromUtf8("actionGenerate"))
        self.menuFile.addAction(self.actionGenerate)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(Updater)
        QtCore.QMetaObject.connectSlotsByName(Updater)

    def retranslateUi(self, Updater):
        Updater.setWindowTitle(_translate("Updater", "Updater", None))
        self.pushButton.setText(_translate("Updater", "Press me", None))
        self.menuFile.setTitle(_translate("Updater", "File", None))
        self.actionGenerate.setText(_translate("Updater", "Generate", None))

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('updater_qt/updater.ui', self)
        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())