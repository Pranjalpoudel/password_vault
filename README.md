# PhaseBuilder

PhaseBuilder is a small Python command-line task tracker designed to demonstrate a calm, phased development process with many small commits. The project starts simple and grows through a series of incremental improvements.

## What this project does

PhaseBuilder helps you manage a personal task list from your terminal. You can:

- add a task with a title and optional note
- list active or completed tasks
- mark tasks as complete
- delete tasks you no longer need
- search by keyword
- review simple task statistics

## Features

- lightweight and dependency-free
- JSON-backed storage for tasks
- simple CLI commands for daily use
- easy to extend for future phases

## Installation

1. Open the project folder.
2. Run the script with Python 3.10+.

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

List tasks:

```bash
python file1.py list
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

Show task statistics:

```bash
python file1.py stats
```

## Project structure

- file1.py - main CLI application
- README.md - overview and usage guide
- .gitignore - local development exclusions

## Development approach

This repository is intentionally built in small, reviewable steps. The commit history is meant to reflect a slow, phased workflow:

1. scaffold the project
2. add the core task model
3. expand CLI commands
4. improve documentation and polish

## Future ideas

- add due dates and reminders
- add export/import support
- add a web-based interface
- add tests and CI workflow

## Notes

The project is intentionally simple so it can be used as a reference for incremental Git history and gradual project growth.
