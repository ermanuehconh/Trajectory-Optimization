"""
This script implements a PySide6-based GUI application for a robot trajectory planner. 
It consists of multiple windows managed by a QStackedWidget, allowing users to define waypoints, 
optimize trajectories, and execute them on a robot.
Classes:
--------
- MainWindow: 
    The main window of the application, providing navigation to other windows.
- WaypointWindow: 
    Allows users to define and manage waypoints for the robot trajectory. 
    Includes functionality to add, delete, and optimize waypoints.
- TrajectoryWindow: 
    Displays the optimized trajectory and allows users to adjust acceleration and velocity 
    parameters before sending the trajectory to the robot.
- LoadingWindow: 
    A placeholder window for loading or processing states.
- ResultsWindow: 
    Displays the results of the trajectory execution, including any logged data.
Functions:
----------
- MainWindow.button1_clicked(): 
    Navigates to the WaypointWindow.
- MainWindow.button2_clicked(): 
    Placeholder for additional functionality.
- WaypointWindow.go_back(): 
    Navigates back to the MainWindow.
- WaypointWindow.go_foward(): 
    Optimizes the waypoints and navigates to the TrajectoryWindow.
- WaypointWindow.add_waypoint(): 
    Adds a new waypoint to the table.
- WaypointWindow.delete_selected_row(): 
    Deletes the currently selected waypoint from the table.
- TrajectoryWindow.go_back(): 
    Navigates back to the WaypointWindow.
- TrajectoryWindow.show_trajectory(trajectory_deg): 
    Displays the optimized trajectory in a table.
- TrajectoryWindow.change_window(): 
    Navigates to the LoadingWindow and initiates trajectory execution.
- TrajectoryWindow.send_to_robot(): 
    Sends the trajectory to the robot for execution, with optional logging.
- TrajectoryWindow.update_av_labels(): 
    Updates the labels displaying acceleration and velocity values.
- ResultsWindow.go_back(): 
    Navigates back to the TrajectoryWindow.
Main Execution:
---------------
- Initializes the QApplication and QStackedWidget.
- Creates instances of all windows and adds them to the stack.
- Sets the initial window to MainWindow and starts the application.
Styling:
--------
- Custom stylesheet applied to enhance the appearance of the application.
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from ui.ui_form import Ui_Form
from ui.ui_waypoints import Ui_Form as Ui_Waypoints
from ui.ui_trajectory import Ui_Form as Ui_Trajectory
from ui.ui_loading import Ui_Form as Ui_Loading
from ui.ui_results import Ui_Form as Ui_Results
from ui.ui_help import Ui_Form as Ui_Help 
import logic.TrajectoryPlannerV1_0 as tp
import logic.RobotExecuterV1_3 as re
import logic.ResultsGrapherV1_0 as rg
import numpy as np

class MainWindow(QWidget):
    def __init__(self,stack):
        super().__init__()
        self.stack = stack

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.startButton.clicked.connect(self.button1_clicked)
        self.ui.helpButton.clicked.connect(self.button2_clicked)

    def button1_clicked(self):
        self.stack.setCurrentIndex(1)

    def button2_clicked(self):
        self.stack.setCurrentIndex(5)

class WaypointWindow(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.ui = Ui_Waypoints()
        self.ui.setupUi(self)

        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.optimizeButton.clicked.connect(self.send_data_foward)
        self.ui.addButton.clicked.connect(self.add_waypoint)
        self.ui.deleteButton.clicked.connect(self.delete_selected_row)
        self.ui.waypointsTable.horizontalHeader().setStretchLastSection(True)
        self.ui.waypointsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.waypointsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.waypointsTable.setSelectionMode(QAbstractItemView.SingleSelection)


    def go_back(self):
        self.stack.setCurrentIndex(0)

    def send_data_foward(self):
        """
        Optimizes the waypoints and sends the optimized trajectory to the TrajectoryWindow.
        """
        waypoints = []
        for row in range(self.ui.waypointsTable.rowCount()):
            wp = []
            for col in range(6):
                item = self.ui.waypointsTable.item(row, col)
                wp.append(float(item.text()) if item else 0.0)
            waypoints.append(wp)

        if len(waypoints) < 2:
            print("Add at least two waypoints.")
            QMessageBox.warning(self, "Warning", "Add at least two waypoints.")
            return

        try:
            optimized = tp.optimize_from_waypoints_deg(waypoints)
            self.stack.widget(2).show_trajectory(optimized)  # Send to TrajectoryWindow
            self.stack.setCurrentIndex(2)
        except Exception as e:
            print("Optimization error:", e)

    def add_waypoint(self):
        """
        Adds a new waypoint to the table with the values from the input fields.
        If the input fields are empty, it defaults to "0".
        """
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

    def show_popup(self,title, message):
        """
        Displays a message box with the given title and message.
        Parameters:
            title (str): The title of the message box.
            message (str): The message to display.
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

class TrajectoryWindow(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.ui = Ui_Trajectory()
        self.ui.setupUi(self)

        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.sendButton.clicked.connect(self.load_robot)
        self.ui.acelerationSlider.valueChanged.connect(self.update_av_labels)
        self.ui.velocitySlider.valueChanged.connect(self.update_av_labels)
        self.ui.homeButton.clicked.connect(self.move_home)
        self.ui.firstpointButton.clicked.connect(self.move_first_position)
        self.update_av_labels()

    def go_back(self):
        self.stack.setCurrentIndex(1)

    def show_trajectory(self, trajectory_deg):
        """
        Displays the optimized trajectory in a table format.
        Parameters:
            trajectory_deg (np.ndarray): 2D array of joint angles in degrees.
        """
        rows = trajectory_deg.shape[1]  # time steps
        cols = trajectory_deg.shape[0]  # joints (should be 6)

        self.ui.trajectoryTable.setRowCount(rows)
        self.ui.trajectoryTable.setColumnCount(cols)
        self.ui.trajectoryTable.setHorizontalHeaderLabels([f"J{i+1}" for i in range(cols)])
        self.ui.trajectoryTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
    
    def load_robot(self):
        """
        Changes the current window to the LoadingWindow and sends the trajectory to the robot.
        """
        self.stack.setCurrentIndex(3)
        QTimer.singleShot(100, self.send_to_robot)

    def move_home(self):
        """
        Moves the robot to the home position.
        """
        if re.check_connection() == False:
            self.show_popup("Connection Error", "No connection to the robot.")
            return
        actual_q = re.get_actual_q("deg")
        q_home = [-90, -90, -90, -90, 90, 0]
        if actual_q != q_home:
            trajectory_deg = np.zeros((6, 2))
            trajectory_deg[:, 0] = actual_q
            trajectory_deg[:, 1] = q_home
            a = self.ui.acelerationSlider.value()/100
            v = self.ui.velocitySlider.value()/100
            re.execute_trajectory_without_logging(trajectory_deg, a, v)
    
    def move_first_position(self):
        """
        Moves the robot to the first position defined in the trajectory table.
        """
        if re.check_connection() == False:
            self.show_popup("Connection Error", "No connection to the robot.")
            return
        actual_q = re.get_actual_q("deg")
        q_obj = [float(self.ui.trajectoryTable.item(0, col).text()) if self.ui.trajectoryTable.item(0, col) else 0.0 
             for col in range(self.ui.trajectoryTable.columnCount())]
        if actual_q != q_obj:
            trajectory_deg = np.zeros((6, 2))
            trajectory_deg[:, 0] = actual_q
            trajectory_deg[:, 1] = q_obj
            a = self.ui.acelerationSlider.value()/100
            v = self.ui.velocitySlider.value()/100
            re.execute_trajectory_without_logging(trajectory_deg, a, v)
    
    def send_to_robot(self):
        """
        Sends the trajectory to the robot for execution.
        """
        if re.check_connection() == False:
            self.show_popup("Connection Error", "No connection to the robot.")
            return
        try:
            rows = self.ui.trajectoryTable.rowCount()
            cols = self.ui.trajectoryTable.columnCount()
            trajectory_deg = np.zeros((cols, rows))

            for i in range(rows):
                for j in range(cols):
                    item = self.ui.trajectoryTable.item(i, j)
                    angle = float(item.text()) if item else 0.0
                    trajectory_deg[j, i] = angle

            a = self.ui.acelerationSlider.value()/100
            v = self.ui.velocitySlider.value()/100
            if self.ui.loggingCheck.isChecked():
                filename = re.execute_trajectory_with_logging(trajectory_deg, a, v, file_prefix="trajectory")
                print(f"Trajectory logged in {filename}")
                self.stack.widget(4).ui.label.setText(f"Trajectory logged in {filename}")
                self.stack.widget(4).show_image(filename)
            else:
                re.execute_trajectory_without_logging(trajectory_deg, a, v)
            self.stack.setCurrentIndex(4)
        except Exception as e:
            print("Error during execution:", e)

    def update_av_labels(self):
        a = self.ui.acelerationSlider.value()
        v = self.ui.velocitySlider.value()
        self.ui.acelerationValue.setText(f"a = {a:.2f}%")
        self.ui.velocityValue.setText(f"v = {v:.2f}%")
    
    def show_popup(self,title, message):
        """
        Displays a message box with the given title and message.
        Parameters:
            title (str): The title of the message box.
            message (str): The message to display.
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        result = msg.exec()

        if result == QMessageBox.Ok:
            self.stack.setCurrentIndex(2)
  

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

    def show_image(self, filename):
        graphimage = rg.process_and_plot_energy_data(filename)
        pixmap = QPixmap(graphimage)
        self.ui.imageLabel.setPixmap(pixmap)
        self.ui.imageLabel.setScaledContents(True)

class HelpWindow(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.ui = Ui_Help()
        self.ui.setupUi(self)

        self.ui.backButton.clicked.connect(self.go_back)
        self.load_manual("manual.txt")

    def go_back(self):
        self.stack.setCurrentIndex(0)
    
    def load_manual(self, filename):
        """
        Loads the manual from a text file and displays it in the text edit area.
        Parameters:
            filename (str): The path to the manual file.
        """
        try:
            with open(filename, "r",encoding="utf-8") as file:
                content = file.read()
                self.ui.textEdit.setPlainText(content)
        except FileNotFoundError:
            self.ui.textEdit.setPlainText("Manual file not found.")

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
    help_window = HelpWindow(stack)
    # Add windows to the stack
    stack.addWidget(main_window)  # Index 0
    stack.addWidget(waypoint_window)  # Index 1
    stack.addWidget(trajectory_window) # Index 2
    stack.addWidget(loading_window)  # Index 3
    stack.addWidget(results_window)  # Index 4
    stack.addWidget(help_window)  # Index 5

    stack.setWindowTitle("Robot Trajectory Planner")

    stack.setCurrentIndex(0)  # Start on MainWindow
    stack.resize(1200, 800)
    stack.show()

    sys.exit(app.exec())
