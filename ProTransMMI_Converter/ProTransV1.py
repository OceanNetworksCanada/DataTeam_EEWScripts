# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProTransV1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_MainWindow(object):
#%% Defines the ap;lication layout
    def setupUi(self, MainWindow):
        #   Set up bin folder and get working directory
        os.makedirs("_bin", exist_ok = True)
        self.curdir = os.getcwd()
        self.parms = self.curdir + '/_bin'
                
        #   Get the ONC API key
        with open(self.parms + '/Parameters.txt', 'r') as p:
            key = p.readlines(0)
            
        try:
            
        
        
        
        #   Define the main application window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1190, 775)
        MainWindow.setMinimumSize(QtCore.QSize(1190, 775))
        MainWindow.setBaseSize(QtCore.QSize(1194, 775))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #   Define the JMA Plot and JMA Plot Widget
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(9, -1, 521, 611))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.JMA_Plot = QtWidgets.QGroupBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.JMA_Plot.setFont(font)
        self.JMA_Plot.setObjectName("JMA_Plot")
        self.JMAPlot_Widg = QtWidgets.QWidget(self.JMA_Plot)
        self.JMAPlot_Widg.setGeometry(QtCore.QRect(0, 20, 500, 260))
        self.JMAPlot_Widg.setMinimumSize(QtCore.QSize(500, 260))
        self.JMAPlot_Widg.setMaximumSize(QtCore.QSize(500, 260))
        self.JMAPlot_Widg.setObjectName("JMAPlot_Widg")
        self.gridLayout_2.addWidget(self.JMA_Plot, 0, 0, 1, 1)
        
        #   Define MMI Plot and MMI Plot Widget
        self.MMI_Plot = QtWidgets.QGroupBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.MMI_Plot.setFont(font)
        self.MMI_Plot.setObjectName("MMI_Plot")
        self.MMIPlot_Widg = QtWidgets.QWidget(self.MMI_Plot)
        self.MMIPlot_Widg.setGeometry(QtCore.QRect(0, 20, 500, 260))
        self.MMIPlot_Widg.setMinimumSize(QtCore.QSize(500, 260))
        self.MMIPlot_Widg.setMaximumSize(QtCore.QSize(500, 260))
        self.MMIPlot_Widg.setObjectName("MMIPlot_Widg")
        self.gridLayout_2.addWidget(self.MMI_Plot, 1, 0, 1, 1)
        
        #   Define the MMI Map
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(530, 0, 651, 611))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.MMI_Map_Web = QtWebEngineWidgets.QWebEngineView(self.groupBox_3)
        self.MMI_Map_Web.setGeometry(QtCore.QRect(10, 30, 631, 571))
        self.MMI_Map_Web.setUrl(QtCore.QUrl("about:blank"))
        self.MMI_Map_Web.setObjectName("MMI_Map_Web")
        
        #   Define the time button frames
        self.TimeFramer = QtWidgets.QFrame(self.centralwidget)
        self.TimeFramer.setGeometry(QtCore.QRect(10, 610, 1171, 124))
        self.TimeFramer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TimeFramer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TimeFramer.setObjectName("TimeFramer")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.TimeFramer)
        self.gridLayout_7.setObjectName("gridLayout_7")
        
        #   Define the statice event selection
        self.StatEvent_Group = QtWidgets.QGroupBox(self.TimeFramer)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.StatEvent_Group.setFont(font)
        self.StatEvent_Group.setObjectName("StatEvent_Group")
        self.gridLayout = QtWidgets.QGridLayout(self.StatEvent_Group)
        self.gridLayout.setObjectName("gridLayout")
        self.StartTime_Group = QtWidgets.QGroupBox(self.StatEvent_Group)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.StartTime_Group.setFont(font)
        self.StartTime_Group.setObjectName("StartTime_Group")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.StartTime_Group)
        self.gridLayout_4.setObjectName("gridLayout_4")
        
        #   Define the static date/time selector
        self.Stat_dateTimeEdit = QtWidgets.QDateTimeEdit(self.StartTime_Group)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Stat_dateTimeEdit.setFont(font)
        self.Stat_dateTimeEdit.setAccelerated(True)
        self.Stat_dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2010, 1, 1), QtCore.QTime(0, 0, 0)))
        self.Stat_dateTimeEdit.setDate(QtCore.QDate(2010, 1, 1))
        self.Stat_dateTimeEdit.setMinimumDate(QtCore.QDate(2010, 1, 1))
        self.Stat_dateTimeEdit.setCalendarPopup(True)
        self.Stat_dateTimeEdit.setObjectName("Stat_dateTimeEdit")
        self.gridLayout_4.addWidget(self.Stat_dateTimeEdit, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.StartTime_Group, 0, 1, 1, 1)
        
        #   Define the static duration entry box
        self.Stat_Duration = QtWidgets.QGroupBox(self.StatEvent_Group)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Stat_Duration.setFont(font)
        self.Stat_Duration.setObjectName("Stat_Duration")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Stat_Duration)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Stat_TimeDur = QtWidgets.QLineEdit(self.Stat_Duration)
        self.Stat_TimeDur.setObjectName("Stat_TimeDur")
        self.gridLayout_3.addWidget(self.Stat_TimeDur, 0, 0, 1, 1)
        self.Stat_TimeUnit = QtWidgets.QComboBox(self.Stat_Duration)
        self.Stat_TimeUnit.setObjectName("Stat_TimeUnit")
        self.Stat_TimeUnit.addItem("")
        self.Stat_TimeUnit.addItem("")
        self.Stat_TimeUnit.addItem("")
        self.gridLayout_3.addWidget(self.Stat_TimeUnit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.Stat_Duration, 0, 2, 1, 1)
        
        #   Define the static event start
        self.RunStatic = QtWidgets.QPushButton(self.StatEvent_Group)
        self.RunStatic.setObjectName("RunStatic")
        self.gridLayout.addWidget(self.RunStatic, 0, 3, 1, 1)
        self.gridLayout_7.addWidget(self.StatEvent_Group, 0, 1, 1, 1)
        
        #   Define the live event buttons
        self.LiveFeed_Group = QtWidgets.QGroupBox(self.TimeFramer)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.LiveFeed_Group.setFont(font)
        self.LiveFeed_Group.setObjectName("LiveFeed_Group")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.LiveFeed_Group)
        self.gridLayout_6.setObjectName("gridLayout_6")
        
        #   Define the live duration entry
        self.Live_Duration = QtWidgets.QGroupBox(self.LiveFeed_Group)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Live_Duration.setFont(font)
        self.Live_Duration.setObjectName("Live_Duration")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.Live_Duration)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.Live_TimeDur = QtWidgets.QLineEdit(self.Live_Duration)
        self.Live_TimeDur.setObjectName("Live_TimeDur")
        self.gridLayout_5.addWidget(self.Live_TimeDur, 0, 0, 1, 1)
        self.Live_TimeUnit = QtWidgets.QComboBox(self.Live_Duration)
        self.Live_TimeUnit.setObjectName("Live_TimeUnit")
        self.Live_TimeUnit.addItem("")
        self.Live_TimeUnit.addItem("")
        self.Live_TimeUnit.addItem("")
        self.gridLayout_5.addWidget(self.Live_TimeUnit, 0, 1, 1, 1)
        self.gridLayout_6.addWidget(self.Live_Duration, 0, 1, 2, 1)
        
        #   Define the start live button
        self.GoLive = QtWidgets.QPushButton(self.LiveFeed_Group)
        self.GoLive.setObjectName("GoLive")
        self.gridLayout_6.addWidget(self.GoLive, 0, 2, 1, 1)
        
        #   Define the stop live button
        self.StopLive = QtWidgets.QPushButton(self.LiveFeed_Group)
        self.StopLive.setObjectName("StopLive")
        self.gridLayout_6.addWidget(self.StopLive, 1, 2, 1, 1)
        self.gridLayout_7.addWidget(self.LiveFeed_Group, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem1, 0, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        
        #   Define the menu options
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1190, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        #   Define get ONC key
        self.actionUpdate_ONC_Key = QtWidgets.QAction(MainWindow)
        self.actionUpdate_ONC_Key.setObjectName("actionUpdate_ONC_Key")
        
        #   Define quit application
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionUpdate_ONC_Key)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
#%% Defines Variable attributes
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ProTrans MMI Conversion"))
        self.groupBox.setTitle(_translate("MainWindow", "Plots"))
        self.JMA_Plot.setTitle(_translate("MainWindow", "JMA"))
        self.MMI_Plot.setTitle(_translate("MainWindow", "MMI"))
        self.groupBox_3.setTitle(_translate("MainWindow", "MMI Map"))
        self.MMI_Map_Web.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:400;\">Map around the ProTrans site that shows the extent of shaking in the immediate area</span></p></body></html>"))
        self.StatEvent_Group.setTitle(_translate("MainWindow", "Static Event"))
        self.StartTime_Group.setTitle(_translate("MainWindow", "Start Time"))
        self.Stat_dateTimeEdit.setToolTip(_translate("MainWindow", "<html><head/><body><p>Time of an earthquake event</p></body></html>"))
        self.Stat_dateTimeEdit.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd hh:mm:ss"))
        self.Stat_Duration.setTitle(_translate("MainWindow", "Duration"))
        self.Stat_TimeDur.setToolTip(_translate("MainWindow", "<html><head/><body><p>Duration of time in the units selected to the right before and after the selected event start time.</p></body></html>"))
        self.Stat_TimeUnit.setItemText(0, _translate("MainWindow", "Seconds"))
        self.Stat_TimeUnit.setItemText(1, _translate("MainWindow", "Minutes"))
        self.Stat_TimeUnit.setItemText(2, _translate("MainWindow", "Hours"))
        self.RunStatic.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:400;\">Run static event</span></p></body></html>"))
        self.RunStatic.setText(_translate("MainWindow", "Run Static"))
        self.LiveFeed_Group.setTitle(_translate("MainWindow", "Live Feed"))
        self.Live_Duration.setTitle(_translate("MainWindow", "Duration"))
        self.Live_TimeDur.setToolTip(_translate("MainWindow", "<html><head/><body><p>Duration of time in the units selected to the right that will be displayed within the plots</p></body></html>"))
        self.Live_TimeUnit.setItemText(0, _translate("MainWindow", "Seconds"))
        self.Live_TimeUnit.setItemText(1, _translate("MainWindow", "Minutes"))
        self.Live_TimeUnit.setItemText(2, _translate("MainWindow", "Hours"))
        self.GoLive.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:400;\">Start live feed</span></p></body></html>"))
        self.GoLive.setText(_translate("MainWindow", "Go Live!"))
        self.StopLive.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:400;\">Stop live feed</span></p></body></html>"))
        self.StopLive.setText(_translate("MainWindow", "Stop Live!"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionUpdate_ONC_Key.setText(_translate("MainWindow", "Update ONC Key"))
        self.actionUpdate_ONC_Key.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

#%% Gets the ONC user API key to access Oceans2.0        
    def getONC(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text","Your name:", QtWidgets.QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)

from PyQt5 import QtWebEngineWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

