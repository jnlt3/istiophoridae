import random
from dataclasses import dataclass
from typing import Callable

NAMES: list[str] = []


@dataclass
class Dna:
    values: list[int]


@dataclass
class Constraints:
    min: list[int]
    max: list[int]
    ordinal: list[bool]

    def __post_init__(self) -> None:
        self.range = [max - min for min, max in zip(self.min, self.max)]

    def random_dna(self) -> Dna:
        constraint_iterator = zip(self.min, self.max)
        return Dna([random.randint(min, max) for (min, max) in constraint_iterator])

    def _new_value(self, dna: Dna, index: int) -> None:
        if self.ordinal[index]:
            delta = self.range[index] / 5
            new_value = random.normalvariate(dna.values[index], delta)
            dna.values[index] = min(
                max(round(new_value), self.min[index]), self.max[index]
            )
        else:
            dna.values[index] = random.randint(self.min[index], self.max[index])

    def mutate(self, dna: Dna, mutation_chance: float) -> None:
        for index in range(len(dna.values)):
            if random.random() < mutation_chance / len(dna.values):
                self._new_value(dna, index)

    def diff(self, a: int, b: int, range: int, ordinal: bool) -> float:
        if ordinal:
            return (a - b) / range
        return 0 if a == b else 1

    def sq_dist(self, a: Dna, b: Dna) -> float:
        return sum(
            self.diff(a, b, r, ordinal) ** 2
            for a, b, r, ordinal in zip(
                a.values, b.values, self.range, self.ordinal
            )
        )


@dataclass
class GaParams:
    constraints: Constraints
    population_size: int
    mutation_rate: float


class GeneticAlgorithm:
    ga_params: GaParams
    population: list[Dna]

    def __init__(self, ga_params: GaParams) -> None:
        assert (
            ga_params.population_size % 4 == 0
        ), "Population size must be divisible by 4"
        self.ga_params = ga_params
        self.population = [
            ga_params.constraints.random_dna() for _ in range(ga_params.population_size)
        ]

    def eliminate(self, select: Callable[[Dna, Dna], Dna]) -> None:
        new_population: list[Dna] = []
        random.shuffle(self.population)
        for i in range(0, len(self.population), 2):
            dna_a = self.population[i]
            dna_b = self.population[i + 1]
            new_population.append(select(dna_a, dna_b))
        self.population = new_population

    def gen_population(self) -> None:
        for i in range(0, len(self.population), 2):
            dna_a = self.population[i]
            dna_b = self.population[i + 1]
            new_dna_a, new_dna_b = self._crossover(dna_a, dna_b)
            self.population.append(new_dna_a)
            self.population.append(new_dna_b)

    def _crossover(self, a: Dna, b: Dna) -> tuple[Dna, Dna]:
        assert len(a.values) == len(b.values)
        switch = [random.random() < 0.1 for _ in range(len(a.values))]

        def zipped() -> zip[tuple[int, int, bool]]:
            return zip(a.values, b.values, switch)

        new_a = Dna([a if switch else b for (a, b, switch) in zipped()])
        new_b = Dna([b if switch else a for (a, b, switch) in zipped()])
        self.ga_params.constraints.mutate(new_a, self.ga_params.mutation_rate)
        self.ga_params.constraints.mutate(new_b, self.ga_params.mutation_rate)
        return new_a, new_b

    def population_mean(self) -> Dna:
        sum = [0] * len(self.ga_params.constraints.min)
        for dna in self.population:
            for i in range(len(sum)):
                sum[i] += dna.values[i]
        for i in range(len(sum)):
            sum[i] //= len(self.population)
        return Dna(sum)
