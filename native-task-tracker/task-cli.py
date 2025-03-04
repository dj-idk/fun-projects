import sys
import os
import json
from datetime import datetime

TASKS_FILE = "tasks.json"


class TaskManager:
    """Class to manage tasks with CRUD operations"""

    def __init__(self, file=TASKS_FILE):
        self.file = file
        self.tasks_data = self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file"""
        if not os.path.exists(self.file):
            return {"total_count": 0, "tasks": []}

        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not read JSON file, initializing an empty task list.")
            return {"total_count": 0, "tasks": []}

    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.file, "w") as f:
            json.dump(self.tasks_data, f, indent=4)

    def add_task(self, description):
        """Add a new task"""
        tasks = self.tasks_data["tasks"]
        new_id = max((task["id"] for task in tasks), default=0) + 1

        new_task = {
            "id": new_id,
            "description": description,
            "status": "todo",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        tasks.append(new_task)
        self.tasks_data["total_count"] = len(tasks)
        self.save_tasks()
        print(f"Task {new_id} was successfully added.")

    def update_task(self, task_id, description):
        """Update an existing task"""
        for task in self.tasks_data["tasks"]:
            if task["id"] == int(task_id):
                task["description"] = description
                task["updated_at"] = datetime.now().isoformat()
                self.save_tasks()
                print(f"Task {task_id} was successfully updated.")
                return
        print("Error: Task not found.")

    def change_task_status(self, task_id, status):
        """Change the status of a task"""
        if status not in ["todo", "in-progress", "done"]:
            print("Error: Invalid status.")
            return

        for task in self.tasks_data["tasks"]:
            if task["id"] == int(task_id):
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                self.save_tasks()
                print(f"Task {task_id} marked as {status}.")
                return
        print("Error: Task not found.")

    def delete_task(self, task_id):
        """Delete a task"""
        tasks = self.tasks_data["tasks"]
        for task in tasks:
            if task["id"] == int(task_id):
                tasks.remove(task)
                self.tasks_data["total_count"] = len(tasks)
                self.save_tasks()
                print(f"Task {task_id} deleted successfully.")
                return
        print("Error: Task not found.")

    def list_tasks(self, status=None):
        """List all tasks, optionally filtered by status"""
        tasks = self.tasks_data["tasks"]
        filtered_tasks = (
            tasks if status is None else [t for t in tasks if t["status"] == status]
        )

        if not filtered_tasks:
            print(
                "No tasks found."
                if status is None
                else f"No tasks with status '{status}'."
            )
            return

        print("\n--- Task List ---")
        for task in filtered_tasks:
            print(
                f"[{task['id']}] {task['description']} ({task['status']}) - "
                f"Created: {task['created_at']} - Updated: {task['updated_at']}"
            )
        print("-----------------\n")


if __name__ == "__main__":
    manager = TaskManager()

    if len(sys.argv) < 2:
        print("Error: No command provided.")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task description.")
        else:
            manager.add_task(" ".join(sys.argv[2:]))

    elif command == "update":
        if len(sys.argv) < 4:
            print("Error: Please provide task ID and new description.")
        else:
            manager.update_task(sys.argv[2], " ".join(sys.argv[3:]))

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
        else:
            manager.delete_task(sys.argv[2])

    elif command == "list":
        manager.list_tasks(sys.argv[2] if len(sys.argv) > 2 else None)

    elif command == "mark-todo":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
        else:
            manager.change_task_status(sys.argv[2], "todo")

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
        else:
            manager.change_task_status(sys.argv[2], "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Error: Please provide a task ID.")
        else:
            manager.change_task_status(sys.argv[2], "done")

    else:
        print("Error: Unknown command.")
