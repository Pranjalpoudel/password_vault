from pathlib import Path

from file1 import (
    add_task,
    complete_all_tasks,
    complete_task,
    delete_task,
    list_tasks,
    search_tasks,
    task_stats,
    task_summary,
    update_task,
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


def test_update_task(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"

    add_task("Draft outline", note="Initial draft", path=path)

    updated = update_task(1, title="Draft outline v2", note="Refined draft", priority="high", path=path)

    assert updated is not None
    assert updated["title"] == "Draft outline v2"
    assert updated["note"] == "Refined draft"
    assert updated["priority"] == "high"


def test_complete_all_tasks(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"

    add_task("Draft plan", path=path)
    add_task("Ship update", path=path)

    completed_count = complete_all_tasks(path=path)

    assert completed_count == 2
    assert list_tasks(path=path, completed=False) == []


def test_list_tasks_by_priority(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"

    add_task("Plan sprint", priority="high", path=path)
    add_task("Review notes", priority="low", path=path)

    filtered = list_tasks(path=path, priority="high")

    assert len(filtered) == 1
    assert filtered[0]["title"] == "Plan sprint"


def test_task_summary(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"

    add_task("Draft plan", path=path)
    add_task("Ship update", path=path)
    complete_task(1, path=path)

    assert task_summary(path=path) == "1 pending, 1 completed, 2 total"
