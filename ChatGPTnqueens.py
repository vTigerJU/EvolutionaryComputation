import random
import time

# --- basic helpers ---
def random_solution(n):
    sol = list(range(n))
    random.shuffle(sol)
    return sol

def conflicts(sol):
    n = len(sol)
    count = 0
    for i in range(n):
        for j in range(i+1, n):
            if abs(i - j) == abs(sol[i] - sol[j]):  # diagonal conflicts
                count += 1
    return count

def fitness(sol):
    return -conflicts(sol)  # fewer conflicts = better (more positive)

def mutate(sol):
    i, j = random.sample(range(len(sol)), 2)
    sol[i], sol[j] = sol[j], sol[i]

# --- simple evolutionary solver ---
def solve_nqueens(n, generations=300, population_size=50, verbose=True):
    start = time.time()
    population = [random_solution(n) for _ in range(population_size)]

    for gen in range(generations):
        # sort by fitness (best first)
        population.sort(key=fitness, reverse=True)
        best = population[0]
        if conflicts(best) == 0:
            elapsed = time.time() - start
            if verbose:
                print(f"Lösning hittad på generation {gen}")
                print(best)
            return {
                "n": n,
                "gen": gen,
                "time_s": elapsed,
                "solution": best,
                "found": True,
            }

        # keep top 10, then fill with mutated copies of top 20
        new_pop = population[:10]
        while len(new_pop) < population_size:
            parent = random.choice(population[:20])[:]  # copy
            mutate(parent)
            new_pop.append(parent)
        population = new_pop

    # no perfect solution found within budget; return best seen
    elapsed = time.time() - start
    best = sorted(population, key=fitness, reverse=True)[0]
    if verbose:
        print("Ingen perfekt lösning inom generationsbudgeten.")
        print(best, "conflicts:", conflicts(best))
    return {
        "n": n,
        "gen": generations,
        "time_s": elapsed,
        "solution": best,
        "found": conflicts(best) == 0,
    }

# --- small experiment runner (prints a compact table) ---
def run_experiments():
    sizes = [3, 8, 50]   # adjust as you like
    runs = 10

    print("n\tSuccess\tAvgGen\tAvgTime(s)")
    for n in sizes:
        successes = 0
        total_gen = 0.0
        total_time = 0.0

        for _ in range(runs):
            result = solve_nqueens(n, verbose=False)  # quiet during batch
            if result["found"]:
                successes += 1
                total_gen += result["gen"]
                total_time += result["time_s"]

        avg_gen = (total_gen / successes) if successes else 0
        avg_time = (total_time / successes) if successes else 0
        print(f"{n}\t{successes}/{runs}\t{avg_gen:.1f}\t{avg_time:.4f}")

if __name__ == "__main__":
    # Option A: single run (simple)
    # r = solve_nqueens(8)  # try 8, 20, 50, ...
    # print(r)

    # Option B: batch experiments (uncomment to use)
    run_experiments()
