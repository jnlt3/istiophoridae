import argparse
import json
import sys
from typing import Callable

from cutechess import CutechessMan
from ga import Dna, GaParams, GeneticAlgorithm
from params import from_params, get_params


def create_uci(names: list[str], params: list[int]) -> list[str]:
    options: list[str] = []
    for name, param in zip(names, params):
        options.append(f"option.{name}={param}")
    return options


def cutechess_from_config(config_path: str) -> CutechessMan:
    with open(config_path) as config_file:
        config = json.load(config_file)
    return CutechessMan(**config)


def create_select(
    cutechess: CutechessMan, names: list[str]
) -> Callable[[Dna, Dna], Dna]:
    def select(dna_a: Dna, dna_b: Dna) -> Dna:
        uci_a = create_uci(names, dna_a.values)
        uci_b = create_uci(names, dna_b.values)
        res = cutechess.run(uci_a, uci_b)
        if res is None:
            print("Error encountered with cutechess", file=sys.stderr)
            return dna_a
        if res.wins > res.losses:
            return dna_a
        else:
            return dna_b

    return select


def run(ga: GeneticAlgorithm, select: Callable[[Dna, Dna], Dna]) -> Dna | None:
    population_mean = None
    try:
        while True:
            ga.eliminate(select)
            ga.gen_population()
            population_mean = ga.population_mean()
    finally:
        return population_mean


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tune", type=str, default="config.json", help="Config JSON file"
    )
    parser.add_argument("--engine", type=str, help="Engine executable path")
    parser.add_argument("--book", type=str, help="Book path (epd)")
    parser.add_argument(
        "--population-size",
        type=int,
        default=128,
        help="Population size of Genetic Algorithm",
    )
    parser.add_argument(
        "--mutation-rate",
        type=float,
        default=0.05,
        help="Mutation rate per member of population is proportional to this number",
    )
    parser.add_argument(
        "--cutechess",
        type=str,
        default="./config/stc.json",
        help="cutechess-cli options",
    )
    parser.add_argument(
        "--threads", type=int, default=1, help="Maximum amount of threads to use"
    )
    args = parser.parse_args()

    params = get_params()
    constraints, names = from_params(params)

    with open(args.cutechess) as cutechess:
        cutechess_params = json.load(cutechess)
    cutechess = CutechessMan(**cutechess_params, engine=args.engine, book=args.book)
    select = create_select(cutechess, names)

    ga_params = GaParams(
        constraints, args.population_size, args.mutation_rate
    )
    ga = GeneticAlgorithm(ga_params)

    print(run(ga, select))


if __name__ == "__main__":
    main()
