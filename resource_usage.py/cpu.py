import psutil
import time

def get_processes_info(parent_pid):
    try:
        parent = psutil.Process(parent_pid)
        processes = [parent] + parent.children(recursive=True)
    except psutil.NoSuchProcess:
        return None

    # Initialize CPU usage measurement for each process
    for proc in processes:
        try:
            with proc.oneshot():
                if psutil.pid_exists(proc.pid):
                    proc.cpu_percent(interval=None)  # Initialize without blocking
        except psutil.NoSuchProcess:
            continue

    # Wait a short period to allow CPU activity
    time.sleep(1)

    total_cores = psutil.cpu_count()

    # Measure CPU usage after the wait
    process_info = []
    for proc in processes:
        try:
            with proc.oneshot():
                pid = proc.pid
                if not psutil.pid_exists(pid):
                    continue
                cpu_percent = proc.cpu_percent(interval=None) / total_cores
                memory_gb = proc.memory_info().rss / 1024 ** 3  # Convert memory usage from bytes to GB
                process_info.append((pid, cpu_percent, memory_gb))
        except psutil.NoSuchProcess:
            continue

    return process_info

def get_cpu_temperature():
    temps = psutil.sensors_temperatures()
    if 'coretemp' in temps:
        # 'coretemp' is commonly used on Linux for CPU temperature
        core_temps = temps['coretemp']
        return max(temp.current for temp in core_temps)
    elif temps:
        # Fallback to any available temperature sensor
        return max(temp.current for sensor in temps.values() for temp in sensor)
    return None

def display_process_info(process_info):
    cpu_temp = get_cpu_temperature()
    cpu_temp_str = f"{cpu_temp:.1f}°C" if cpu_temp is not None else "N/A"

    print(f"CPU Temperature: {cpu_temp_str}")
    print("{:<8} {:<8} {:<8}".format("PID", "%CPU", "MEM(GB)"))
    print("{:<8} {:<8} {:<8}".format("---", "----", "-------"))
    for info in process_info:
        print("{:<8} {:<8.2f} {:<8.2f}".format(*info))
    print("---------------------------")