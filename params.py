from dataclasses import dataclass

from ga import Constraints


@dataclass
class Param:
    name: str
    min: int
    max: int
    ordinal: bool


def get_params() -> list[Param]:
    params: list[Param] = []
    params.append(Param("A", 0, 100, True))
    params.append(Param("B", 0, 100, True))
    params.append(Param("C", 0, 100, True))
    return params


def from_params(params: list[Param]) -> tuple[Constraints, list[str]]:
    name: list[str] = []
    min: list[int] = []
    max: list[int] = []
    ordinal: list[bool] = []
    for param in params:
        name.append(param.name)
        min.append(param.min)
        max.append(param.max)
        ordinal.append(param.ordinal)
    return Constraints(min, max, ordinal), name
