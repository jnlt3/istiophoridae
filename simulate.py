from ga import GaParams, GeneticAlgorithm, Dna, Constraints
import random

from matplotlib import pyplot as plt


def rate(dna: Dna) -> float:
    optimal_a: list[float] = [50, 30, 40, 35, 45, 90, 80, 20, 50, 50, 60]

    def elo(x: list[float], y: list[int]) -> float:
        return 3000 - sum([(x - y) ** 2 / 100 for (x, y) in zip(x, y)])

    return elo(optimal_a, dna.values)


def fight(a: Dna, b: Dna) -> Dna:
    return a if random.random() < 1 / (1 + 10 ** ((rate(b) - rate(a)) / 400)) else b


def fight_8(a: Dna, b: Dna) -> Dna:
    wins = 0
    losses = 0
    for _ in range(8):
        if fight(a, b) is a:
            wins += 1
        else:
            losses += 1
    if wins > losses:
        return a
    else:
        return b


def rate_ga(ga_params: GaParams, iter: int = 128, trials: int = 128) -> float:
    sum_rating: float = 0

    density_estimation_ratings: list[float] = []
    population_mean_ratings: list[float] = []

    avg_ratings: list[float] = []
    max_ratings: list[float] = []
    min_ratings: list[float] = []

    for _ in range(trials):
        ga: GeneticAlgorithm = GeneticAlgorithm(ga_params)
        for _ in range(iter):
            ga.eliminate(fight_8)
            ga.gen_population()
            density_estimation_ratings.append(rate(ga.highest_density()))
            population_mean_ratings.append(rate(ga.population_mean()))
            ratings = [rate(dna) for dna in ga.population]
            avg_rating: float = sum(ratings) / len(ga.population)
            avg_ratings.append(avg_rating)
            max_ratings.append(max(ratings))
            min_ratings.append(min(ratings))

        estimated: Dna = ga.population_mean()
        rating: float = rate(estimated)
        sum_rating += rating

    times: list[int] = [x for x in range(iter)]
    # for i in range(len(estimateds[0])):
    plt.plot(times, density_estimation_ratings, label="Density Selection")
    plt.plot(times, population_mean_ratings, label="Arithmetic Mean")
    plt.plot(times, avg_ratings, label="Population Elo average ")
    plt.plot(times, max_ratings, label="Population Max")
    plt.plot(times, min_ratings, label="Population Min")
    plt.xlabel("Generation")
    plt.ylabel("Simulated Elo")
    # plt.yticks(1)
    plt.legend()
    plt.show()
    return sum_rating / trials


def main():
    population: int = 1024
    iter: int = 128
    params: GaParams = GaParams(
        Constraints(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200],
            [True, True, True, True, True, True, True, True, True, True, True],
        ),
        population,
        0.05,
    )
    print(f"rating: {rate_ga(params, iter, 1)}")


if __name__ == "__main__":
    main()
