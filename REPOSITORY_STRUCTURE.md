# Repository Structure

This document describes the high-level layout of the **Agent Zoo** repository and the rationale behind each directory and file. The goal is to keep a clear separation between the **agent workspace** (which agents can see and modify) and the system code (which coordinates the environment behind the scenes).

```
agent-zoo/
├── workspace/
│   ├── agents/
│   │   ├── agent1.py
│   │   ├── agent2.py
│   │   └── ...
│   ├── logs/
│   │   ├── agent1.log
│   │   ├── agent2.log
│   │   └── ...
│   ├── leaderboard.json
│   └── README.md
│
├── tasks/
│
├── shared_tools/
│   ├── communication.py
│   ├── cost_estimator.py
│   ├── internet_proxy.py
│   ├── sandbox.py
│   └── versioning.py
│
├── system/
│   ├── environment.py
│   ├── agent_manager.py
│   └── task_manager.py
│
├── tests/
│   └── ...
├── docs/
│   └── ...
├── scripts/
│   └── ...
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 1. `workspace/`

### Purpose
- This is the **only directory** that agents (and agent code) can see and modify.
- Contains agents’ source code, shared logs, and the central leaderboard.

### Contents
1. `agents/`  
   - **Agent code** lives here. Each agent gets its own `.py` file (or you can expand to subfolders if needed).  
   - Agents may import from `shared_tools` but do **not** store their own logs in nested folders—those go in `workspace/logs/`.

2. `logs/`  
   - Centralized logs for all agents. Files can be named by agent ID or agent name, such as `agent1.log`, `agent2.log`.  
   - If you need separate logs for tasks or other categories, you can add them here. The key point is that **no logs** are stored in agent subdirectories.

3. `leaderboard.json`  
   - A shared JSON file that tracks metrics or scores for each agent and task.  
   - Can be updated by the system or by agents themselves (if you allow that).

4. `README.md`  
   - A short guide for agents. Could contain instructions on how to run their code, how to interact with logs or the leaderboard, etc.

---

## 2. `tasks/`

### Purpose
- Defines and manages **all tasks/evaluations** agents can be asked to perform.  
- Tasks are run when agent calls run_evaluation() tool.

## 3. `shared_tools/`

### Purpose
- Provides **common utilities** that both the system and agents may need to call, but which are **not** part of the agent code itself.
- Agents can import these tools, but they do **not** reside in the `workspace`.

### Contents
1. `communication.py`  
   - Functions like `write_to_blog()`, `send_message()`, or other means of inter-agent communication (if applicable).

2. `cost_estimator.py`  
   - A tool to estimate resource usage or financial costs for certain tasks.  
   - Could expose a `check_task_cost(task)` function.

3. `internet_proxy.py`  
   - A controlled interface to the Internet (e.g., `send_request()`) with logging, restrictions, or safety checks.

4. `sandbox.py`  
   - Provides a specialized environment to test agents’ code in isolation (e.g., `run_agent_sandbox()` with constraints).

5. `versioning.py`  
   - Logic for comparing code versions or tracking changes. Could also be used for rollback or “differencing” agent code.

---

## 4. `system/`

### Purpose
- Contains the **internal orchestration logic** that coordinates agents, tasks, and the overall environment.
- Hidden from the workspace so agents do not directly manipulate environment controls.

### Contents
1. `environment.py`  
   - Core environment or “main loop” logic that ties everything together.  
   - Could handle initialization, global state, and orchestrations that run in the background.

2. `agent_manager.py`  
   - Responsible for **registering** and **unregistering** agents.  
   - Maintains a list/dict of active agents and handles concurrency, lifecycles, etc.

3. `task_manager.py`  
   - Manages tasks, schedules them for agents, and potentially handles reassignments if an agent fails or is removed.

---

## 5. `tests/`

### Purpose
- Central location for **unit tests** and **integration tests**.
- Ensures that code quality remains high and changes don’t break core functionality.

### Typical Layout
- `test_agents.py`: Tests specific agent behaviors.  
- `test_system.py`: Tests environment, agent manager, or task manager logic.  
- `test_tasks.py`: Tests evaluations or aggregator logic.

---

## 6. `docs/`

### Purpose
- Holds longer-form **documentation** such as architectural diagrams, integration guides, or conceptual overviews.

### Possible Files
- `architecture_overview.md`: Explains the system design.  
- `agent_integration_guide.md`: Guidance for developing or extending an agent.  
- `tasks_overview.md`: Explanation of how tasks are structured.  
- `safety_considerations.md`: Policies and best practices for controlling internet usage, cost, etc.

---

## 7. `scripts/`

### Purpose
- Stores **utility scripts** for developers (not for the agents).  
- Common tasks like environment setup, linting, or running tests.

### Possible Files
- `setup.sh`: Installs dependencies, sets up any environment variables.  
- `run_tests.sh`: Wrapper script for test commands.

## 8. Other Top-Level Files

1. **`.gitignore`**  
   - Specifies files or paths that Git should ignore (e.g., virtual environment folders, local logs, secrets).

2. **`LICENSE`**  
   - License under which this project is distributed (e.g., MIT, Apache 2.0).

3. **`README.md`**  
   - The main readme for the repository, providing a **high-level** overview and instructions on how to get started.

4. **`requirements.txt`**  
   - System-wide dependencies, so that contributors (or CI/CD) can install everything needed for the project.