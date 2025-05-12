"""
Robot Trajectory Execution with Logging and Without Logging
This script provides two main functions to execute a trajectory on a robot:
1. `execute_trajectory_with_logging`: Executes a trajectory while logging robot data to a CSV file.
2. `execute_trajectory_without_logging`: Executes a trajectory without logging.
Modules Imported:
- `socket`: For communication with the robot controller.
- `numpy`: For numerical operations, such as converting degrees to radians.
- `time`: For time-related operations, such as timestamps and delays.
- `rtde.rtde`: For communication with the robot using the RTDE protocol.
- `csv`: For writing log data to a CSV file.
- `os`: For file path operations.
- `threading`: For running the logging process in a separate thread.
Functions:
1. `execute_trajectory_with_logging(trajectory_deg, a, v, file_prefix="log", robot_ip="192.168.0.102")`:
    - Executes a trajectory on the robot while logging data such as timestamp, voltage, and current to a CSV file.
    - Parameters:
        - `trajectory_deg`: A 2D numpy array where each column represents a time step of joint angles in degrees.
        - `a`: Acceleration parameter for the robot's movement.
        - `v`: Velocity parameter for the robot's movement.
        - `file_prefix`: Prefix for the log file name (default is "log").
        - `robot_ip`: IP address of the robot.
    - Returns:
        - The filename of the generated log file.
2. `execute_trajectory_without_logging(trajectory_deg, a, v, robot_ip="192.168.0.102")`:
    - Executes a trajectory on the robot without logging any data.
    - Parameters:
        - `trajectory_deg`: A 2D numpy array where each column represents a time step of joint angles in degrees.
        - `a`: Acceleration parameter for the robot's movement.
        - `v`: Velocity parameter for the robot's movement.
        - `robot_ip`: IP address of the robot (default is "192.168.0.102").
Helper Functions (Defined within the main functions):
- `send_movej(q_deg)`:
    - Sends a `movej` command to the robot to move to the specified joint angles.
    - Converts joint angles from degrees to radians before sending the command.
- `wait_until_reached(q_deg, tol=0.5)`:
    - Waits until the robot reaches the specified joint angles within a given tolerance (default is 0.5 degrees).
Threading:
- In `execute_trajectory_with_logging`, a separate thread is used for continuous logging of robot data while the trajectory is being executed.
Logging:
- Data logged includes:
    - Timestamp (elapsed time since logging started).
    - Robot voltage.
    - Robot current.
- Data is written to a CSV file with a dynamically generated filename based on the current timestamp.
Robot Communication:
- RTDE protocol is used for real-time data exchange with the robot.
- Socket communication is used to send movement commands (`movej`) to the robot.
Execution Flow:
1. Connect to the robot using RTDE.
2. Retrieve the initial position of the robot.
3. For each step in the trajectory:
    - Send a `movej` command to move the robot to the desired position.
    - Wait until the robot reaches the desired position.
4. If logging is enabled:
    - Start a separate thread for continuous logging.
    - Stop logging after the trajectory is completed.
5. Disconnect from the robot and close any open resources (e.g., CSV file).
"""
import socket
import numpy as np
import time
import rtde.rtde as rtde
import csv
import os
import threading

def execute_trajectory_with_logging(trajectory_deg, a, v, file_prefix="log", robot_ip="192.168.0.102"):
    """
    Execute a trajectory on the robot while logging data to a CSV file.
    Parameters:
        trajectory_deg (np.ndarray): 2D array of joint angles in degrees.
        a (float): Acceleration parameter for the robot's movement.
        v (float): Velocity parameter for the robot's movement.
        file_prefix (str): Prefix for the log file name.
        robot_ip (str): IP address of the robot.
    Returns:
        str: The filename of the generated log file.
    """
    RTDE_PORT = 30004
    URPORT = 30002
    filename = f"{file_prefix}_{int(time.time())}.csv"
    filepath = os.path.join(os.getcwd(), filename)
    csv_file = open(filepath, mode="w", newline="")
    csv_writer = csv.writer(csv_file)
    header = ['timestamp', 'voltage', 'joint_current', 'actual_qd']
    csv_writer.writerow(header)

    con = rtde.RTDE(robot_ip, RTDE_PORT)
    con.connect()
    con.get_controller_version()
    con.send_output_setup(["actual_q", "actual_robot_voltage", "actual_current","actual_qd"], frequency=50)
    con.send_start()

    state = con.receive()
    if state:
        print("Initial position (°):", np.round(np.rad2deg(state.actual_q), 2))

    logging_active = True
    log_thread_start = time.time()

    def continuous_logging():
        while logging_active:
            state = con.receive()
            if state:
                elapsed = time.time() - log_thread_start
                row = [round(elapsed, 3), state.actual_robot_voltage, state.actual_current, state.actual_qd]
                csv_writer.writerow(row)

    thread = threading.Thread(target=continuous_logging)
    thread.start()

    def send_movej(q_deg):
        q_rad = np.radians(q_deg)
        cmd = f"movej([{','.join(map(str, q_rad))}], a={a}, v={v})\n"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((robot_ip, URPORT))
        sock.send(cmd.encode("utf-8"))
        sock.close()

    def wait_until_reached(q_deg, tol=0.5):
        q_rad = np.radians(q_deg)
        while True:
            state = con.receive()
            if state:
                actual = np.array(state.actual_q)
                error = np.abs(actual - q_rad)
                if np.all(error < np.radians(tol)):
                    break
            time.sleep(0.1)

    for i, q_deg in enumerate(trajectory_deg.T):  # .T because each column is a time step
        print(f"Movement {i+1}")
        send_movej(q_deg)
        wait_until_reached(q_deg)
        print("Movement reached.")

    logging_active = False
    thread.join()
    con.send_pause()
    con.disconnect()
    csv_file.close()
    print(f"Logging completed: {filename}")
    return filename

def execute_trajectory_without_logging(trajectory_deg, a, v, robot_ip="192.168.0.102"):
    """
    Execute a trajectory on the robot without logging.
    Parameters:
        trajectory_deg (np.ndarray): 2D array of joint angles in degrees.
        a (float): Acceleration parameter for the robot's movement.
        v (float): Velocity parameter for the robot's movement.
        robot_ip (str): IP address of the robot.
    """
    RTDE_PORT = 30004
    URPORT = 30002

    con = rtde.RTDE(robot_ip, RTDE_PORT)
    con.connect()
    con.get_controller_version()
    con.send_output_setup(["actual_q"], frequency=50)
    con.send_start()

    state = con.receive()
    if state:
        print("Initial position (°):", np.round(np.rad2deg(state.actual_q), 2))

    def send_movej(q_deg):
        q_rad = np.radians(q_deg)
        cmd = f"movej([{','.join(map(str, q_rad))}], a={a}, v={v})\n"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((robot_ip, URPORT))
        sock.send(cmd.encode("utf-8"))
        sock.close()

    def wait_until_reached(q_deg, tol=0.5):
        q_rad = np.radians(q_deg)
        while True:
            state = con.receive()
            if state:
                actual = np.array(state.actual_q)
                error = np.abs(actual - q_rad)
                if np.all(error < np.radians(tol)):
                    break
            time.sleep(0.1)

    for i, q_deg in enumerate(trajectory_deg.T):
        print(f"Movement {i+1}")
        send_movej(q_deg)
        wait_until_reached(q_deg)
        print("Movement reached.")

    con.send_pause()
    con.disconnect()

def get_actual_q( units , robot_ip="192.168.0.102"):
    """
    Get the current position of the robot on the unit specified.
    Parameters:
        units (str): Units for the output ('deg' or 'rad').
        robot_ip (str): IP address of the robot.
    Returns:
        np.ndarray: Current joint angles in asked unit.
    """
    RTDE_PORT = 30004
    con = rtde.RTDE(robot_ip, RTDE_PORT)
    con.connect()
    con.get_controller_version()
    con.send_output_setup(["actual_q"], frequency=50)
    con.send_start()

    state = con.receive()
    if state:
        if units == "deg":
            current_position = np.rad2deg(state.actual_q)
            print("Current position (°):", np.round(current_position, 2))
        elif units == "rad":
            current_position = state.actual_q
            print("Current position (rad):", np.round(current_position, 2))
        else:
            raise ValueError("Invalid units. Use 'deg' or 'rad'.")
    con.send_pause()
    con.disconnect()
    return current_position

def check_connection(robot_ip="198.168.0.102"):
    """
    Check if the robot is reachable.
    Parameters:
        robot_ip (str): IP address of the robot.
    Returns:
        bool: True if the robot is reachable, False otherwise.
    """
    try:
        sock = socket.create_connection((robot_ip, 30002), timeout=5)
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

if __name__ == "__main__":    
    # Example usage
    trajectory_deg = np.array([[0, 0, 0, 0, 0, 0],
                                [30, 30, 30, 30, 30, 30],
                                [60, 60, 60, 60, 60, 60]])
    a = 1.0
    v = 1.0
    # Check connection
    if not check_connection():
        print("Robot is not reachable.")
        exit(1)
    execute_trajectory_with_logging(trajectory_deg, a, v)
    execute_trajectory_without_logging(trajectory_deg, a, v)
    get_actual_q("deg")
