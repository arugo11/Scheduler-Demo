import datetime

class Task:
    def __init__(self, name, arrival_time, processing_time, deadline, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.processing_time = processing_time
        self.deadline = datetime.datetime.strptime(deadline, "%H:%M")
        self.priority = priority
        self.remaining_time = processing_time
        self.start_time = None
        self.finish_time = None

def fcfs(tasks):
    current_time = 0
    for task in tasks:
        if current_time < task.arrival_time:
            current_time = task.arrival_time
        task.start_time = current_time
        current_time += task.processing_time
        task.finish_time = current_time
    return tasks

def spt(tasks):
    current_time = 0
    sorted_tasks = sorted(tasks, key=lambda x: x.processing_time)
    for task in sorted_tasks:
        if current_time < task.arrival_time:
            current_time = task.arrival_time
        task.start_time = current_time
        current_time += task.processing_time
        task.finish_time = current_time
    return sorted_tasks

def deadline_scheduling(tasks):
    current_time = 0
    sorted_tasks = sorted(tasks, key=lambda x: x.deadline)
    for task in sorted_tasks:
        if current_time < task.arrival_time:
            current_time = task.arrival_time
        task.start_time = current_time
        current_time += task.processing_time
        task.finish_time = current_time
    return sorted_tasks

def priority(tasks):
    current_time = 0
    sorted_tasks = sorted(tasks, key=lambda x: x.priority, reverse=True)
    for task in sorted_tasks:
        if current_time < task.arrival_time:
            current_time = task.arrival_time
        task.start_time = current_time
        current_time += task.processing_time
        task.finish_time = current_time
    return sorted_tasks

def round_robin(tasks, time_slice):
    current_time = 0
    queue = []
    completed_tasks = []
    while tasks or queue:
        while tasks and tasks[0].arrival_time <= current_time:
            queue.append(tasks.pop(0))
        if not queue:
            current_time = tasks[0].arrival_time
            continue
        task = queue.pop(0)
        if task.start_time is None:
            task.start_time = current_time
        if task.remaining_time <= time_slice:
            current_time += task.remaining_time
            task.finish_time = current_time
            task.remaining_time = 0
            completed_tasks.append(task)
        else:
            current_time += time_slice
            task.remaining_time -= time_slice
            while tasks and tasks[0].arrival_time <= current_time:
                queue.append(tasks.pop(0))
            queue.append(task)
    return completed_tasks

def calculate_average_turnaround_time(tasks):
    total_turnaround_time = sum(task.finish_time - task.arrival_time for task in tasks if task.finish_time is not None)
    completed_tasks = sum(1 for task in tasks if task.finish_time is not None)
    if completed_tasks == 0:
        return 0
    return total_turnaround_time / completed_tasks

# Multilevel Queues and Multilevel Feedback Queues are more complex and would require additional implementation