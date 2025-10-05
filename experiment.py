import nqueens
import nqueensEmilMutation
import json
    
def solve_multiple(n_size, sample_size, population_size, inversion_rate, tag):
    avg_gen = 0
    avg_time_s = 0
    number_failures = 0
    for _ in range(sample_size):
        solution = nqueens.solve(n_size, population_size,inversion_rate)
        try:
            avg_gen += solution.get("gen")
            avg_time_s += solution.get("time_s")
        except:
            number_failures +=1

    if sample_size != number_failures:
        avg_gen = avg_gen/(sample_size - number_failures)
        avg_time_s = avg_time_s/(sample_size - number_failures)

    return {
        "n": n_size,
        "population_size": population_size,
        "avg_gen": round(avg_gen,2),
        "avg_time_s": round(avg_time_s,2),
        "failures": number_failures,
        "inversion_rate": inversion_rate,
        "max_gen": 1000,
        "tag": tag
    }

def population_experiment():
    results = []
    population_size = 50
    for i in range(1,25):
        results.append(solve_multiple(100,25,population_size*i,"pop"))
        results.append(solve_multiple(200,25,population_size*i,"pop"))
    return results

def inversion_rate_experiment():
    results = []
    inversion_rate = 0
    for _ in range(20):
        print(inversion_rate)
        results.append(solve_multiple(100,25,400, inversion_rate,"ir"))
        inversion_rate += 0.05
    return results

def inversion_rate_experiment_narrow():
    results = []
    inversion_rate = 0
    for i in range(6):
        print(inversion_rate)
        n_size = 50
        while n_size <= 250:
            print("n_size", n_size)
            results.append(solve_multiple(n_size,25,400, inversion_rate,"irn"))
            n_size += 50
        inversion_rate += 0.05
    return results

def experiment():
    file_path = "results.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except:
        data = []
    results = []
    #results += population_experiment()
    #results += inversion_rate_experiment()
    results += inversion_rate_experiment_narrow()
    data += results
    with open(file_path, "w") as file:
        file.write("[\n")
        for i, entry in enumerate(data):
            json.dump(entry, file)
            if i < len(data) - 1:
                file.write(",\n")
            else:
                file.write("\n")
        file.write("]")
if __name__ == "__main__":
    experiment()
