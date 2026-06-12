import argparse
from pathlib import Path
from rich.table import Table
from rich.console import Console

from models.athlete import Athlete
from models.result import Result
from utils.managers import DataStore, AthleteManager, ResultManager, RankingManager
from utils.utils import parse_date, is_lower_better, compute_improvement

console = Console()


def cmd_add_athlete(args, store):
    am = AthleteManager(store)
    try:
        a = Athlete(name=args.name, age=int(args.age), position=args.position, team=(args.team or ""))
        am.add_athlete(a)
        console.print(f"Added athlete: {args.name}")
    except Exception as e:
        console.print(f"Error: {e}")


def cmd_list_athletes(args, store):
    am = AthleteManager(store)
    athletes = am.list_athletes()
    table = Table(title="Athletes")
    table.add_column("Name")
    table.add_column("Age")
    table.add_column("Position")
    table.add_column("Team")
    for a in athletes:
        table.add_row(a.name, str(a.age), a.position, a.team)
    console.print(table)


def cmd_add_result(args, store):
    rm = ResultManager(store)
    try:
        # validate date
        parse_date(args.date)
        r = Result(athlete_name=args.name, test_name=args.test, score=float(args.score), date=args.date)
        rm.add_result(r)
        console.print(f"Added result for {args.name} - {args.test} on {args.date}")
    except Exception as e:
        console.print(f"Error: {e}")


def cmd_compare(args, store):
    rm = ResultManager(store)
    rs = rm.results_for_athlete_test(args.name, args.test)
    if not rs:
        console.print("No results found")
        return
    table = Table(title=f"History: {args.name} - {args.test}")
    table.add_column("Date")
    table.add_column("Score")
    for r in rs:
        table.add_row(r.date, str(r.score))
    console.print(table)

    if len(rs) >= 2:
        prev, curr = rs[-2], rs[-1]
        diff, pct, status = compute_improvement(prev.score, curr.score, is_lower_better(args.test))
        console.print(f"Previous: {prev.score} on {prev.date}")
        console.print(f"Latest:   {curr.score} on {curr.date}")
        console.print(f"Change: {diff:.3f} ({pct:.2f}%) -> {status}")
    else:
        console.print("Not enough data to compare (need 2 results)")


def cmd_rankings(args, store):
    rm = ResultManager(store)
    rk = RankingManager(rm)
    ranked = rk.rankings_for_test(args.test)
    if not ranked:
        console.print("No results for this test")
        return
    table = Table(title=f"Rankings: {args.test}")
    table.add_column("Rank", justify="right")
    table.add_column("Athlete")
    table.add_column("Score")
    lower_better = is_lower_better(args.test)
    metric = "(lower is better)" if lower_better else "(higher is better)"
    table.title = table.title + " " + metric
    for i, r in enumerate(ranked, start=1):
        table.add_row(str(i), r.athlete_name, str(r.score))
    console.print(table)


def cmd_athlete_report(args, store):
    rm = ResultManager(store)
    am = AthleteManager(store)
    athlete = am.get(args.name)
    if not athlete:
        console.print("Athlete not found")
        return
    console.print(f"Report for {athlete.name} - {athlete.position} (Team: {athlete.team})")
    allr = rm.all_results_for_athlete(athlete.name)
    if not allr:
        console.print("No results")
        return
    # Group by test
    tests = {}
    for r in allr:
        tests.setdefault(r.test_name, []).append(r)

    for test_name, results in tests.items():
        results.sort(key=lambda r: r.date_obj())
        table = Table(title=f"{test_name}")
        table.add_column("Date")
        table.add_column("Score")
        for r in results:
            table.add_row(r.date, str(r.score))
        console.print(table)
        if len(results) >= 2:
            first, last = results[0], results[-1]
            diff, pct, status = compute_improvement(first.score, last.score, is_lower_better(test_name))
            console.print(f"From {first.date} -> {last.date}: Change {diff:.3f} ({pct:.2f}%) -> {status}")


def build_parser():
    epilog = '''Examples:
  python main.py add-athlete --name "Leon" --age 22 --position "Wing" --team "Academy"
  python main.py list-athletes
  python main.py add-result --name "Leon" --test "40m Sprint" --score 5.2 --date 2026-06-09
  python main.py compare --name "Leon" --test "40m Sprint"
  python main.py rankings --test "100m Sprint"
  python main.py athlete-report --name "Leon"
'''
    p = argparse.ArgumentParser(description="Athlete Performance CLI", epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("add-athlete", help="Add an athlete")
    a.add_argument("--name", required=True)
    a.add_argument("--age", required=True)
    a.add_argument("--position", required=True)
    a.add_argument("--team", required=False)
    a.set_defaults(func=cmd_add_athlete)

    la = sub.add_parser("list-athletes", help="List athletes")
    la.set_defaults(func=cmd_list_athletes)

    ar = sub.add_parser("add-result", help="Add a test result")
    ar.add_argument("--name", required=True)
    ar.add_argument("--test", required=True)
    ar.add_argument("--score", required=True)
    ar.add_argument("--date", required=True, help="YYYY-MM-DD")
    ar.set_defaults(func=cmd_add_result)

    c = sub.add_parser("compare", help="Compare historical results for an athlete/test")
    c.add_argument("--name", required=True)
    c.add_argument("--test", required=True)
    c.set_defaults(func=cmd_compare)

    r = sub.add_parser("rankings", aliases=["rank"], help="Rankings for a test")
    r.add_argument("--test", required=True)
    r.set_defaults(func=cmd_rankings)

    rep = sub.add_parser("athlete-report", aliases=["report"], help="Athlete detailed report")
    rep.add_argument("--name", required=True)
    rep.set_defaults(func=cmd_athlete_report)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    store = DataStore()
    if hasattr(args, "func") and callable(args.func):
        args.func(args, store)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
