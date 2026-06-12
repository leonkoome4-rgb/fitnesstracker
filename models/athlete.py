from dataclasses import dataclass, asdict


@dataclass
class Athlete:
    name: str
    age: int
    position: str
    team: str = ""

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Athlete(name=d["name"], age=int(d["age"]), position=d["position"], team=d.get("team", ""))
