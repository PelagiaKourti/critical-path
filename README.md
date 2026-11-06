# Critical Path Method (CPM)

A small Python implementation of the Critical Path Method for project scheduling, with a Gantt chart.

Given a list of tasks with durations and dependencies, it computes for every task:

- **ES / EF**: earliest start and earliest finish (forward pass)
- **LS / LF**: latest start and latest finish (backward pass)
- **Slack**: how long a task can be delayed without delaying the whole project (LS − ES)
- **Critical tasks**: the tasks with zero slack, which determine the project duration
- **Kahn's algorithm**: topological sorting of tasks, so tasks can be given in any order (contaings cycle detection)


## Input

Each task has a duration and a list of predecessors:

```python
tasks = {
    "A": (4, []),
    "B": (3, []),
    "C": (5, ["A", "B"]),
    "D": (5, ["C"]),
    "E": (6, ["C"]),
    "F": (3, ["D", "E"]),
    "G": (4, ["B"]),
    "H": (1, ["F", "G"]),
}
```

Tasks must be listed so that every task comes after its predecessors.

## Usage

Requires Python 3 and matplotlib (`pip install matplotlib`).

```python
from cpm import cpm, gantt

results = cpm(tasks)
print(results["critical"])   # ['A', 'C', 'E', 'F', 'H']
print(results["slack"])      # {'A': 0, 'B': 1, 'C': 0, ..., 'G': 11, 'H': 0}

gantt(tasks, results)
```

Running `python cpm.py` executes this example.

## Results for the example

| Task | Duration | ES | EF | LS | LF | Slack |
|------|----------|----|----|----|----|-------|
| A | 4 | 0 | 4 | 0 | 4 | **0** |
| B | 3 | 0 | 3 | 1 | 4 | 1 |
| C | 5 | 4 | 9 | 4 | 9 | **0** |
| D | 5 | 9 | 14 | 10 | 15 | 1 |
| E | 6 | 9 | 15 | 9 | 15 | **0** |
| F | 3 | 15 | 18 | 15 | 18 | **0** |
| G | 4 | 3 | 7 | 14 | 18 | 11 |
| H | 1 | 18 | 19 | 18 | 19 | **0** |

Critical path: **A → C → E → F → H**, project duration **19 days**.

In the Gantt chart, critical tasks are shown in red, other tasks in green, and the available slack in light green.

## How it works

The project is a directed acyclic graph (DAG): tasks are nodes and dependencies are edges.

- **Forward pass** (in dependency order): `ES = max(EF of predecessors)`, `EF = ES + duration`
- **Backward pass** (in reverse order): `LF = min(LS of successors)`, `LS = LF − duration`

Each task and each dependency is processed once, so the computation is linear in the size of the project.

## Notes

- **Unlimited resources.** CPM assumes that tasks without mutual dependencies can run in parallel. With limited people or equipment, a resource-levelling step is needed, and the project may take longer.
- **Multiple critical paths.** If, for example, task D lasts 6 days instead of 5, both A → C → D → F → H and A → C → E → F → H become critical, and `critical` returns the tasks of both.


## Roadmap

- List each critical path separately (recursive search)
- PERT: three-point duration estimates and Monte Carlo simulation of the project duration
- Resource-constrained scheduling
