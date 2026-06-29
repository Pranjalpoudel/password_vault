from pathlib import Path

from file1 import (
    add_task,
    complete_task,
    delete_task,
    list_tasks,
    search_tasks,
    task_stats,
)


def test_add_and_list_tasks(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"

    task = add_task("Write plan", note="Use the roadmap", priority="high", path=path)

    assert task["title"] == "Write plan"
    assert task["note"] == "Use the roadmap"
    assert task["priority"] == "high"

    tasks = list_tasks(path=path)
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Write plan"


def test_complete_delete_and_stats(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"

    add_task("Review code", path=path)
    add_task("Ship release", path=path)

    complete_task(1, path=path)
    remaining = list_tasks(path=path, completed=False)

    assert len(remaining) == 1
    assert remaining[0]["title"] == "Ship release"

    deleted = delete_task(2, path=path)
    assert deleted is True

    stats = task_stats(path=path)
    assert stats["total"] == 1
    assert stats["completed"] == 1
    assert stats["pending"] == 0


def test_search_tasks(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"

    add_task("Refactor parser", note="Improve CLI", path=path)
    add_task("Write docs", note="Document parser", path=path)

    matches = search_tasks("parser", path=path)
    assert len(matches) == 2
