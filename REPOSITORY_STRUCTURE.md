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
│   ├── web_browser.py
│   └── evaluation.py
│
│
├── system/
│   └── agent_manager.py
│
├── tests/
│   └── ...
├── docs/
│   └── ...
├── utils/
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
2. `web_browser.py`  
   - Functions like `browse_web()`, `search_web()`, or other means of interacting with the web (if applicable).
3. `evaluation.py`  
   - Functions like `run_evaluation()`, `get_leaderboard()`, or other means of evaluating agents (if applicable).
4. Other tools

---

## 4. `system/`

### Purpose
- Contains the **internal orchestration logic** that coordinates agents, tasks, and the overall environment.
- Hidden from the workspace so agents do not directly manipulate environment controls.

### Contents

1. `agent_manager.py`  
   - Responsible for **registering** and **unregistering** agents.  
   - Maintains a list/dict of active agents and handles concurrency, lifecycles, etc.
   - This list is used to populate and update system prompts of all agents with current list of active agents.

---

## 5. `tests/`

- Central location for **unit tests** and **integration tests**.

---

## 6. `docs/`


---

## 7. `scripts/`

- Stores **utility scripts** for developers (not for the agents).  
- Common tasks like environment setup, linting, or running tests.

## 8. Other Top-Level Files

1. **`.gitignore`**  
   - Specifies files or paths that Git should ignore (e.g., virtual environment folders, local logs, secrets).

2. **`LICENSE`**  
   - License under which this project is distributed (e.g., MIT, Apache 2.0).

3. **`README.md`**  
   - The main readme for the repository, providing a **high-level** overview and instructions on how to get started.