import json
from pathlib import Path
from typing import List, Dict, Optional

from models.athlete import Athlete
from models.result import Result
from utils.utils import parse_date, is_lower_better, compute_improvement


class DataStore:
    def __init__(self, path: str = "data/database.json"):
        self.path = Path(path)
        self.data = {"athletes": [], "results": []}
        self.load()

    def load(self):
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.save()
        try:
            with open(self.path, "r", encoding="utf8") as f:
                self.data = json.load(f)
        except Exception:
            self.data = {"athletes": [], "results": []}
            self.save()

    def save(self):
        with open(self.path, "w", encoding="utf8") as f:
            json.dump(self.data, f, indent=2)


class AthleteManager:
    def __init__(self, store: DataStore):
        self.store = store

    def add_athlete(self, athlete: Athlete):
        if any(a["name"] == athlete.name for a in self.store.data["athletes"]):
            raise ValueError("Athlete already exists")
        self.store.data["athletes"].append(athlete.to_dict())
        self.store.save()

    def list_athletes(self) -> List[Athlete]:
        return [Athlete.from_dict(d) for d in self.store.data["athletes"]]

    def get(self, name: str) -> Optional[Athlete]:
        for d in self.store.data["athletes"]:
            if d["name"] == name:
                return Athlete.from_dict(d)
        return None


class ResultManager:
    def __init__(self, store: DataStore):
        self.store = store

    def add_result(self, result: Result):
        # validate date
        parse_date(result.date)
        self.store.data["results"].append(result.to_dict())
        self.store.save()

    def results_for_athlete_test(self, athlete_name: str, test_name: str) -> List[Result]:
        rs = [Result.from_dict(d) for d in self.store.data["results"] if d["athlete_name"] == athlete_name and d["test_name"] == test_name]
        rs.sort(key=lambda r: r.date_obj())
        return rs

    def latest_results_for_test(self, test_name: str) -> Dict[str, Result]:
        # return latest result per athlete for given test
        res = [Result.from_dict(d) for d in self.store.data["results"] if d["test_name"] == test_name]
        latest = {}
        for r in sorted(res, key=lambda x: x.date_obj()):
            latest[r.athlete_name] = r
        return latest

    def all_results_for_athlete(self, athlete_name: str) -> List[Result]:
        rs = [Result.from_dict(d) for d in self.store.data["results"] if d["athlete_name"] == athlete_name]
        rs.sort(key=lambda r: (r.test_name, r.date_obj()))
        return rs


class RankingManager:
    def __init__(self, result_manager: ResultManager):
        self.rm = result_manager

    def rankings_for_test(self, test_name: str) -> List[Result]:
        latest = list(self.rm.latest_results_for_test(test_name).values())
        lower_better = is_lower_better(test_name)
        sorted_list = sorted(latest, key=lambda r: r.score, reverse=(not lower_better))
        return sorted_list

    def compare_last_two(self, athlete_name: str, test_name: str):
        rs = self.rm.results_for_athlete_test(athlete_name, test_name)
        if len(rs) < 1:
            return []
        if len(rs) == 1:
            return [rs[0], None, None]
        prev, curr = rs[-2], rs[-1]
        diff, pct, status = compute_improvement(prev.score, curr.score, is_lower_better(test_name))
        return [prev, curr, {"diff": diff, "percent": pct, "status": status}]
