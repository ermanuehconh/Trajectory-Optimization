# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'waypoints.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLineEdit,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(449, 300)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.J1waypoint = QLineEdit(Form)
        self.J1waypoint.setObjectName(u"J1waypoint")

        self.horizontalLayout.addWidget(self.J1waypoint)

        self.J2waypoint = QLineEdit(Form)
        self.J2waypoint.setObjectName(u"J2waypoint")

        self.horizontalLayout.addWidget(self.J2waypoint)

        self.J3waypoint = QLineEdit(Form)
        self.J3waypoint.setObjectName(u"J3waypoint")

        self.horizontalLayout.addWidget(self.J3waypoint)

        self.J4waypoint = QLineEdit(Form)
        self.J4waypoint.setObjectName(u"J4waypoint")

        self.horizontalLayout.addWidget(self.J4waypoint)

        self.J5waypoint = QLineEdit(Form)
        self.J5waypoint.setObjectName(u"J5waypoint")

        self.horizontalLayout.addWidget(self.J5waypoint)

        self.J6waypoint = QLineEdit(Form)
        self.J6waypoint.setObjectName(u"J6waypoint")

        self.horizontalLayout.addWidget(self.J6waypoint)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.waypointsTable = QTableWidget(Form)
        if (self.waypointsTable.columnCount() < 6):
            self.waypointsTable.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.waypointsTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.waypointsTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.waypointsTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.waypointsTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.waypointsTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.waypointsTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.waypointsTable.setObjectName(u"waypointsTable")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waypointsTable.sizePolicy().hasHeightForWidth())
        self.waypointsTable.setSizePolicy(sizePolicy)
        self.waypointsTable.setAutoFillBackground(False)
        self.waypointsTable.setRowCount(0)

        self.verticalLayout_2.addWidget(self.waypointsTable)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.addButton = QPushButton(Form)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout_2.addWidget(self.addButton)

        self.deleteButton = QPushButton(Form)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setStyleSheet(u"background-color: rgb(255, 0, 0);")

        self.horizontalLayout_2.addWidget(self.deleteButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.optimizeButton = QPushButton(Form)
        self.optimizeButton.setObjectName(u"optimizeButton")

        self.verticalLayout_2.addWidget(self.optimizeButton)

        self.backButton = QPushButton(Form)
        self.backButton.setObjectName(u"backButton")

        self.verticalLayout_2.addWidget(self.backButton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        ___qtablewidgetitem = self.waypointsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"J1", None));
        ___qtablewidgetitem1 = self.waypointsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"J2", None));
        ___qtablewidgetitem2 = self.waypointsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"J3", None));
        ___qtablewidgetitem3 = self.waypointsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"J4", None));
        ___qtablewidgetitem4 = self.waypointsTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"J5", None));
        ___qtablewidgetitem5 = self.waypointsTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"J6", None));
        self.addButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.deleteButton.setText(QCoreApplication.translate("Form", u"Delete", None))
        self.optimizeButton.setText(QCoreApplication.translate("Form", u"Optimize", None))
        self.backButton.setText(QCoreApplication.translate("Form", u"Back", None))
    # retranslateUi

