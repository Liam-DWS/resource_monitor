#!/usr/bin/env python3

import psutil
import time
import cpu


def get_user_choice():
    print("Select the hardware to monitor:")
    print("1. NVIDIA GPU #ignore for now")
    print("2. AMD GPU #ignore for now")
    print("3. CPU Only")
    choice = input("Enter your choice (1, 2, or 3): ")
    return choice

def display_initial_info(parent_pid):
    total_cores = psutil.cpu_count()
    total_memory_gb = psutil.virtual_memory().total / 1024 ** 3
    process_count = len(cpu.get_processes_info(parent_pid)) if psutil.pid_exists(parent_pid) else 0

    print(f"Number of Processes: {process_count}")
    print(f"CPU Cores: {total_cores}")
    print(f"Total Memory: {total_memory_gb:.2f} GB")
    print()

def main():
    user_choice = get_user_choice()
    parent_pid = int(input("Enter the PID of the process to monitor: "))

    if not psutil.pid_exists(parent_pid):
        print(f"Process with PID {parent_pid} not found.")
        return

    print(f"Monitoring resources for PID and its child processes: {parent_pid}")
    display_initial_info(parent_pid)  # Display system info before entering the loop

    print("Press Ctrl+C to exit.")

    try:
        while True:
            process_info = cpu.get_processes_info(parent_pid)
            if process_info is None:
                print(f"No information found for PID {parent_pid}. It might have terminated.")
                break

            # Update and display the number of processes
            print(f"Number of Processes: {len(process_info)}")

            cpu.display_process_info(process_info)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
