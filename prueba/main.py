import sys
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtCore import Qt, QTimer
from ui_form import Ui_Form
from ui_waypoints import Ui_Form as Ui_Waypoints
from ui_trajectory import Ui_Form as Ui_Trajectory
from ui_loading import Ui_Form as Ui_Loading
from ui_results import Ui_Form as Ui_Results
import TrajectoryPlannerV1_0 as tp
import RobotExecuterV1_0 as re
import numpy as np

class MainWindow(QWidget):
    def __init__(self,stack):
        super().__init__()
        self.stack = stack

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.button1_clicked)
        self.ui.pushButton_2.clicked.connect(self.button2_clicked)

    def button1_clicked(self):
        self.stack.setCurrentIndex(1)

    def button2_clicked(self):
        print("Button 2 clicked!")

class WaypointWindow(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.ui = Ui_Waypoints()
        self.ui.setupUi(self)

        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.optimizeButton.clicked.connect(self.go_foward)
        self.ui.addButton.clicked.connect(self.add_waypoint)
        self.ui.deleteButton.clicked.connect(self.delete_selected_row)
        self.ui.waypointsTable.horizontalHeader().setStretchLastSection(True)
        self.ui.waypointsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.waypointsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.waypointsTable.setSelectionMode(QAbstractItemView.SingleSelection)


    def go_back(self):
        self.stack.setCurrentIndex(0)

    def go_foward(self):
        waypoints = []
        for row in range(self.ui.waypointsTable.rowCount()):
            wp = []
            for col in range(6):
                item = self.ui.waypointsTable.item(row, col)
                wp.append(float(item.text()) if item else 0.0)
            waypoints.append(wp)

        if len(waypoints) < 2:
            print("Add at least two waypoints.")
            return

        try:
            optimized = tp.optimize_from_waypoints_deg(waypoints)
            self.stack.widget(2).show_trajectory(optimized)  # Enviar a TrajectoryWindow
            self.stack.setCurrentIndex(2)
        except Exception as e:
            print("Optimization error:", e)

    def add_waypoint(self):
        inputs = [
            self.ui.J1waypoint.text(), self.ui.J2waypoint.text(), self.ui.J3waypoint.text(),
            self.ui.J4waypoint.text(), self.ui.J5waypoint.text(), self.ui.J6waypoint.text()
        ]
        row = self.ui.waypointsTable.rowCount()
        self.ui.waypointsTable.insertRow(row)

        for col, val in enumerate(inputs):
            safe_value = val if val else "0"
            item = QTableWidgetItem(safe_value)
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.waypointsTable.setItem(row, col, item)

    def delete_selected_row(self):
        selected_row = self.ui.waypointsTable.currentRow()
        if selected_row != -1:
            self.ui.waypointsTable.removeRow(selected_row)


class TrajectoryWindow(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.ui = Ui_Trajectory()
        self.ui.setupUi(self)

        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.sendButton.clicked.connect(self.change_window)
        self.ui.acelerationSlider.valueChanged.connect(self.update_av_labels)
        self.ui.velocitySlider.valueChanged.connect(self.update_av_labels)
        self.update_av_labels()  # Inicializar con los valores actuales

    def go_back(self):
        self.stack.setCurrentIndex(1)

    def show_trajectory(self, trajectory_deg):
       

        rows = trajectory_deg.shape[1]  # time steps
        cols = trajectory_deg.shape[0]  # joints (should be 6)

        self.ui.trajectoryTable.setRowCount(rows)
        self.ui.trajectoryTable.setColumnCount(cols)
        self.ui.trajectoryTable.setHorizontalHeaderLabels([f"J{i+1}" for i in range(cols)])

        for i in range(rows):
                for j in range(cols):
                    item = QTableWidgetItem(f"{trajectory_deg[j, i]:.2f}")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.trajectoryTable.setItem(i, j, item)

    # Stretch to fit content
        self.ui.trajectoryTable.horizontalHeader().setStretchLastSection(True)
        self.ui.trajectoryTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.trajectoryTable.verticalHeader().setDefaultSectionSize(30)

        self.ui.label.setText("Optimized Trajectory")
        self.ui.label.setAlignment(Qt.AlignCenter)
    
    def change_window(self):
        self.stack.setCurrentIndex(3)
        QTimer.singleShot(100, self.send_to_robot)
        
    def send_to_robot(self):
        self.stack.setCurrentIndex(3)
        try:
            rows = self.ui.trajectoryTable.rowCount()
            cols = self.ui.trajectoryTable.columnCount()
            trajectory_deg = np.zeros((cols, rows))

            for i in range(rows):
                for j in range(cols):
                    item = self.ui.trajectoryTable.item(i, j)
                    angle = float(item.text()) if item else 0.0
                    trajectory_deg[j, i] = angle

            a = self.ui.acelerationSlider.value()/10
            v = self.ui.velocitySlider.value()/10
            if self.myCheckBox.isChecked():
                filename = re.execute_trajectory_with_logging(trajectory_deg, a, v, file_prefix="trajectory")
                prinbt(f"Trajectory logged in {filename}")
                self.stack.widget(4).ui.label.setText(f"Trajectory logged in {filename}")
            else:
                re.execute_trajectory_without_logging(trajectory_deg, a, v)
            self.stack.setCurrentIndex(4)
        except Exception as e:
            print("Error during execution:", e)

    def update_av_labels(self):
        a = self.ui.acelerationSlider.value()/10
        v = self.ui.velocitySlider.value()/10
        self.ui.acelerationValue.setText(f"a = {a:.2f}")
        self.ui.velocityValue.setText(f"v = {v:.2f}")

class LoadingWindow(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.ui = Ui_Loading()
        self.ui.setupUi(self)

class ResultsWindow(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.ui = Ui_Results()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.go_back)

    def go_back(self):
        self.stack.setCurrentIndex(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stack = QStackedWidget()
    stack.setStyleSheet("""
        QWidget {
            background-color: #f0f2f5;
            font-family: 'Segoe UI';
            font-size: 14px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 6px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLineEdit, QTextEdit {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 6px;
        }
        QTableWidget {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #999999;
            gridline-color: #cccccc;
            selection-background-color: #cceeff;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            color: #333333;
            font-weight: bold;
            padding: 4px;
            border: 1px solid #999999;
        }   
        QTableWidget::item {
            padding: 6px;
        }
        QTableWidget::item:selected {
            background-color: #a0c4ff;
            color: #000000;
        }
        QLabel {
            color: #333333;
            font-weight: bold;
        }
    """)
    main_window = MainWindow(stack)
    waypoint_window = WaypointWindow(stack)
    trajectory_window = TrajectoryWindow(stack)
    loading_window = LoadingWindow(stack)
    results_window = ResultsWindow(stack)
    # Add windows to the stack
    stack.addWidget(main_window)  # Index 0
    stack.addWidget(waypoint_window)  # Index 1
    stack.addWidget(trajectory_window) # Index 2
    stack.addWidget(loading_window)  # Index 3
    stack.addWidget(results_window)  # Index 4
    stack.setWindowTitle("Robot Trajectory Planner")

    stack.setCurrentIndex(0)  # Start on MainWindow
    stack.resize(1200, 800)
    stack.show()

    sys.exit(app.exec())
