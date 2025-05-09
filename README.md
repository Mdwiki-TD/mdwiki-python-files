[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Mdwiki-TD/mdwiki-python-files)

# MDWiki Automation Tool

## Overview

This project is a multi-module, bot-oriented automation tool primarily designed for interacting with the MediaWiki ecosystem. It consists of several self-contained Python packages (submodules) that perform various automated tasks. These tasks include copying text, updating references, processing markdown, interfacing with wiki APIs, and performing maintenance. The project emphasizes modularity, reusability, and testability, with a strong focus on automation through GitHub Actions.

## Architecture

The system is structured around several key components:

**1. Bot/Task Modules:**

* **`copy_text`**: Handles text copying operations between wiki pages.
* **`copy_to_en`**: Specifically designed for copying content to the English Wikipedia.
* **`fix_use`**: Focuses on fixing and maintaining the usage of templates or elements within wiki pages.
* **`md_core`**: Provides core functionalities for MediaWiki interactions, including submodules for adding references (`add_rtt`), fixing citation style 1 templates (`fix_cs1`), markdown processing (`mdpy`), and generating statistics (`stats`).
* **`td_core`**: Contains tools for translation-related tasks, such as copying data after translation (`after_translate`), copying data (`copy_data`), and counting markdown elements (`mdcount`).
* **`wprefs`**: Manages wiki preferences and settings, providing API interactions and bot functionalities.
* **`newupdater`**: Facilitates updates and modifications to wiki pages, potentially involving specific update scripts.

Each of these modules contains one or more "bots" (scripts within the `bots` directories or files named `bot.py`) that are responsible for executing specific automation tasks.

**2. Helper and Core Libraries:**

* **`md_core_helps`**: Provides shared functions and integrations, particularly for interacting with MediaWiki APIs and SQL databases. This module is crucial for the other bot modules to perform their tasks effectively.

**3. Testing & Validation:**

* Each major module includes a `tests` directory containing Python files (e.g., `tests.py`) that implement unit and integration tests. This highlights the project's commitment to ensuring the reliability and correctness of its operations.

**4. Configuration & CI/CD:**

* **`.github/workflows`**: Contains GitHub Actions workflow files (`d.yml`, `snorkell-auto-documentation.yml`) that automate various aspects of the development lifecycle, such as continuous integration, testing, and potentially documentation generation.
* **Configuration Files**: Files like `.coderabbit.yaml`, `.pre-commit-config.yaml`, and `sweep.yaml` are used to configure code quality checks, pre-commit hooks, and other development tools, ensuring consistency and maintainability.

**5. External Services and APIs:**

* The bot modules interact with external systems to perform their tasks. These include:
    * **MediaWiki API**: Used to access and modify wiki content. The `md_core_helps/apis` directory contains modules like `mdwiki_api.py` and `wiki_api.py` that facilitate this interaction.
    * **WikiData**: Potentially used for accessing and integrating structured data. The `md_core_helps/apis` directory includes `wikidataapi.py`.
    * **SQL Databases**: Used for data storage and retrieval, as suggested by the presence of `sql.py` and `sqlviews.py`.

## System Design Diagram (Conceptual)

```mermaid
flowchart TD
    A["Automation/CI/CD"]:::automation
    T["Testing & Configuration"]:::testconfig

    subgraph "Bot/Task Layer"
        B1["copy_text Module"]:::bot
        B2["copy_to_en Module"]:::bot
        B3["fix_use Module"]:::bot
        B4["md_core Module"]:::bot
        B5["newupdater Module"]:::bot
        B6["td_core Module"]:::bot
        B7["wprefs Module"]:::bot
    end

    subgraph "Data Processing/Helper Layer"
        C1["md_core_helps API Layer"]:::api
        C2["Database/SQL Module"]:::db
    end

    D["External Wiki Systems"]:::external

    A -->|"triggers"| B1
    A -->|"triggers"| B2
    A -->|"triggers"| B3
    A -->|"triggers"| B4
    A -->|"triggers"| B5
    A -->|"triggers"| B6
    A -->|"triggers"| B7
    A -->|"integrates"| T

    B1 -->|"processes"| C1
    B2 -->|"processes"| C1
    B7 -->|"processes"| C1
    B4 -->|"queries"| C2
    B6 -->|"queries"| C2
    B3 -->|"updates"| D
    B5 -->|"updates"| D

    C1 -->|"integrates"| D
    C2 -->|"updates"| D

    click A "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/.github/workflows/d.yml"
    click B1 "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/copy_text/bot.py"
    click B2 "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/copy_to_en/bot.py"
    click B3 "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/fix_use/bot.py"
    click B4 "https://github.com/mdwiki-td/mdwiki-python-files/tree/main/md_core/"
    click B5 "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/newupdater/MedWorkNew.py"
    click B6 "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/td_core/after_translate/sql_new.py"
    click B7 "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/wprefs/bot.py"
    click C1 "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/md_core_helps/apis/mdwiki_api.py"
    click C2 "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/md_core_helps/mdapi_sql/sql.py"
    click T "https://github.com/mdwiki-td/mdwiki-python-files/blob/main/.pre-commit-config.yaml"

    classDef automation fill:#ffcc00,stroke:#333,stroke-width:2px;
    classDef testconfig fill:#ff9966,stroke:#333,stroke-width:2px;
    classDef bot fill:#ccffcc,stroke:#333,stroke-width:2px;
    classDef api fill:#cce5ff,stroke:#333,stroke-width:2px;
    classDef db fill:#e6ffe6,stroke:#333,stroke-width:2px;
    classDef external fill:#ffe6f2,stroke:#333,stroke-width:2px;
```
