Athlete Performance CLI
======================

Mini sports analytics CLI for tracking athlete performance over time.

Commands:
- `add-athlete` - add an athlete
- `list-athletes` - list athletes
- `add-result` - add a test result with date
- `compare` - compare historical results for an athlete & test
- `rankings` - rankings for a test
- `athlete-report` - detailed athlete report

Data stored in `data/database.json`.

Install:

```bash
python -m pip install -r requirements.txt
```

Run:

```bash
python main.py --help
```

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
