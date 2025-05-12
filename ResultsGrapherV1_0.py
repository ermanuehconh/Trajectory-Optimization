import pandas as pd
import matplotlib.pyplot as plt
import ast
import os

def process_and_plot_energy_data(csv_filename, output_png=None):
    # === 1. Load CSV ===
    data = pd.read_csv(csv_filename)
    print("Columns in CSV:", data.columns.tolist())

    # === 2. Check required columns ===
    required_columns = {'timestamp', 'voltage', 'joint_current', 'actual_qd'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"CSV must contain columns: {required_columns}")

    # === 3. Parse stringified lists into real Python lists ===
    data['actual_qd'] = data['actual_qd'].apply(ast.literal_eval)
    data['joint_current'] = data['joint_current'].apply(ast.literal_eval)

    # === 4. Calculate Instantaneous Power ===
    data['current'] = data['joint_current'].apply(lambda x: sum(x) / len(x))  # average current from joints
    data['power'] = data['voltage'] * data['current']  # W

    # === 5. Time and Energy Calculations ===
    data['delta_time'] = data['timestamp'].diff().fillna(0)
    data['energy_increment'] = data['power'] * data['delta_time']  # J
    data['cumulative_energy'] = data['energy_increment'].cumsum()
    total_energy = data['energy_increment'].sum()
    print(f"\n Total Energy Consumed: {total_energy:.2f} Joules")

    # === 6. Separate joint data for plotting ===
    joint_speeds = list(zip(*data['actual_qd']))
    joint_currents = list(zip(*data['joint_current']))

    # === 7. Plot ===
    fig, axs = plt.subplots(
        7, 1,
        figsize=(14, 16),
        sharex=True,
        gridspec_kw={'height_ratios': [1,1,1,1,1,1,0.3], 'hspace': 0.6}
    )
    fig.subplots_adjust(left=0.2, right=0.7, top=0.95, bottom=0.05)
    # Voltage
    axs[0].plot(data['timestamp'], data['voltage'], label='Voltage (V)', color='blue')
    axs[0].set_ylabel('Voltage (V)')
    axs[0].set_title('Voltage vs Time')
    axs[0].legend(loc='upper left',
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0.,
        fontsize='x-small',
        ncol=1)
    axs[0].grid(True)

    # Current
    axs[1].plot(data['timestamp'], data['current'], label='Avg Joint Current (A)', color='orange')
    axs[1].set_ylabel('Current (A)')
    axs[1].set_title('Average Current vs Time')
    axs[1].legend(loc='upper left',
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0.,
        fontsize='x-small',
        ncol=1)
    axs[1].grid(True)

    # Power
    axs[2].plot(data['timestamp'], data['power'], label='Power (W)', color='green')
    axs[2].set_ylabel('Power (W)')
    axs[2].set_title('Power vs Time')
    axs[2].legend(loc='upper left',
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0.,
        fontsize='x-small',
        ncol=1)
    axs[2].grid(True)

    # Energy
    axs[3].plot(data['timestamp'], data['cumulative_energy'], label='Cumulative Energy (J)', color='red', marker='o', markersize=2)
    axs[3].set_ylabel('Energy (J)')
    axs[3].set_title('Cumulative Energy vs Time')
    axs[3].legend(loc='upper left',
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0.,
        fontsize='x-small',
        ncol=1)
    axs[3].grid(True)

    # Joint Speeds
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']
    for i in range(6):
        axs[4].plot(data['timestamp'], joint_speeds[i], label=f'Joint {i+1} Speed', color=colors[i])
    axs[4].set_ylabel('Speed (rad/s)')
    axs[4].set_title('Joint Speeds vs Time')
    axs[4].legend(loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0.,fontsize='x-small', ncol=1)
    axs[4].grid(True)

    # Joint Currents
    for i in range(6):
        axs[5].plot(data['timestamp'], joint_currents[i], label=f'Joint {i+1} Current', linestyle='--')
    axs[5].set_ylabel('Joint Currents (A)')
    axs[5].set_title('Joint Motor Currents vs Time')
    axs[5].legend(loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0.,fontsize='x-small', ncol=1)
    axs[5].grid(True)

    # Shared X label
    axs[6].axis('off')
    axs[6].set_xlabel('Time (s)')

    if output_png is None:
        output_png = os.path.splitext(csv_filename)[0] + "_plot.png"
    plt.savefig(output_png)
    plt.close()

    return output_png

if __name__ == "__main__":
    # Example usage
    #ask user for the filename
    csv_filename = input("Enter the CSV filename (with .csv extension): ") 
    process_and_plot_energy_data(csv_filename)