# PhaseBuilder

PhaseBuilder is a small Python command-line task manager created to demonstrate a slow, phased development process with many small commits. The project starts simple and grows through a series of incremental improvements, making it a good example of how a lightweight idea can evolve into a more polished tool over time.

## Overview

This repository contains a dependency-free task manager that stores tasks in a JSON file. It is intentionally simple so it can be used as a learning project, a daily task helper, or a reference for practicing Git workflows with lots of small, well-labeled commits.

## What the tool does

PhaseBuilder allows you to:

- add tasks with a title and optional note
- assign a priority level to each task
- list pending or completed tasks
- mark tasks as complete
- remove tasks you no longer need
- search tasks by keyword
- review simple task statistics

## Features

- lightweight and fast
- no external dependencies required
- plain JSON storage for portability
- a simple CLI for everyday use
- easy to extend in future phases

## Installation

1. Open the project folder.
2. Make sure Python 3.10 or newer is available.
3. Run the script from the project root.

```bash
python file1.py --help
```

## Usage examples

Add a task:

```bash
python file1.py add --title "Write project summary"
```

Add a task with a note and priority:

```bash
python file1.py add --title "Review design" --note "Check the roadmap" --priority high
```

List pending tasks:

```bash
python file1.py list
```

List all tasks including completed ones:

```bash
python file1.py list --all
```

Complete a task:

```bash
python file1.py complete 1
```

Delete a task:

```bash
python file1.py delete 1
```

Search tasks:

```bash
python file1.py search roadmap
```

Show statistics:

```bash
python file1.py stats
```

## Project structure

- file1.py - the main CLI application
- tests/test_file1.py - regression tests for core task operations
- README.md - overview and usage guide
- .gitignore - local exclusions for Python development
- requirements.txt - dependency placeholder for future growth

## Development approach

This project is being built in small, reviewable phases. The commit history is meant to reflect a calm workflow where each step adds a little more value without trying to do everything at once.

Planned phases include:

1. scaffold the project structure
2. add core task persistence and data handling
3. expand CLI commands for everyday use
4. improve test coverage and documentation
5. refine the UX and prepare future features

## Future ideas

- add due dates and reminders
- support tags and categories
- export and import task lists
- add a web or GUI version
- add automated tests in CI

## Notes

The project is intentionally simple so it can serve as a practical example of incremental development and gradual Git history growth.
