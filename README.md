# PySlyphie

**PySlyphie** is a **next-generation, tool-augmented AI framework** designed to empower LLMs with multifunctional capabilities. Unlike traditional AI models that only generate text, PySlyphie allows an LLM to **interact dynamically with modules, tools, and external data sources**, enabling it to perform tasks autonomously, asynchronously, and intelligently.

---

## Table of Contents

* [Overview](#overview)
* [Key Features](#key-features)
* [Architecture](#architecture)
* [Modules](#modules)
* [Installation](#installation)
* [Usage](#usage)
* [Extending PySlyphie](#extending-pyslyphie)
* [Examples](#examples)
* [Philosophy & Vision](#philosophy--vision)
* [License](#license)

---

## Overview

PySlyphie is a **Python library that transforms a standard LLM into a multifunctional AI agent**. It achieves this by providing a **modular plugin system** that exposes various tools the LLM can call programmatically.

Core concepts:

* **Modules:** Collections of commands (functions) with schemas describing capabilities.
* **Job Queueing:** Asynchronous execution of tasks, with tracking of progress and results.
* **Web & Knowledge Access:** Built-in support for web scraping, DuckDuckGo search, Wikipedia retrieval, and cleaning of HTML content for LLM consumption.
* **Integration Ready:** Interfaces with GUI frontends (via WebView) and supports logging and context updating.

PySlyphie is designed to be **extensible**, **autonomous**, and **tool-driven**, enabling AI to go beyond text generation and interact with the world programmatically.

---

## Key Features

* **Unified Search Engine:**

  * Search the web, DuckDuckGo summaries, and Wikipedia programmatically.
  * Fetch, clean, and summarize HTML content for LLM-friendly input.

* **Modular Tool System:**

  * Network utilities (ping, trace routes, TCP scans, IP info)
  * Open camera access worldwide
  * String utilities (hex ↔ string, word combinations)

* **Asynchronous Job Execution:**

  * Commands are executed in threads and tracked with job IDs.
  * LLM can request a task and check status/results without blocking.

* **Web & GUI Integration:**

  * Provides real-time progress updates through a `Window` object.
  * Logs can be sent to a web service or frontend dashboard.

* **LLM-Focused Design:**

  * The library is built to allow an AI model to dynamically reason, select, and execute the right tools for tasks.
  * Provides structured outputs (schemas) for programmatic AI consumption.

---

## Architecture

```
+--------------------+
|     LLM Agent      |
+--------------------+
           |
           v
+--------------------+      +--------------------+
|  PySlyphie Core    | ---> | Module Registry     |
|  (fnt.py, cache,   |      |   net, ocam, string|
|   ContextUpdater)  |      +--------------------+
+--------------------+
           |
           v
+--------------------+
| Asynchronous Jobs  |
|   (job queue,      |
|    status tracking)|
+--------------------+
           |
           v
+--------------------+
| External Resources |
|  Web Scraping      |
|  APIs, Cameras     |
|  Wikipedia, DDG    |
+--------------------+
```

---

## Modules

PySlyphie comes with several **pre-registered modules**:

### 1. Network Utilities (`net`)

* **ping(host):** Ping a host.
* **domtrace(domain):** Trace a domain’s route.
* **domrtrace(domain):** Reverse trace a domain.
* **tcp(host, port_range):** Run a TCP scan.
* **ip(host):** Get detailed information about an IP address.

### 2. Open Camera Access (`ocam`)

* **update():** Update the camera index.
* **add(url):** Add an open camera URL.
* **get(url):** Fetch an image from the camera.
* **len():** Get the number of available cameras.
* **list():** List all available cameras.
* **feed():** Feed camera to a monitor.
* **for():** Get a specific list of cameras.

### 3. String Utilities (`string`)

* **h2s(hex_str):** Convert hex to string.
* **s2h(str):** Convert string to hex.
* **fco(word):** Generate all possible combinations of a word.

### 4. Web & Knowledge (`web.py`)

* **fetch(module='all', query, solve, results):** Query web, DuckDuckGo, or Wikipedia.
* **from_url(url):** Fetch content from a URL.
* **from_sources(sources):** Fetch and clean multiple URLs.
* **wiki_event_api(mode, date, month):** Fetch historical events or deaths from a given date.

---

## Usage

```python
from pyslyphie.fnt import exec_module_cmd, get_job, list_modules

# List all modules and their commands
print(list_modules())

# Execute a network ping asynchronously
res = exec_module_cmd("net", "ping", '["8.8.8.8"]', js=None)
job_id = res["job_id"]

# Later, check job status
status = get_job(job_id)
print(status)
```

---

## Extending PySlyphie

You can **add new modules** by defining:

1. A **schema** describing the module and commands.
2. A **handler map** connecting command names to Python functions.

```python
from pyslyphie.fnt import register_module

def my_hello_handler(args, js=None):
    return f"Hello, {args[0]}!"

register_module(
    "my_module",
    {
        "desc": "Example module",
        "commands": {"hello": {"desc": "Greet someone"}}
    },
    {"hello": my_hello_handler}
)
```

---

## Examples

* **Fetch and clean Wikipedia summary**

```python
from pyslyphie.web import UnifiedSearchEngine

se = UnifiedSearchEngine()
data = se.fetch(module='wiki', query="Nikola Tesla")
print(data)
```

* **Async job with network scan**

```python
res = exec_module_cmd("net", "tcp", '["192.168.0.1"]', js=None)
job_id = res["job_id"]
print(get_job(job_id))
```

---

## Philosophy & Vision

PySlyphie is **designed for the next evolution of AI**:

1. **Tool-Augmented AI:** Give LLMs real-world tools beyond text.
2. **Autonomous Decision-Making:** LLM can reason, select, and execute tasks dynamically.
3. **Modular & Extensible:** Developers can easily add new capabilities.
4. **Asynchronous Intelligence:** Tasks run in parallel without blocking the AI agent.

This approach enables a **truly multifunctional AI** capable of research, data analysis, automation, and world interaction — all programmatically controlled by a reasoning LLM.

---

## License

MIT License — see `LICENSE` file.

---
