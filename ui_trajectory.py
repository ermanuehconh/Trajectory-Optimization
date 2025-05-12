# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trajectory.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSlider,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(278, 369)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.trajectoryTable = QTableWidget(Form)
        if (self.trajectoryTable.columnCount() < 7):
            self.trajectoryTable.setColumnCount(7)
        self.trajectoryTable.setObjectName(u"trajectoryTable")
        self.trajectoryTable.setColumnCount(7)

        self.verticalLayout_2.addWidget(self.trajectoryTable)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.velocityLabel = QLabel(Form)
        self.velocityLabel.setObjectName(u"velocityLabel")

        self.verticalLayout.addWidget(self.velocityLabel)

        self.velocitySlider = QSlider(Form)
        self.velocitySlider.setObjectName(u"velocitySlider")
        self.velocitySlider.setMaximum(100)
        self.velocitySlider.setSingleStep(1)
        self.velocitySlider.setPageStep(1)
        self.velocitySlider.setValue(70)
        self.velocitySlider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout.addWidget(self.velocitySlider)

        self.velocityValue = QLabel(Form)
        self.velocityValue.setObjectName(u"velocityValue")

        self.verticalLayout.addWidget(self.velocityValue)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.acelerationLabel = QLabel(Form)
        self.acelerationLabel.setObjectName(u"acelerationLabel")

        self.verticalLayout_3.addWidget(self.acelerationLabel)

        self.acelerationSlider = QSlider(Form)
        self.acelerationSlider.setObjectName(u"acelerationSlider")
        self.acelerationSlider.setMaximum(100)
        self.acelerationSlider.setSingleStep(1)
        self.acelerationSlider.setPageStep(1)
        self.acelerationSlider.setValue(70)
        self.acelerationSlider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout_3.addWidget(self.acelerationSlider)

        self.acelerationValue = QLabel(Form)
        self.acelerationValue.setObjectName(u"acelerationValue")

        self.verticalLayout_3.addWidget(self.acelerationValue)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.homeButton = QPushButton(Form)
        self.homeButton.setObjectName(u"homeButton")
        self.homeButton.setStyleSheet(u"background-color: rgb(86, 86, 86);")

        self.horizontalLayout_2.addWidget(self.homeButton)

        self.firstpointButton = QPushButton(Form)
        self.firstpointButton.setObjectName(u"firstpointButton")
        self.firstpointButton.setStyleSheet(u"background-color: rgb(86, 86, 86);")

        self.horizontalLayout_2.addWidget(self.firstpointButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.loggingCheck = QCheckBox(Form)
        self.loggingCheck.setObjectName(u"loggingCheck")
        self.loggingCheck.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"font: 9pt \"Segoe UI\";\n"
"border-color: rgb(13, 13, 13);\n"
"color: #000000;")

        self.verticalLayout_2.addWidget(self.loggingCheck)

        self.sendButton = QPushButton(Form)
        self.sendButton.setObjectName(u"sendButton")

        self.verticalLayout_2.addWidget(self.sendButton)

        self.backButton = QPushButton(Form)
        self.backButton.setObjectName(u"backButton")

        self.verticalLayout_2.addWidget(self.backButton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Trajectory", None))
        self.velocityLabel.setText(QCoreApplication.translate("Form", u"Velocity", None))
        self.velocityValue.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.acelerationLabel.setText(QCoreApplication.translate("Form", u"Aceleration", None))
        self.acelerationValue.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.homeButton.setText(QCoreApplication.translate("Form", u"Home", None))
        self.firstpointButton.setText(QCoreApplication.translate("Form", u"First position", None))
        self.loggingCheck.setText(QCoreApplication.translate("Form", u"logging", None))
        self.sendButton.setText(QCoreApplication.translate("Form", u"Send to robot", None))
        self.backButton.setText(QCoreApplication.translate("Form", u"Back", None))
    # retranslateUi

