# task_manager.py
# TechStart — Student Task Manager (Prototype)
# Run: python task_manager.py

tasks = []

def add_task(name, priority="Medium"):
    task = {
        "id": len(tasks) + 1,
        "name": name,
        "priority": priority,
        "status": "Pending"
    }
    tasks.append(task)
    print(f"Added: [{task['id']}] {name} ({priority})")

def view_tasks():
    if not tasks:
        print("No tasks yet.")
        return
    print("\n--- Task List ---")
    for t in tasks:
        print(f"[{t['id']}] {t['name']} | {t['priority']} | {t['status']}")
    print()

def complete_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Done"
            print(f"Marked as done: {t['name']}")
            return
    print("Task not found.")

def print_task_summary():
    """
    Groups tasks by status and prints the count for each status in bullet points.
    """
    summary = {}
    for task in tasks:
        status = task["status"]
        summary[status] = summary.get(status, 0) + 1
    
    for status, count in summary.items():
        print(f"- **{status}**: {count}")

def main():
    add_task("Design login page", "High")
    add_task("Write unit tests", "Medium")
    add_task("Update documentation", "Low")

    view_tasks()
    complete_task(1)
    view_tasks()
    print_task_summary()

if __name__ == "__main__":
    main()
