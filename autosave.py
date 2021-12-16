# -*- coding: utf-8 -*-
"""
/***************************************************************************
 autoSaver
                                 A QGIS plugin
 auto save current project
                              -------------------
        begin                : 2014-06-16
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
if False:
    from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QTimer
    from PyQt4.QtGui import *
    from PyQt4.QtGui import QAction, QIcon
    from PyQt4 import uic
    
if True:
    from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QTimer, QFileInfo
    from qgis.PyQt.QtGui import *
    from qgis.PyQt.QtGui import  QIcon
    from qgis.PyQt import uic
    
try:
    from qgis.PyQt.QtGui import QAction
    QGIS3_PLATFORM = None
except:
    from qgis.PyQt.QtWidgets import QAction
    QGIS3_PLATFORM = True

    
from qgis.core import *
from qgis.utils import plugins
import qgis
# Initialize Qt resources from file resources.py
#import .resources_rc
from . import resources_rc
# Import the code for the dialog
from .autosave_dialog import autoSaverDialog
import os.path

class trace:

    def __init__(self):
        self.trace = True
        
    def ce(self,string):
        if self.trace:
            print(string)

class autoSaver:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'autoSaver_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = autoSaverDialog()
        self.tra = trace()


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&autoSaver')
        # TODO: We are going to let the user set this up in a future iteration
        #self.toolbar = self.iface.addToolBar(u'autoSaver')
        #self.toolbar.setObjectName(u'autoSaver')


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('autoSaver', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            #self.toolbar.addAction(action)
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/autoSaver/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'auto save current project'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.cron = QTimer()
        self.cron.timeout.connect(self.cronEvent)
        #self.cron.stop()
        self.initAutoSaver()
        self.dlg.enableAutoSave.clicked.connect(self.enableAutoSave)
        self.dlg.buttonOkNo.accepted .connect(self.acceptedAction)
        self.dlg.buttonOkNo.rejected.connect(self.rejectedAction)
        if QGIS3_PLATFORM:
            self.dlg.enableSaveLayersBuffer.hide()

    def initAutoSaver(self):
        s = QSettings()
        autoSaveEnabled = s.value("autoSaver/enabled", defaultValue =  "undef")
        if autoSaveEnabled == "undef":
            s.setValue("autoSaver/enabled","false")
            s.setValue("autoSaver/alternateBak","true")
            s.setValue("autoSaver/saveLayerInEditMode","false")
            s.setValue("autoSaver/saveLayerBuffer","false")
            s.setValue("autoSaver/interval","10")
            self.dlg.enableAlternate.setChecked(True)
            self.dlg.interval.setText("10")
            self.dlg.enableAlternate.setDisabled(True)
            self.dlg.interval.setDisabled(True)
            self.dlg.intervalLabel.setDisabled(True)
            self.dlg.enableSaveLayers.setDisabled(True)
            self.dlg.enableSaveLayers.setDisabled(True)
            #self.dlg.enableSaveLayersBuffer.setUnchecked(True)
            self.dlg.enableSaveLayersBuffer.setChecked(False)
            #self.dlg.enableSaveLayersBuffer.setDisabled(True)
            self.dlg.enableSaveLayersBuffer.setEnabled(False)
        elif autoSaveEnabled == "true":
            self.startAutosave(s.value("autoSaver/interval",""))
            self.dlg.enableAlternate.setEnabled(True)
            self.dlg.interval.setEnabled(True)
            self.dlg.intervalLabel.setEnabled(True)
            self.dlg.interval.setText(s.value("autoSaver/interval", ""))
            self.dlg.enableAutoSave.setChecked(True)
            if s.value("autoSaver/alternateBak", "") == "true":
                self.dlg.enableAlternate.setChecked(True)
            else:
                self.dlg.enableAlternate.setChecked(bool(None))
            self.dlg.enableSaveLayers.setEnabled(True)
            if s.value("autoSaver/saveLayerInEditMode", "") == "true":
                self.dlg.enableSaveLayers.setChecked(True)
                if 'layerVersion' in plugins:
                    self.dlg.enableSaveLayersBuffer.setEnabled(True)
                    if s.value("autoSaver/saveLayerBuffer", "") == "true":
                        self.dlg.enableSaveLayersBuffer.setChecked(True)
                    else:
                        self.dlg.enableSaveLayersBuffer.setChecked(bool(None))
                else:
                    #self.dlg.enableSaveLayersBuffer.setDisabled(True)
                    self.dlg.enableSaveLayersBuffer.setEnabled(False)
            else:
                self.dlg.enableSaveLayers.setChecked(bool(None))
                
        elif autoSaveEnabled == "false":
            #self.startAutosave(s.value("autoSaver/interval"),"")
            self.dlg.enableAlternate.setDisabled(True)
            self.dlg.interval.setDisabled(True)
            self.dlg.intervalLabel.setDisabled(True)
            self.dlg.enableAutoSave.setChecked(False)
            self.dlg.interval.setText(s.value("autoSaver/interval", ""))
            if s.value("autoSaver/alternateBak", "") == "true":
                self.dlg.enableAlternate.setChecked(True)
            else:
                self.dlg.enableAlternate.setChecked(bool(None))
            self.dlg.enableSaveLayers.setDisabled(True)
            if s.value("autoSaver/saveLayerInEditMode", "") == "true":
                self.dlg.enableSaveLayers.setChecked(True)
            else:
                self.dlg.enableSaveLayers.setChecked(bool(None))
            self.dlg.enableSaveLayersBuffer.setDisabled(True)
            
            if s.value("autoSaver/saveLayerInEditMode", "") == "true":
                self.dlg.enableSaveLayers.setChecked(True)
                if 'layerVersion' in plugins:
                    self.dlg.enableSaveLayersBuffer.setEnabled(True)
                    if s.value("autoSaver/saveLayerBuffer", "") == "true":
                        self.dlg.enableSaveLayersBuffer.setChecked(True)
                    else:
                        self.dlg.enableSaveLayersBuffer.setChecked(bool(None))
                else:
                    self.dlg.enableSaveLayersBuffer.setDisabled(True)
            else:
                self.dlg.enableSaveLayers.setChecked(bool(None))

    def enableAutoSave(self):
        if self.dlg.enableAutoSave.isChecked():
            self.dlg.enableAlternate.setEnabled(True)
            self.dlg.interval.setEnabled(True)
            self.dlg.intervalLabel.setEnabled(True)
            self.dlg.enableSaveLayers.setEnabled(True)
            if 'layerVersion' in plugins:
                self.dlg.enableSaveLayersBuffer.setEnabled(True)
            else:
                self.dlg.enableSaveLayersBuffer.setDisabled(True)
        else:
            self.dlg.enableAlternate.setDisabled(True)
            self.dlg.interval.setDisabled(True)
            self.dlg.intervalLabel.setDisabled(True)
            self.dlg.enableSaveLayers.setDisabled(True)
            self.dlg.enableSaveLayersBuffer.setDisabled(True)

    def rejectedAction(self):
        self.dlg.hide()

    def acceptedAction(self):
        try:
            number = int(self.dlg.interval.text())
        except Exception as e :
            QMessageBox.about(None, 'Error','Interval can only be a number')
            return None
        s = QSettings()
        if self.dlg.enableAutoSave.isChecked():
            s.setValue("autoSaver/enabled","true")
            if self.dlg.enableAlternate.isChecked():
                s.setValue("autoSaver/alternateBak","true")
            else:
                s.setValue("autoSaver/alternateBak","false")
            if self.dlg.enableSaveLayers.isChecked():
                s.setValue("autoSaver/saveLayerInEditMode","true")
            else:
                s.setValue("autoSaver/saveLayerInEditMode","false")
            if self.dlg.enableSaveLayersBuffer.isChecked():
                s.setValue("autoSaver/saveLayerBuffer","true")
            else:
                s.setValue("autoSaver/saveLayerBuffer","false")
            s.setValue("autoSaver/interval",self.dlg.interval.text())
            self.startAutosave(self.dlg.interval.text())
        else:
            s.setValue("autoSaver/enabled","false")
            if self.dlg.enableAlternate.isChecked():
                s.setValue("autoSaver/alternateBak","true")
            else:
                s.setValue("autoSaver/alternateBak","false")
            if self.dlg.enableSaveLayers.isChecked():
                s.setValue("autoSaver/saveLayerInEditMode","true")
            else:
                s.setValue("autoSaver/saveLayerInEditMode","false")
            if self.dlg.enableSaveLayersBuffer.isChecked():
                s.setValue("autoSaver/saveLayerBuffer","true")
            else:
                s.setValue("autoSaver/saveLayerBuffer","false")
            s.setValue("autoSaver/interval",self.dlg.interval.text())
            self.stopAutosave()
        self.dlg.hide()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.cron.stop()
        self.cron.timeout.disconnect(self.cronEvent)
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&autoSaver'),
                action)
            self.iface.removeToolBarIcon(action)

    def startAutosave(self,interval):
        self.cron.start(int(interval)*60000)

    def stopAutosave(self):
        self.cron.stop()

    def cronEvent(self):
        if self.dlg.enableSaveLayers.isChecked():
            self.saveLayersInEditMode()
        self.saveCurrentProject()

    def saveLayersInEditMode(self):
        if 'layerVersion' in plugins and self.dlg.enableSaveLayersBuffer.isChecked():
            lv = plugins['layerVersion']
            DOM = lv.editingStateSaver.getEditsXMLDefinition()
            if DOM:
                outFile = open(os.path.join(QgsProject.instance().readPath("./"),"autosave.qlv"), "w")
                outFile.write(DOM.toString())
                outFile.close
        else:
            for layer in self.iface.mapCanvas().layers():
                if layer.isEditable() and layer.isModified():
                    layer.commitChanges()
                    layer.startEditing()
                    #self.tra.ce(u"autosaved"+layer.name())
                    if QGIS3_PLATFORM:
                        self.iface.messageBar().pushSuccess("Autosaver", u"autosaved : "+layer.name())
                    else:
                        self.iface.messageBar().pushMessage("Autosave", u"autosaved : "+layer.name(), level=qgis.gui.QgsMessageBar.SUCCESS, duration=3 )

    def saveCurrentProject(self):
        origFileName = QgsProject.instance().fileName()
        if origFileName != "" and QgsProject.instance().isDirty():
            if self.dlg.enableAlternate.isChecked():

                extension = QFileInfo(origFileName).completeSuffix()
                basename = QFileInfo(origFileName).baseName()
                basedir = QFileInfo(origFileName).dir().absolutePath()

                basename,extension = os.path.splitext(origFileName)

                bakFileName = basename + "_bak" + extension
                targetBakFile = origFileName + '.bak'
                try:
                    os.remove(targetBakFile)
                    os.remove(bakFileName)
                except:
                    pass
                msg = u"project autosaved to: "+targetBakFile
            else:
                bakFileName = origFileName
                msg = u"project autosaved"
            QgsProject.instance().setFileName(bakFileName)
            QgsProject.instance().write()
            QgsProject.instance().setFileName(origFileName)
            if self.dlg.enableAlternate.isChecked():
                os.rename(bakFileName, targetBakFile)
            if QGIS3_PLATFORM:
                self.iface.messageBar().pushSuccess("Autosaver", msg)
            else:
                self.iface.messageBar().pushMessage("Autosave", msg, level=qgis.gui.QgsMessageBar.SUCCESS, duration=3 )

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
