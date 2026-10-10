import json
import os

FILE_NAME = "tasks.json"


# ---------- MODEL (data logic) ----------
def load_tasks():
    """Read tasks from disk. Return an empty list if no file yet."""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_tasks(tasks):
    """Write the whole list to disk as JSON."""
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(tasks, text):
    """Append a new task (a dictionary) to the list."""
    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": new_id, "task": text})
    save_tasks(tasks)


def delete_task(tasks, number):
    """Remove task by its displayed number (1-based). Return True if removed."""
    if 1 <= number <= len(tasks):
        tasks.pop(number - 1)
        save_tasks(tasks)
        return True
    return False


# ---------- VIEW (user interface) ----------
def show_menu():
    print("\n===== TO-DO LIST =====")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Delete a task")
    print("4. Exit")


def view_tasks(tasks):
    if not tasks:
        print("Your list is empty.")
        return
    print("\nYour tasks:")
    for index, item in enumerate(tasks, start=1):
        print(f"{index}. {item['task']}")


# ---------- MAIN LOOP ----------
def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            text = input("Enter a task: ").strip()
            if text:
                add_task(tasks, text)
                print("Task added!")
            else:
                print("Task cannot be empty.")

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            view_tasks(tasks)
            if tasks:
                try:
                    number = int(input("Task number to delete: "))
                    if delete_task(tasks, number):
                        print("Task deleted.")
                    else:
                        print("That number doesn't exist.")
                except ValueError:
                    print("Please type a number.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()