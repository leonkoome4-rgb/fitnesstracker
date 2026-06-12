**Athlete Performance CLI**
===========================

**Purpose**
- A lightweight sports performance analytics CLI that tracks athletes, training tests, and test results over time. It's designed for rugby, football academies, and athletics programs that need to record sessions and measure progress.

**Key Features**
- Athlete management (add / list)
- Time-series test results (dateed results)
- Historical comparison per athlete/test
- Rankings per test (direction inferred from test name)
- Athlete performance reports grouped by test

**Project layout**
- `main.py` — CLI entrypoint (argparse + rich tables)
- `models/` — `athlete.py`, `result.py` dataclasses
- `utils/` — `managers.py` (DataStore, managers), `utils.py` (helpers)
- `data/database.json` — single-file JSON datastore
- `tests/` — pytest test suite
- `requirements.txt` — external dependencies (`rich`, `pytest`)

Requirements
- Python 3.10+ recommended
- Uses `rich` for pretty tables and `pytest` for tests

Installation (recommended: virtual environment)
```bash
cd /Users/leonkoome4gmail.com/python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Quick help
```bash
python main.py --help
```

Commands (summary & examples)
- Add an athlete
	```bash
	python main.py add-athlete --name "Leon" --age 22 --position "Wing" --team "Academy"
	```
- List athletes
	```bash
	python main.py list-athletes
	```
- Add a test result (date must be `YYYY-MM-DD`)
	```bash
	python main.py add-result --name "Leon" --test "40m Sprint" --score 5.2 --date 2026-06-09
	```
- Compare an athlete's test history
	```bash
	python main.py compare --name "Leon" --test "40m Sprint"
	```
- Rankings for a test (aliases: `rank`)
	```bash
	python main.py rankings --test "100m Sprint"
	# or
	python main.py rank --test "100m Sprint"
	```
- Athlete report (aliases: `report`)
	```bash
	python main.py athlete-report --name "Leon"
	# or
	python main.py report --name "Leon"
	```

Behavior & rules
- Data is persisted to `data/database.json` and saved after every change.
- Date format is strictly `YYYY-MM-DD` (validated by the CLI).
- Rankings use the latest result per athlete for that test. The system infers whether "lower is better" from test name keywords (speed/time keywords such as "sprint", "m", "sec" indicate lower-is-better).

Data format (`data/database.json`)
```json
{
	"athletes": [
		{"name": "Leon", "age": 22, "position": "Wing", "team": "Academy"}
	],
	"results": [
		{"athlete_name": "Leon", "test_name": "40m Sprint", "score": 5.2, "date": "2026-06-09"}
	]
}
```

Programmatic usage (example)
```python
from utils.managers import DataStore, AthleteManager, ResultManager
from models.athlete import Athlete
from models.result import Result

store = DataStore()
am = AthleteManager(store)
rm = ResultManager(store)

am.add_athlete(Athlete("Leon", 22, "Wing", "Academy"))
rm.add_result(Result("Leon", "40m Sprint", 5.2, "2026-06-09"))
```

Testing
```bash
source .venv/bin/activate
python -m pytest -q
```

Extending the project
- Add fields to `Result` (e.g., `session_id`, `notes`) in `models/result.py`, then update serialization and manager methods.
- Tune ranking direction by editing keywords in `utils/utils.py` (`is_lower_better`).
- Add dashboard or CSV export commands in `main.py` using `rich` for formatted output.

Developer notes
- The codebase uses OOP managers (`AthleteManager`, `ResultManager`, `RankingManager`) to separate concerns and keep persistence centralized in `DataStore`.
- CLI uses `argparse` and registers handlers via `set_defaults(func=...)` for clear dispatch.

Questions or next steps
- I can add a `seed.py` to populate sample data, a `Makefile` with common commands, or a `pyproject.toml`/console entry for pipx installation. Tell me which you prefer.

Commands (examples)
-------------------

Activate venv (optional but recommended):

```bash
source .venv/bin/activate
```

- Add an athlete:

```bash
python main.py add-athlete --name "Leon" --age 22 --position "Wing" --team "Academy"
```

- List athletes:

```bash
python main.py list-athletes
```

- Add a test result (date YYYY-MM-DD):

```bash
python main.py add-result --name "Leon" --test "40m Sprint" --score 5.2 --date 2026-06-09
```

- Compare an athlete's test history:

```bash
python main.py compare --name "Leon" --test "40m Sprint"
```

- Rankings for a test (alias: `rank`):

```bash
python main.py rankings --test "100m Sprint"
# or
python main.py rank --test "100m Sprint"
```

- Athlete report (alias: `report`):

```bash
python main.py athlete-report --name "Leon"
# or
python main.py report --name "Leon"
```

Testing:

```bash
python -m pytest -q
```
