import argparse
import json
from pathlib import Path
from typing import Optional

DEFAULT_PATH = Path(__file__).with_name(".phasebuilder_tasks.json")


def _load_tasks(path: Path) -> list[dict]:
    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    if isinstance(data, list):
        return [task for task in data if isinstance(task, dict)]

    return []


def _save_tasks(path: Path, tasks: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add_task(title: str, note: Optional[str] = None, priority: str = "medium", path: Optional[Path] = None) -> dict:
    storage_path = path or DEFAULT_PATH
    tasks = _load_tasks(storage_path)
    new_task = {
        "id": (tasks[-1]["id"] + 1) if tasks else 1,
        "title": title,
        "note": note or "",
        "priority": priority,
        "completed": False,
    }
    tasks.append(new_task)
    _save_tasks(storage_path, tasks)
    return new_task


def update_task(
    task_id: int,
    title: Optional[str] = None,
    note: Optional[str] = None,
    priority: Optional[str] = None,
    path: Optional[Path] = None,
) -> Optional[dict]:
    storage_path = path or DEFAULT_PATH
    tasks = _load_tasks(storage_path)

    for task in tasks:
        if task.get("id") == task_id:
            if title is not None:
                task["title"] = title
            if note is not None:
                task["note"] = note
            if priority is not None:
                task["priority"] = priority
            _save_tasks(storage_path, tasks)
            return task

    return None


def list_tasks(path: Optional[Path] = None, completed: Optional[bool] = None) -> list[dict]:
    storage_path = path or DEFAULT_PATH
    tasks = _load_tasks(storage_path)

    if completed is None:
        return tasks

    return [task for task in tasks if task.get("completed") is completed]


def complete_task(task_id: int, path: Optional[Path] = None) -> Optional[dict]:
    storage_path = path or DEFAULT_PATH
    tasks = _load_tasks(storage_path)

    for task in tasks:
        if task.get("id") == task_id:
            task["completed"] = True
            _save_tasks(storage_path, tasks)
            return task

    return None


def delete_task(task_id: int, path: Optional[Path] = None) -> bool:
    storage_path = path or DEFAULT_PATH
    tasks = _load_tasks(storage_path)
    remaining = [task for task in tasks if task.get("id") != task_id]

    if len(remaining) == len(tasks):
        return False

    _save_tasks(storage_path, remaining)
    return True


def complete_all_tasks(path: Optional[Path] = None) -> int:
    storage_path = path or DEFAULT_PATH
    tasks = _load_tasks(storage_path)
    pending = [task for task in tasks if not task.get("completed")]

    for task in pending:
        task["completed"] = True

    if pending:
        _save_tasks(storage_path, tasks)

    return len(pending)


def search_tasks(keyword: str, path: Optional[Path] = None) -> list[dict]:
    storage_path = path or DEFAULT_PATH
    query = keyword.lower()
    tasks = _load_tasks(storage_path)
    return [
        task
        for task in tasks
        if query in str(task.get("title", "")).lower()
        or query in str(task.get("note", "")).lower()
        or query in str(task.get("priority", "")).lower()
    ]


def task_stats(path: Optional[Path] = None) -> dict:
    storage_path = path or DEFAULT_PATH
    tasks = _load_tasks(storage_path)
    completed = sum(1 for task in tasks if task.get("completed"))
    return {
        "total": len(tasks),
        "completed": completed,
        "pending": len(tasks) - completed,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PhaseBuilder task manager")
    parser.add_argument("--path", default=str(DEFAULT_PATH), help="Path to the task storage file")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("--title", required=True, help="Task title")
    add_parser.add_argument("--note", default="", help="Optional task note")
    add_parser.add_argument("--priority", default="medium", choices=["low", "medium", "high"], help="Task priority")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--all", action="store_true", help="Show completed and pending tasks")

    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to complete")

    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("task_id", type=int, help="ID of the task to update")
    update_parser.add_argument("--title", help="New task title")
    update_parser.add_argument("--note", help="New task note")
    update_parser.add_argument("--priority", choices=["low", "medium", "high"], help="New task priority")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to remove")

    subparsers.add_parser("complete-all", help="Mark all pending tasks as complete")

    search_parser = subparsers.add_parser("search", help="Search tasks")
    search_parser.add_argument("keyword", help="Keyword to search for")

    subparsers.add_parser("stats", help="Show task statistics")
    return parser


def _print_tasks(tasks: list[dict]) -> None:
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "x" if task.get("completed") else " "
        note = f" - {task.get('note')}" if task.get("note") else ""
        print(f"[{status}] {task['id']}. {task['title']} ({task['priority']}){note}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    storage_path = Path(args.path)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "add":
        task = add_task(args.title, note=args.note, priority=args.priority, path=storage_path)
        print(f"Added task {task['id']}: {task['title']}")
        return 0

    if args.command == "list":
        completed_filter = None if args.all else False
        _print_tasks(list_tasks(path=storage_path, completed=completed_filter))
        return 0

    if args.command == "complete":
        task = complete_task(args.task_id, path=storage_path)
        if task:
            print(f"Completed task {task['id']}: {task['title']}")
        else:
            print("Task not found.")
        return 0

    if args.command == "update":
        task = update_task(
            args.task_id,
            title=args.title,
            note=args.note,
            priority=args.priority,
            path=storage_path,
        )
        if task:
            print(f"Updated task {task['id']}: {task['title']}")
        else:
            print("Task not found.")
        return 0

    if args.command == "delete":
        deleted = delete_task(args.task_id, path=storage_path)
        if deleted:
            print(f"Deleted task {args.task_id}.")
        else:
            print("Task not found.")
        return 0

    if args.command == "complete-all":
        completed_count = complete_all_tasks(path=storage_path)
        print(f"Completed {completed_count} task(s).")
        return 0

    if args.command == "search":
        _print_tasks(search_tasks(args.keyword, path=storage_path))
        return 0

    if args.command == "stats":
        stats = task_stats(path=storage_path)
        print(f"Total: {stats['total']}")
        print(f"Completed: {stats['completed']}")
        print(f"Pending: {stats['pending']}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
