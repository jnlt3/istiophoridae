from dataclasses import dataclass

from ga import Constraints


@dataclass
class Param:
    name: str
    min: int
    max: int
    ordinal: bool


def get_params() -> list[Param]:
    return [
        Param("A", 0, 100, True),
        Param("B", 0, 100, True),
        Param("C", 0, 100, True),
    ]


def from_params(params: list[Param]) -> tuple[Constraints, list[str]]:
    names: list[str] = []
    min_: list[int] = []
    max_: list[int] = []
    ordinal: list[bool] = []
    for param in params:
        names.append(param.name)
        min_.append(param.min)
        max_.append(param.max)
        ordinal.append(param.ordinal)
    return Constraints(min_, max_, ordinal), names
