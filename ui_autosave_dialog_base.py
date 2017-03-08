# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_autosave_dialog_base.ui'
#
# Created: Thu Oct 09 11:09:51 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

#from PyQt4 import QtCore, QtGui
from qgis.PyQt import QtCore, QtGui

try:
    from qgis.PyQt.QtGui import QDialogButtonBox, QCheckBox, QLabel, QLineEdit, QApplication
except:
    from qgis.PyQt.QtWidgets import QDialogButtonBox, QCheckBox, QLabel, QLineEdit, QApplication

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_autoSaverDialogBase(object):
    def setupUi(self, autoSaverDialogBase):
        autoSaverDialogBase.setObjectName(_fromUtf8("autoSaverDialogBase"))
        autoSaverDialogBase.resize(364, 141)
        self.buttonOkNo = QDialogButtonBox(autoSaverDialogBase)
        self.buttonOkNo.setGeometry(QtCore.QRect(185, 103, 171, 32))
        self.buttonOkNo.setOrientation(QtCore.Qt.Horizontal)
        self.buttonOkNo.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonOkNo.setObjectName(_fromUtf8("buttonOkNo"))
        self.enableAutoSave = QCheckBox(autoSaverDialogBase)
        self.enableAutoSave.setGeometry(QtCore.QRect(30, 10, 151, 17))
        self.enableAutoSave.setObjectName(_fromUtf8("enableAutoSave"))
        self.enableAlternate = QCheckBox(autoSaverDialogBase)
        self.enableAlternate.setGeometry(QtCore.QRect(30, 30, 321, 17))
        self.enableAlternate.setObjectName(_fromUtf8("enableAlternate"))
        self.interval = QLineEdit(autoSaverDialogBase)
        self.interval.setGeometry(QtCore.QRect(12, 110, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.interval.setFont(font)
        self.interval.setInputMethodHints(QtCore.Qt.ImhNone)
        self.interval.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.interval.setObjectName(_fromUtf8("interval"))
        self.intervalLabel = QLabel(autoSaverDialogBase)
        self.intervalLabel.setGeometry(QtCore.QRect(48, 110, 91, 16))
        self.intervalLabel.setObjectName(_fromUtf8("intervalLabel"))
        self.enableSaveLayers = QCheckBox(autoSaverDialogBase)
        self.enableSaveLayers.setGeometry(QtCore.QRect(30, 50, 221, 18))
        self.enableSaveLayers.setObjectName(_fromUtf8("enableSaveLayers"))
        self.enableSaveLayersBuffer = QCheckBox(autoSaverDialogBase)
        self.enableSaveLayersBuffer.setGeometry(QtCore.QRect(30, 70, 321, 18))
        self.enableSaveLayersBuffer.setObjectName(_fromUtf8("enableSaveLayersBuffer"))

        self.retranslateUi(autoSaverDialogBase)
        QtCore.QMetaObject.connectSlotsByName(autoSaverDialogBase)

    def retranslateUi(self, autoSaverDialogBase):
        autoSaverDialogBase.setWindowTitle(_translate("autoSaverDialogBase", "autoSaver", None))
        self.enableAutoSave.setText(_translate("autoSaverDialogBase", "Enable auto saver", None))
        self.enableAlternate.setText(_translate("autoSaverDialogBase", "Auto save in alternate backup file (*.bak)", None))
        self.interval.setInputMask(_translate("autoSaverDialogBase", "00; ", None))
        self.intervalLabel.setText(_translate("autoSaverDialogBase", "Interval (minutes)", None))
        self.enableSaveLayers.setText(_translate("autoSaverDialogBase", "Auto save layers in edit mode", None))
        self.enableSaveLayersBuffer.setText(_translate("autoSaverDialogBase", "Auto save layers in file *.qlv (to open with layerVersion plugin)", None))

