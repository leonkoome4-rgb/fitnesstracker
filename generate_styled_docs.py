from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

doc = SimpleDocTemplate(
    "athlete_cli_styled_documentation.pdf",
    rightMargin=30,
    leftMargin=30,
    topMargin=30,
    bottomMargin=30
)

styles = getSampleStyleSheet()
content = []

# -----------------------------
# HELPERS
# -----------------------------
def section(title):
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"<b>{title}</b>", styles["Heading1"]))
    content.append(Spacer(1, 6))

def text_block(text):
    content.append(Paragraph(text.replace("\n", "<br/>"), styles["BodyText"]))
    content.append(Spacer(1, 10))

def add_table(data):
    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    content.append(table)
    content.append(Spacer(1, 15))


# -----------------------------
# TITLE
# -----------------------------
content.append(Paragraph(
    "Athlete Performance CLI — Technical Documentation",
    styles["Title"]
))
content.append(Spacer(1, 20))

# -----------------------------
# OVERVIEW
# -----------------------------
section("1. Overview")
text_block("""
This system is a CLI tool for tracking athlete performance, storing results,
and generating analytics such as rankings and improvement comparisons.
Data persists in a JSON database.
""")

# -----------------------------
# SETUP
# -----------------------------
section("2. Setup Instructions")
text_block("""
Create environment:
python3 -m venv venv

Activate:
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run CLI:
python main.py --help
""")

# -----------------------------
# COMMAND TABLE
# -----------------------------
section("3. CLI Commands Summary")

add_table([
    ["Command", "Description"],
    ["add-athlete", "Add a new athlete"],
    ["list-athletes", "Show all athletes"],
    ["add-result", "Add performance test result"],
    ["compare", "Compare historical performance"],
    ["rank / rankings", "Rank athletes by test"],
    ["report / athlete-report", "Full athlete analytics report"]
])

# -----------------------------
# ADD ATHLETE
# -----------------------------
section("4. Add Athlete Command")
text_block("""
python main.py add-athlete --name "albet biron " --age 21 --position "Runner" --team "Alpha"

Rules:
- Name must be unique
- Stored instantly in database.json
""")

# -----------------------------
# ADD RESULT
# -----------------------------
section("5. Add Result Command")
text_block("""
python main.py add-result --name "John Doe" --test "100m Sprint" --score 10.52 --date 2026-06-09

Rules:
- Date format: YYYY-MM-DD
- Stored under athlete record
- Score must be numeric
""")

# -----------------------------
# RANKINGS TABLE
# -----------------------------
section("6. Ranking Logic")

add_table(['python main.py rank --test "100m Sprint"       
    ["Rule", "Behavior"],
    ["Latest result", "Only most recent score is used"],
    ["Direction", "Auto-detected (lower or higher is better)"],
    ["Output", "Sorted best → worst athletes"]
])

# -----------------------------
# COMPARE
# -----------------------------    
section("7. Performance Comparison")
text_block("""
Compares historical results for a specific athlete + test.

Output includes:
- Previous score
- Latest score
- Absolute difference
- Percentage change
- Status (Improved / Declined / No change)
""")

# -----------------------------
# DATA MODEL
# -----------------------------
section("8. Data Structure")

add_table([
    ["Entity", "Fields"],
    ["Athlete", "name, age, position, team, results[]"],
    ["Result", "test, score, date"]
])

# -----------------------------
# CODE USAGE
# -----------------------------
section("9. Programmatic Usage Example")
text_block("""
from managers import DataStore, Manager

store = DataStore("database.json")
manager = Manager(store)

manager.add_athlete("John Doe", 21, "Runner", "Alpha")
manager.add_result("John Doe", "100m Sprint", 10.52, "2026-06-09")
""")

# -----------------------------
# FUTURE IMPROVEMENTS
# -----------------------------
section("10. Suggested Improvements")

text_block("""
- Add session tracking (session_id)
- Add notes per result
- Export CSV / Excel reports
- Add REST API layer
- Build web dashboard
- Convert CLI to Typer for scalability
""")

# -----------------------------
# BUILD PDF
# -----------------------------
doc.build(content)

print("Styled PDF generated: athlete_cli_styled_documentation.pdf")