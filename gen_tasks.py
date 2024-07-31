import random
import string
import datetime
import os
import itertools

def generate_process_name():
    for length in itertools.count(1):
        for name in [''.join(chars) for chars in itertools.product(string.ascii_uppercase, repeat=length)]:
            yield name

def generate_tasks(num_tasks):
    process_names = generate_process_name()
    tasks = []
    current_time = 0
    
    for _ in range(num_tasks):
        name = next(process_names)
        arrival_time = current_time + random.randint(1, 10)
        current_time = arrival_time
        processing_time = random.randint(1, 30)
        deadline = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        priority = random.randint(1, 30)
        
        tasks.append(f"{name},{arrival_time},{processing_time},{deadline},{priority}")
    
    return tasks

def save_tasks(tasks):
    now = datetime.datetime.now()
    filename = now.strftime("%Y_%m_%d_%H_%M_%S.csv")
    os.makedirs("test", exist_ok=True)
    with open(f"test/{filename}", "w") as f:
        for task in tasks:
            f.write(f"{task}\n")
    return filename

def main(num_tasks):
    tasks = generate_tasks(num_tasks)
    filename = save_tasks(tasks)
    print(f"Generated {num_tasks} tasks and saved to {filename}")
    return filename

if __name__ == "__main__":
    num_tasks = int(input("Enter the number of tasks to generate: "))
    main(num_tasks)