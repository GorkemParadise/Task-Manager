from collections import deque
from decorators import log_action, timer
import os


class FileManager:
    """Context manager for safe file operations."""
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc, tb):
        if self.file:
            self.file.close()


class TaskManager:
    """
    A class to manage tasks using a queue.
    """

    def __init__(self, filename="queue.txt"):
        self.tasks = deque()
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the queue file safely."""
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()  # create empty queue file

        with FileManager(self.filename, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) < 4:   # skip corrupted lines
                    continue

                name, due_date, completed, description = parts

                task = {
                    "name": name,
                    "due_date": due_date,
                    "completed": completed == "True",
                    "description": description
                }
                self.tasks.append(task)

    @log_action
    @timer
    def add_task(self, name, due_date, description):
        """Add a new task to the task queue."""
        new_task = {
            "name": name,
            "due_date": due_date,
            "completed": False,
            "description": description
        }

        self.tasks.append(new_task)
        self.save_tasks_to_file()

    @log_action
    @timer
    def view_tasks(self):
        """Display all tasks in the queue."""
        if not self.tasks:
            print("No tasks in the queue.")
            return

        for index, task in enumerate(self.tasks):
            print(f"{index + 1}. {self.task_to_string(task)}")

    @log_action
    @timer
    def mark_complete(self, task_index):
        """Mark a task as completed and move it to completed_tasks.txt."""
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            task["completed"] = True

            # save to completed file
            self.save_completed_task(task)

            # remove from queue
            del self.tasks[task_index]

            # rewrite queue file
            self.save_tasks_to_file()

            print(f"Task '{task['name']}' marked as complete.")
        else:
            print("Task not found.")

    def save_tasks_to_file(self):
        """Rewrite the queue file with updated tasks."""
        with FileManager(self.filename, "w") as f:
            for task in self.tasks:
                f.write(f"{task['name']},{task['due_date']},{task['completed']},{task['description']}\n")

    def save_completed_task(self, task):
        """Append completed task to completed_tasks.txt."""
        with FileManager("completed_tasks.txt", "a") as f:
            f.write(f"{task['name']},{task['due_date']},{task['completed']},{task['description']}\n")

    def task_to_string(self, task):
        """Convert a task dictionary to a readable format."""
        mark = "x" if task["completed"] else " "
        return f"[{mark}] {task['name']} (Due: {task['due_date']}) - {task['description']}"

    @log_action
    @timer
    def view_next_queue_task(self):
        """View the next task without removing it."""
        if not self.tasks:
            return "No tasks in the queue."
        return self.task_to_string(self.tasks[0])
