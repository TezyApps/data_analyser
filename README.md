# data-analyser

A command-line tool that loads a `.csv` file into a pandas `DataFrame`, detects missing
(`NaN`) values across columns, automatically fills them with sensible defaults, and
prints a before/after summary plus a quick statistical overview of the cleaned data.

## Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) (used for dependency management and running the tool)

## Install

```bash
uv sync
```

## Usage

Run the tool against any `.csv` file, using either the `data-analyser` or the shorter
`dca` script installed via `pyproject.toml`:

```bash
uv run dca path/to/your-file.csv
```

```bash
uv run data-analyser path/to/your-file.csv
```

### What it does

1. Reads the given `.csv` file into a `DataFrame`.
2. Scans every column for missing values.
3. If missing values are found, fills them using a default per column type:
   - **String columns** → filled with `"undefined"`.
   - **Numeric columns** → filled with `0`.
4. Prints a summary table showing, per column: missing entries before cleanup,
   missing entries after cleanup, and the strategy used.
5. Prints `DataFrame.describe()` for a quick statistical look at the cleaned data.

If no missing values are found, the tool reports that there is nothing to clean.

### Example

```bash
uv run dca test/student-performance.csv
```

Given a CSV with some missing values:

```csv
name,age,department
Alice,29,Engineering
Bob,,Sales
Carol,34,
Dan,41,Engineering
```

```
==============================
🕵️‍♂️ Data Quality Analyser
==============================
 👓 Reading the input file…
 🔎 Checking for Data quality issues...
 🧹 Data Quality Analysis Complete!
 🪄 Found few missing values and replaced with defaults...

==============================
🗒️ Summary of the changes
==============================
      columns  missing_entries  after replacing_strategy
0        name                0      0                  -
1         age                1      0                  0
2  department                1      0          undefined
------------------------------

========================================
📊 Some Interesting facts about your data
========================================

             age
count   4.000000
mean   26.000000
...
------------------------------
```

## Project layout

```
src/data_analyser/
├── __init__.py        # CLI entry point (main)
├── file_reader/        # Reads a .csv path from argv and loads it into a DataFrame
├── cleanser/            # Detects and fills missing values, tracks a before/after summary
└── utils/                # Console output helpers (header/footer formatting)
```

## Current scope (MVP)

- Missing-value detection and auto-fill for both string and numeric columns.
- Fixed default fill strategy (`"undefined"` / `0`) — not yet configurable per column.

See [JOURNEY.md](./JOURNEY.md) for the design decisions, trade-offs, and lessons behind
this implementation.

## Running tests

```bash
uv run pytest -q
```

## License

[MIT](./LICENSE)
