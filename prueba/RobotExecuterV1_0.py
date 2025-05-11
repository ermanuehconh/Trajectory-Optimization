import socket
import numpy as np
import time
import rtde.rtde as rtde
import csv
import os
import threading

def execute_trajectory_with_logging(trajectory_deg, a, v, file_prefix="log", robot_ip="192.168.0.102"):
    RTDE_PORT = 30004
    URPORT = 30002
    filename = f"{file_prefix}_{int(time.time())}.csv"
    filepath = os.path.join(os.getcwd(), filename)
    csv_file = open(filepath, mode="w", newline="")
    csv_writer = csv.writer(csv_file)
    header = ["timestamp", "voltage", "current"]
    csv_writer.writerow(header)

    con = rtde.RTDE(robot_ip, RTDE_PORT)
    con.connect()
    con.get_controller_version()
    con.send_output_setup(["actual_q", "actual_robot_voltage", "actual_robot_current"], frequency=50)
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
                row = [round(elapsed, 3), state.actual_robot_voltage, state.actual_robot_current]
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
