import gen_tasks
import scheduler
import show
import os
import datetime

def load_tasks(filename):
    tasks = []
    with open(f"test/{filename}", "r") as f:
        for line in f:
            name, arrival_time, processing_time, deadline, priority = line.strip().split(',')
            tasks.append(scheduler.Task(name, int(arrival_time), int(processing_time), deadline, int(priority)))
    return tasks

def save_results(algorithm_name, tasks, avg_turnaround_time):
    os.makedirs("log", exist_ok=True)
    now = datetime.datetime.now()
    filename = f"log/{now.strftime('%Y_%m_%d_%H_%M_%S')}_{algorithm_name}.txt"
    
    with open(filename, "w") as f:
        f.write(f"アルゴリズム: {algorithm_name}\n")
        f.write(f"タスク数: {len(tasks)}\n")
        f.write(f"総完了時間: {max(task.finish_time for task in tasks)}\n")
        f.write(f"平均ターンアラウンド時間: {avg_turnaround_time:.2f}\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'名前':<10}{'到着時間':<10}{'処理時間':<15}{'締切時間':<15}{'優先度':<10}{'開始時間':<10}{'終了時間':<10}\n")
        f.write("-" * 80 + "\n")
        
        for task in tasks:
            f.write(f"{task.name:<10}{task.arrival_time:<10}{task.processing_time:<15}{task.deadline.strftime('%H:%M'):<15}{task.priority:<10}{task.start_time:<10}{task.finish_time:<10}\n")
    
    print(f"結果が {filename} に保存されました")
    return filename

def execute_all_algorithms(tasks):
    results = []
    algorithms = [
        ("FCFS", scheduler.fcfs, []),
        ("SPT", scheduler.spt, []),
        ("Deadline Scheduling", scheduler.deadline_scheduling, []),
        ("Priority Scheduling", scheduler.priority, []),
        ("Round Robin", scheduler.round_robin, [int(input("ラウンドロビンのタイムスライスを入力してください: "))])
    ]

    for name, func, args in algorithms:
        scheduled_tasks = func(tasks.copy(), *args)
        avg_turnaround_time = scheduler.calculate_average_turnaround_time(scheduled_tasks)
        result_file = save_results(name, scheduled_tasks, avg_turnaround_time)
        results.append((name, result_file, avg_turnaround_time))

    # サマリーファイルに保存
    summary_file = "log/summary.txt"
    with open(summary_file, "w") as f:
        f.write("すべてのアルゴリズムのサマリー\n")
        f.write("-" * 80 + "\n")
        for name, result_file, avg_turnaround_time in results:
            f.write(f"アルゴリズム: {name}\n")
            f.write(f"結果ファイル: {result_file}\n")
            f.write(f"平均ターンアラウンド時間: {avg_turnaround_time:.2f}\n")
            f.write("-" * 80 + "\n")
    
    print(f"結果のサマリーが {summary_file} に保存されました")

def main():
    while True:
        try:
            num_tasks = int(input("タスクの数を入力してください（0で終了）: "))
            if num_tasks == 0:
                break
            if num_tasks < 0:
                raise ValueError("タスク数は正の数でなければなりません")
        except ValueError as e:
            print(f"入力エラー: {e}")
            continue

        filename = gen_tasks.main(num_tasks)
        tasks = load_tasks(filename)

        while True:
            print("\nスケジューリングアルゴリズムを選んでください:")
            print("1. 先着順（FCFS）")
            print("2. 最短処理時間優先（SPT）")
            print("3. 締切優先スケジューリング")
            print("4. 優先度スケジューリング")
            print("5. ラウンドロビン")
            print("6. すべてのアルゴリズムを実行")
            print("7. 新しいタスクを生成")
            print("8. 終了")

            choice = input("選択してください（1-8）: ")

            if choice == '1':
                scheduled_tasks = show.show_scheduling(tasks, "FCFS", scheduler.fcfs)
                algorithm_name = "FCFS"
            elif choice == '2':
                scheduled_tasks = show.show_scheduling(tasks, "SPT", scheduler.spt)
                algorithm_name = "SPT"
            elif choice == '3':
                scheduled_tasks = show.show_scheduling(tasks, "締切優先スケジューリング", scheduler.deadline_scheduling)
                algorithm_name = "Deadline_Scheduling"
            elif choice == '4':
                scheduled_tasks = show.show_scheduling(tasks, "優先度スケジューリング", scheduler.priority)
                algorithm_name = "Priority_Scheduling"
            elif choice == '5':
                time_slice = int(input("ラウンドロビンのタイムスライスを入力してください: "))
                scheduled_tasks = show.show_scheduling(tasks, "ラウンドロビン", scheduler.round_robin, time_slice)
                algorithm_name = f"Round_Robin_TS{time_slice}"
            elif choice == '6':
                execute_all_algorithms(tasks)
                continue
            elif choice == '7':
                break
            elif choice == '8':
                return
            else:
                print("無効な選択です。もう一度お試しください。")
                continue

            avg_turnaround_time = scheduler.calculate_average_turnaround_time(scheduled_tasks)
            print(f"\n最終的な平均ターンアラウンド時間: {avg_turnaround_time:.2f}")
            save_results(algorithm_name, scheduled_tasks, avg_turnaround_time)

if __name__ == "__main__":
    main()
