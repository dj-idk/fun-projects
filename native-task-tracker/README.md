# CLI Task Manager

A simple command-line task manager that allows you to add, update, delete, and track tasks with different statuses.

## Features
- Add tasks with descriptions
- Update task descriptions
- Delete tasks by ID
- List all tasks or filter by status
- Mark tasks as "todo", "in-progress", or "done"
- Persistent storage using a JSON file

## Installation
Ensure you have Python installed, then clone this repository:

```sh
git clone <repo-url>
cd cli-task-manager
```

## Usage
Run the script with the appropriate command:

```sh
python task_manager.py <command> [arguments]
```

### Commands
| Command                 | Description |
|-------------------------|-------------|
| `add <description>`     | Add a new task |
| `update <id> <desc>`   | Update task description |
| `delete <id>`          | Delete a task |
| `list [status]`        | List tasks (optional: filter by status) |
| `mark-todo <id>`       | Set task status to "todo" |
| `mark-in-progress <id>` | Set task status to "in-progress" |
| `mark-done <id>`       | Set task status to "done" |

### Examples
**Adding a task:**
```sh
python task_manager.py add "Buy groceries"
```

**Updating a task:**
```sh
python task_manager.py update 1 "Buy groceries and milk"
```

**Listing tasks:**
```sh
python task_manager.py list
```

**Marking a task as done:**
```sh
python task_manager.py mark-done 1
```

## Notes
- Tasks are stored in `tasks.json`.
- Ensure the script has write permissions to modify the JSON file.

## License
This project is open-source. Feel free to modify and use it as needed.

