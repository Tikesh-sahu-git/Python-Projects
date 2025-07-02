import json
import os

USERS_FILE = "users.json"
TODO_FILE = "todos.json"

# Load or create JSON files
def load_data(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f)
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Auth Functions
def signup():
    users = load_data(USERS_FILE)
    username = input("Enter new username: ")
    if username in users:
        print("Username already exists.")
        return None
    password = input("Enter new password: ")
    users[username] = password
    save_data(USERS_FILE, users)
    print("Signup successful.")
    return username

def login():
    users = load_data(USERS_FILE)
    username = input("Enter username: ")
    password = input("Enter password: ")
    if users.get(username) == password:
        print("Login successful.")
        return username
    else:
        print("Invalid credentials.")
        return None

# Todo Functions
def add_task(username):
    todos = load_data(TODO_FILE)
    task = input("Enter a task: ")
    todos.setdefault(username, []).append(task)
    save_data(TODO_FILE, todos)
    print("Task added.")

def view_tasks(username):
    todos = load_data(TODO_FILE)
    user_tasks = todos.get(username, [])
    if not user_tasks:
        print("No tasks.")
    else:
        for i, task in enumerate(user_tasks, 1):
            print(f"{i}. {task}")

def remove_task(username):
    todos = load_data(TODO_FILE)
    tasks = todos.get(username, [])
    view_tasks(username)
    try:
        task_num = int(input("Enter task number to remove: "))
        if 1 <= task_num <= len(tasks):
            removed = tasks.pop(task_num - 1)
            todos[username] = tasks
            save_data(TODO_FILE, todos)
            print(f"Removed: {removed}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Enter a valid number.")

# Main CLI Loop
def main():
    while True:
        print("Welcome to CLI To-Do App with Auth")
        current_user = None

        while not current_user:
            choice = input("\n1. Signup\n2. Login\n3. Exit\nChoose an option: ")
            if choice == '1':
                current_user = signup()
            elif choice == '2':
                current_user = login()
            elif choice == '3':
                print("Goodbye!")
                return
            else:
                print("Invalid choice.")

        while current_user:
            print("\nTo-Do Menu:")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Remove Task")
            print("4. Logout")
            print("5. Exit")

            option = input("Choose an option: ")

            if option == '1':
                add_task(current_user)
            elif option == '2':
                view_tasks(current_user)
            elif option == '3':
                remove_task(current_user)
            elif option == '4':
                current_user = None
                print("Logged out.")
            elif option == '5':
                print("Goodbye!")
                return
            else:
                print("Invalid option.")

if __name__ == "__main__":
    main()
