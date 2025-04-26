# semeval-task8

Python repository containing the proposed solution for **SemEval-2025 Task 8** (Subtask-1 and Subtask-2). This project uses a language-model-driven SQL agent to automatically query tabular datasets and answer natural-language questions.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Data Preparation](#data-preparation)
- [Database Generation](#database-generation)
- [Running the SQL Agent](#running-the-sql-agent)
- [Evaluation](#evaluation)
- [Scripts Details](#scripts-details)
- [Contributing](#contributing)

## Project Overview

SemEval-2025 Task 8 involves natural language question answering over tabular data. This repository implements two subtasks:

1. **Subtask-1**: Querying a *sample* set of tables (lite version) to retrieve answers.
2. **Subtask-2**: Querying the *full* dataset tables for more complex or large-scale queries.

We leverage:
- **Hugging Face Datasets** for retrieving parquet tables.
- **SQLite** to store tables locally as `.db` files.
- **LangChain** and **OpenAI** LLMs to generate and execute SQL queries.
- **Jupyter Notebooks** for interactive demos and evaluation.

## Repository Structure

```text
├── README.md                     # This documentation file
├── requirements.txt              # Python dependencies
├── scripts/
│   ├── sql-db-loading.py         # Script: download & load tables into SQLite
│   ├── sql-agent.ipynb           # Notebook: LLM-driven SQL agent demo
│   └── evaluation.ipynb          # Notebook: evaluate agent outputs vs. ground truth
└── data/
    └── questions-with-metadata-dataset.xlsx  # Excel: ground-truth questions & metadata
```

## Requirements

- Python **3.8+**
- Internet access (to fetch Hugging Face datasets and call OpenAI API)
- An **OpenAI API key** set as environment variable `OPENAI_API_KEY`

All other Python libraries are listed in `requirements.txt`.

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/<your-org>/semeval-task8.git
cd semeval-task8

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\\Scripts\\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## Data Preparation

1. **Download** the ground-truth Excel sheet (`questions-with-metadata-dataset.xlsx`) from the SemEval Task 8 website or repository.
2. **Create** a `data/` directory in the project root if it does not exist:
   ```bash
   mkdir -p data
   ```
3. **Place** the Excel file under `data/`:
   ```bash
   mv /path/to/questions-with-metadata-dataset.xlsx data/
   ```

## Database Generation

Run the loader script to fetch parquet tables from Hugging Face and store them in two SQLite databases:

```bash
python scripts/sql-db-loading.py
```

- `semeval-lite.db`: Contains **sample** tables (for Subtask 1).
- `semeval.db`     : Contains **full** tables (for Subtask 2).

The script handles column renaming for problematic names and skips missing files.

## Running the SQL Agent

1. **Set** your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
   ```
2. **Launch** the Jupyter notebook:
   ```bash
   jupyter notebook scripts/sql-agent.ipynb
   ```
3. **Walk through** the cells:
   - Connect to the appropriate SQLite database.
   - Load metadata questions.
   - Initialize a LangChain agent to translate questions into SQL.
   - Execute SQL against the DB and collect answers.
   - Save results to `gpt_4o_semeval_results.xlsx`.

### Example Agent Snippet

```python
from langchain import SQLDatabase, SQLDatabaseChain
from langchain.llms import OpenAI
import sqlite3

# Connect to SQLite
conn = sqlite3.connect('semeval.db')
llm = OpenAI(temperature=0)
db = SQLDatabase(engine=conn)
chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Ask a question
question = "What is the average flight delay for airports with more than 1000 flights?"
response = chain.run(question)
print(response)
```

## Evaluation

Evaluate the agent’s output against ground truth:

```bash
jupyter notebook scripts/evaluation.ipynb
```

The evaluation notebook:
- Loads `gpt_4o_semeval_results.xlsx`.
- Compares generated answers to expected answers from `questions-with-metadata-dataset.xlsx`.
- Computes accuracy and error analyses for Subtask 1 and Subtask 2.

## Scripts Details

- **sql-db-loading.py**
  - Loads metadata Excel.
  - Iterates over table names, fetches `sample` and `all` parquet files via `hf://` paths.
  - Renames problematic columns and writes tables to SQLite.

- **sql-agent.ipynb**
  - Sample-driven demonstration of how to set up and run the LLM-to-SQL chain.

- **evaluation.ipynb**
  - Automated metrics calculation and visualization of results.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-change`).
3. Commit your changes and push (`git push origin feature/my-change`).
4. Open a pull request describing your changes.

---

<sup>Created for SemEval-2025 Task 8 | Maintainer: [Your Name] | License: MIT</sup>
