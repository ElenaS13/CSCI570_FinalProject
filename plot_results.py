import matplotlib.pyplot as plt
import csv
import sys
import os

INPUT_CSV = "summary_results.csv"
TIME_PLOT_FILE = "CPU_Time_vs_Problem_Size.png"
MEMORY_PLOT_FILE = "Memory_vs_Problem_Size.png"

def read_data(csv_file):
    sizes = []
    basic_times = []
    eff_times = []
    basic_mems = []
    eff_mems = []
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sizes.append(float(row["ProblemSize(M+N)"]))
                basic_times.append(float(row["Basic_Time(ms)"]))
                eff_times.append(float(row["Efficient_Time(ms)"]))
                basic_mems.append(float(row["Basic_Memory(KB)"]))
                eff_mems.append(float(row["Efficient_Memory(KB)"]))
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}. Did you run 'run_experiments.py' first?")
        sys.exit(1)
        
    return sizes, basic_times, eff_times, basic_mems, eff_mems

def plot_graph(x, y1, y2, title, ylabel, filename, y1_label, y2_label):
    plt.figure(figsize=(10, 6))
    
    # Plotting the lines
    plt.plot(x, y1, label=y1_label, marker='o', linestyle='-', color='red')
    plt.plot(x, y2, label=y2_label, marker='x', linestyle='--', color='blue')
    
    # Labels and Title
    plt.title(title)
    plt.xlabel('Problem Size (M + N)')
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    
    # Save file
    plt.savefig(filename)
    print(f"Generated plot: {filename}")
    plt.close() 

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"File {INPUT_CSV} not found! Run the experiment script first.")
        return

    print("Reading data...")
    sizes, b_times, e_times, b_mems, e_mems = read_data(INPUT_CSV)
    
    # 1. Plot CPU Time vs Problem Size
    plot_graph(
        sizes, b_times, e_times, 
        "CPU Time vs Problem Size", 
        "Time (milliseconds)", 
        TIME_PLOT_FILE,
        "Basic Algorithm",
        "Efficient Algorithm"
    )
    
    # 2. Plot Memory vs Problem Size
    plot_graph(
        sizes, b_mems, e_mems, 
        "Memory Usage vs Problem Size", 
        "Memory (KB)", 
        MEMORY_PLOT_FILE,
        "Basic Algorithm",
        "Efficient Algorithm"
    )

    print("\nSuccess! Two image files have been created.")

if __name__ == "__main__":
    main()