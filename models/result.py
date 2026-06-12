from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Result:
    athlete_name: str
    test_name: str
    score: float
    date: str  # ISO date YYYY-MM-DD

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Result(athlete_name=d["athlete_name"], test_name=d["test_name"], score=float(d["score"]), date=d["date"])

    def date_obj(self):
        return datetime.strptime(self.date, "%Y-%m-%d").date()
