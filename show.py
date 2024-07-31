import time
import os
from scheduler import calculate_average_turnaround_time
import sys
import select

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_q_pressed():
    if os.name == 'nt':  
        import msvcrt
        return msvcrt.kbhit() and msvcrt.getch().decode().lower() == 'q'
    else:  
        i, o, e = select.select([sys.stdin], [], [], 0.0001)
        for s in i:
            if s == sys.stdin:
                input = sys.stdin.readline()
                return input.strip().lower() == 'q'
    return False

def display_tasks(tasks, current_time, algorithm_name):
    clear_screen()
    print(f"Current Time: {current_time}")
    print(f"Algorithm: {algorithm_name}")
    print("-" * 80)
    print(f"{'Name':<10}{'Arrival':<10}{'Processing':<15}{'Deadline':<15}{'Priority':<10}{'Status':<10}")
    print("-" * 80)
    
    completed_tasks = [task for task in tasks if task.finish_time is not None]
    running_tasks = [task for task in tasks if task.start_time is not None and task.finish_time is None]
    waiting_tasks = [task for task in tasks if task.start_time is None]
    
    display_tasks = completed_tasks[-9:] + running_tasks[:1]
    
    for task in display_tasks:
        status = "Waiting"
        if task.finish_time is not None:
            status = "Completed"
        elif task.start_time is not None and task.start_time <= current_time:
            status = "Running"
        
        print(f"{task.name:<10}{task.arrival_time:<10}{task.processing_time:<15}{task.deadline.strftime('%H:%M'):<15}{task.priority:<10}{status:<10}")
    
    print("-" * 80)
    total_tasks = len(tasks)
    completed_count = len(completed_tasks)
    print(f"Progress: {completed_count} / {total_tasks}")
    avg_turnaround_time = calculate_average_turnaround_time(tasks)
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    print("-" * 80)
    print("Press 'q' to stop the simulation")
    time.sleep(0.1)  # Reduced delay for responsiveness

def show_scheduling(tasks, algorithm_name, scheduling_function, *args):
    current_time = 0
    max_time = max(task.arrival_time + task.processing_time for task in tasks)
    
    while current_time <= max_time:
        scheduled_tasks = scheduling_function(tasks.copy(), *args)
        display_tasks(scheduled_tasks, current_time, algorithm_name)
        if is_q_pressed():
            print("Simulation stopped by user")
            break
        current_time += 1
        if all(task.finish_time is not None for task in scheduled_tasks):
            break

    return scheduled_tasks