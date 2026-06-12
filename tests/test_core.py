import json
from pathlib import Path

from utils.managers import DataStore, AthleteManager, ResultManager, RankingManager
from models.athlete import Athlete
from models.result import Result


def test_athlete_creation(tmp_path):
    db = tmp_path / "db.json"
    store = DataStore(str(db))
    am = AthleteManager(store)
    a = Athlete(name="Test", age=20, position="FW", team="A")
    am.add_athlete(a)
    assert am.get("Test") is not None


def test_result_storage_and_retrieval(tmp_path):
    db = tmp_path / "db.json"
    store = DataStore(str(db))
    rm = ResultManager(store)
    r = Result(athlete_name="Test", test_name="40m Sprint", score=5.2, date="2026-06-09")
    rm.add_result(r)
    res = rm.results_for_athlete_test("Test", "40m Sprint")
    assert len(res) == 1
    assert abs(res[0].score - 5.2) < 1e-6


def test_ranking_logic(tmp_path):
    db = tmp_path / "db.json"
    store = DataStore(str(db))
    rm = ResultManager(store)
    # speed test (lower better)
    rm.add_result(Result("A", "40m Sprint", 5.0, "2026-06-01"))
    rm.add_result(Result("B", "40m Sprint", 4.8, "2026-06-01"))
    rk = RankingManager(rm)
    ranked = rk.rankings_for_test("40m Sprint")
    assert ranked[0].athlete_name == "B"
    # strength (higher better)
    rm.add_result(Result("A", "Bench Press", 100, "2026-06-01"))
    rm.add_result(Result("B", "Bench Press", 120, "2026-06-01"))
    ranked_s = rk.rankings_for_test("Bench Press")
    assert ranked_s[0].athlete_name == "B"


def test_improvement_calc(tmp_path):
    db = tmp_path / "db.json"
    store = DataStore(str(db))
    rm = ResultManager(store)
    rm.add_result(Result("X", "40m Sprint", 5.2, "2026-06-01"))
    rm.add_result(Result("X", "40m Sprint", 5.0, "2026-07-01"))
    rk = RankingManager(rm)
    prev, curr, stats = rk.compare_last_two("X", "40m Sprint")
    assert stats["status"] == "Improved"
