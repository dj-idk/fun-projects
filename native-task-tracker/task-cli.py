import sys
import os
import json
from datetime import datetime

TASKS_FILE = "simple-tasks.json"


class Task:
    """Base Task Class"""

    def __init__(self, id, description, status, created_at, updated_at):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return f"Task {self.id}: {self.description}"


def load_tasks():
    """Load tasks from JSON file or
    return an empty structure if missing/corrupt."""
    if not os.path.exists(TASKS_FILE):
        return {"total_count": 0, "tasks": []}

    try:
        with open(TASKS_FILE, "r") as inputfile:
            return json.load(inputfile)
    except (json.JSONDecodeError, IOError):
        print("Warning: Could not read JSON file, initializing an empty list.")
        return {"total_count": 0, "tasks": []}


def save_tasks(data):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_task(description):
    """Add a new task with a unique ID."""
    data = load_tasks()
    tasks = data["tasks"]

    new_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    tasks.append(new_task)
    data["total_count"] = len(tasks)

    save_tasks(data)
    print(f"Task {new_id} was successfully added.")


def update_task(id, description):
    """Update a task"""
    data = load_tasks()
    tasks = data["tasks"]

    for task in tasks:
        if task["id"] == int(id):
            task["description"] = description
            task["updated_at"] = datetime.now().isoformat()
            save_tasks(data)
            print(f"Task {id} was successfully updated.")
            return

    print("Couldn't find the task you're looking for.")


def change_task_status(id, status):
    """Change task status"""
    data = load_tasks()
    tasks = data["tasks"]
    if status == "in-progress" or status == "done" or status == "todo":
        for task in tasks:
            if task["id"] == int(id):
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                save_tasks(data)
                print(f"Task {id} was marked as {status} successfully.")
                return
        print("Couldn't find the task you're looking for.")


def delete_task(id):
    """Delete a task"""
    data = load_tasks()
    tasks = data["tasks"]

    for task in tasks:
        if task["id"] == int(id):
            tasks.remove(task)
            data["total_count"] = len(tasks)
            save_tasks(data)
            print(f"Task {id} was deleted successfully.")
            return
    print("Couldn't find the task you're looking for.")


def list_all_tasks(status=None):
    """List all tasks, optionally filtered by status"""
    data = load_tasks()
    tasks = data["tasks"]

    filtered_tasks = (
        tasks if status is None else [t for t in tasks if t["status"] == status]
    )

    if not filtered_tasks:
        print(
            "No tasks found." if status is None else f"No tasks with status '{status}'."
        )
        return

    print("\n--- Task List ---")
    for task in filtered_tasks:
        print(
            f"""[{task['id']}] {task['description']} ({task['status']}) - Created: {task['created_at']} - Updated: {task['updated_at']}"""
        )
    print("-----------------\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No command provided.")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task description.")
        else:
            add_task(sys.argv[2])

    elif command == "update":
        if len(sys.argv) < 4:
            print("Error: Please provide task ID and new description.")
        else:
            update_task(sys.argv[2], sys.argv[3])

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
        else:
            delete_task(sys.argv[2])

    elif command == "list":
        list_all_tasks(sys.argv[2] if len(sys.argv) > 2 else None)

    elif command == "mark-todo":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
        else:
            change_task_status(sys.argv[2], "todo")

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
        else:
            change_task_status(sys.argv[2], "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
        else:
            change_task_status(sys.argv[2], "done")

    else:
        print("Error: Unknown command.")
