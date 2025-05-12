"""
# Trajectory Planner for a 6DOF Robot Arm UR 10
This script implements a trajectory planner for a 6DOF robot arm using CasADi for optimization.
The trajectory planner generates a smooth joint trajectory that avoids obstacles and adheres to joint limits.
The script includes the following components:
1. **DH Parameters and TCP Offset**: Functions to compute the transformation matrices based on Denavit-Hartenberg parameters and the tool center point (TCP) offset.
2. **Forward Kinematics**: Function to compute the end-effector position based on joint angles using the transformation matrices.
3. **Optimization Setup**: Function to set up the optimization problem, including joint limits, waypoint constraints, and obstacle avoidance.
4. **Trajectory Optimization**: Function to solve the optimization problem and print the optimized joint trajectory.
5. **Main Function**: The main function to execute the trajectory optimization process.
"""
# ----------------------------------
# IMPORTS
# ----------------------------------
import casadi as ca
import numpy as np

# ----------------------------------
# DH + TCP offset
# ----------------------------------
def dh_transform(theta, d, a, alpha):
    """
    Compute the Denavit-Hartenberg transformation matrix.
    Parameters:
    - theta: Joint angle
    - d: Link offset
    - a: Link length
    - alpha: Link twist
    Returns:
    - T: Transformation matrix
    """
    return ca.vertcat(
        ca.horzcat(ca.cos(theta), -ca.sin(theta)*ca.cos(alpha), ca.sin(theta)*ca.sin(alpha), a*ca.cos(theta)),
        ca.horzcat(ca.sin(theta), ca.cos(theta)*ca.cos(alpha), -ca.cos(theta)*ca.sin(alpha), a*ca.sin(theta)),
        ca.horzcat(0, ca.sin(alpha), ca.cos(alpha), d),
        ca.horzcat(0, 0, 0, 1)
    )

def tcp_offset():
    """
    Compute the TCP offset transformation matrix.
    Returns:
    - T: Transformation matrix for TCP offset
    """
    return ca.vertcat(
        ca.horzcat(1, 0, 0, 0),
        ca.horzcat(0, 1, 0, 0),
        ca.horzcat(0, 0, 1, 0.200),  # TCP offset in Z direction
        ca.horzcat(0, 0, 0, 1)
    )

def forward_kinematics(q):
    """
    Compute the forward kinematics of the robot arm.
    Parameters:
    - q: Joint angles
    Returns:
    - T: End-effector position
    """
    d = [0.1273, 0, 0, 0.1639, 0.1157, 0.0922]
    a = [0, -0.612, -0.5723, 0, 0, 0]
    alpha = [ca.pi/2, 0, 0, ca.pi/2, -ca.pi/2, 0]
    T = ca.MX.eye(4)
    for i in range(6):
        T = ca.mtimes(T, dh_transform(q[i], d[i], a[i], alpha[i]))
    T = ca.mtimes(T, tcp_offset())
    return T[0:3, 3]

# ----------------------------------
# OPTIMIZATION
# ----------------------------------
def setup_optimization(waypoints, steps_between_waypoints, joint_limits, obstacles, d_min):
    """
    Set up the optimization problem.
    Parameters:
    - waypoints: List of waypoints (each waypoint is a list of joint angles).
    - steps_between_waypoints: Number of steps between waypoints.
    - joint_limits: Joint limits for each joint.
    - obstacles: List of obstacles (each obstacle is defined by its bounding box).
    - d_min: Minimum distance from obstacles.
    Returns:
    - opti: CasADi optimization problem.
    - q: Joint angles variable.
    - N: Number of time steps.
    """
    N = (len(waypoints) - 1) * steps_between_waypoints + 1
    opti = ca.Opti()
    q = opti.variable(6, N)

    # Minimize joint velocity squared
    dq = q[:, 1:] - q[:, :-1]
    opti.minimize(ca.sumsqr(dq))

    # Joint limits
    for j in range(6):
        opti.subject_to(opti.bounded(joint_limits[j][0], q[j, :], joint_limits[j][1]))

    # Waypoint constraints
    for i, wp in enumerate(waypoints):
        idx = i * steps_between_waypoints
        opti.subject_to(q[:, idx] == wp)

    # Obstacle avoidance
    for k in range(N):
        ee_pos = forward_kinematics(q[:, k])
        x, y, z = ee_pos[0], ee_pos[1], ee_pos[2]
        for (xmin, xmax, ymin, ymax, zmin, zmax) in obstacles:
            dx = ca.fmax(xmin - x, 0) + ca.fmax(x - xmax, 0)
            dy = ca.fmax(ymin - y, 0) + ca.fmax(y - ymax, 0)
            dz = ca.fmax(zmin - z, 0) + ca.fmax(z - zmax, 0)
            outside_dist_sq = dx**2 + dy**2 + dz**2
            opti.subject_to(outside_dist_sq >= d_min**2)

    return opti, q, N

# ----------------------------------
# SOLVE AND PRINT
# ----------------------------------
def solve_and_print_trajectory(opti, q, N):
    """
    Solve the optimization problem and print the optimized trajectory.
    Parameters:
    - opti: CasADi optimization problem.
    - q: Joint angles variable.
    - N: Number of time steps.
    Returns:
    - optimized_q_deg: Optimized joint trajectory in degrees.
    """
    opti.solver("ipopt") # other solvers can be used as well
    sol = opti.solve()
    optimized_q = sol.value(q)
    optimized_q_deg = np.rad2deg(optimized_q)
    print("\n Optimized Joint Trajectory (Degrees):")
    for i in range(N):
        print(f"Waypoint {i+1}: {optimized_q_deg[:, i].round(2)}")
    return optimized_q_deg

# ----------------------------------
# OPTIMIZATION FROM WAYPOINTS
# ----------------------------------

def optimize_from_waypoints_deg(waypoints_deg):
    """
    Optimize a trajectory from given waypoints in degrees.
    Parameters:
        waypoints_deg (list of list): List of waypoints in degrees.
    Returns:
        optimized_q_deg (np.ndarray): Optimized joint trajectory in degrees.
    """
    waypoints_rad = [np.radians(wp) for wp in waypoints_deg]
    steps_between_waypoints = 3
    joint_limits = [(-np.pi, np.pi)] * 6
    obstacles = [(-0.095, 0.115, -0.76, -0.70, 0.125, 0.325)]
    d_min = 0.05  # 5 cm

    opti, q, N = setup_optimization(waypoints_rad, steps_between_waypoints, joint_limits, obstacles, d_min)
    return solve_and_print_trajectory(opti, q, N)

# ----------------------------------
# MAIN
# ----------------------------------
if __name__ == "__main__":
    waypoints_deg = [
        [0, 0, 0, 0, 0, 0],
        [np.pi/4, np.pi/4, np.pi/4, np.pi/4, np.pi/4, np.pi/4],
        [np.pi/2, np.pi/2, np.pi/2, np.pi/2, np.pi/2, np.pi/2]
    ]
    optimize_from_waypoints_deg(waypoints_deg)
