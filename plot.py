import matplotlib.pyplot as plt
import json
import pandas as pd


def plot_rate_narrow(df):
    x = "n"
    y = "avg_time_s"
    ir = "inversion_rate"
    df = df[df["population_size"] == 400]
    df = df[df["tag"]=="irn"]
    df = df.sort_values(by="n")
    df0 = df[df[ir]== 0]
    df05 = df[df[ir]== 0.05]
    df1 = df[df[ir]== 0.1]
    df15 = df[df[ir]== 0.15]
    df2 = df[df[ir]== 0.2]
    df25 = df[df[ir] == 0.25]
    df3 = df[df[ir] == 0.3]

    plt.plot(df0[x],df0[y],label="0.00")
    plt.plot(df05[x],df05[y],label="0.05")
    plt.plot(df1[x],df1[y],label="0.10")
    plt.plot(df15[x],df15[y],label="0.15")
    plt.plot(df2[x],df2[y],label="0.20")
    plt.plot(df25[x],df25[y],label="0.25")
    plt.plot(df3[x],df3[y],label="0.30")
    plt.xlabel("n-size")
    plt.ylabel("Average Time (s)")
    plt.title("Inversion Rate across n-size")
    plt.legend()
    plt.show()

def plot_rate(df):
    df = df[df["tag"]=="ir"]
    df100 = df[df['n'] == 100]
    dfIR = df100[df100["population_size"]==400]
    dfIR = dfIR.sort_values(by="inversion_rate")
    
    figure, axis = plt.subplots(1, 2)
    axis[0].set_title("n-size 100, Population 400")
    axis[0].plot(dfIR['inversion_rate'], dfIR['avg_time_s'])
    axis[0].set_xlabel("Inversion Rate")
    axis[0].set_ylabel("Average time (s)")
    axis[1].plot(dfIR['inversion_rate'], dfIR['avg_gen'])
    axis[1].set_xlabel("Inversion Rate")
    axis[1].set_ylabel("Average generation")

    plt.show()

def plot_pop_test(df):
    df = df[df["tag"]=="pop"]
    df100 = df[df['n'] == 100]
    df200 = df[df['n'] == 200]
    df100 = df100.sort_values(by="population_size")
    df200 = df200.sort_values(by="population_size")
    figure, axis = plt.subplots(1, 2)
    axis[0].plot(df100["population_size"],df100["avg_time_s"])
    axis[0].set_xlabel("Population Size")
    axis[0].set_ylabel("Average time (s)")
    axis[0].set_title("n-size 100")
    axis[1].set_ylabel("Average time (s)")
    axis[1].set_xlabel("Population Size")
    axis[1].set_title("n-size 200")
    axis[1].plot(df200["population_size"],df200["avg_time_s"])
    plt.show()

def plot_n_test(df):
    n = "n"
    t = "avg_time_s"
    df = df[df["tag"]=="ntest"]
    df0 = df[df['inversion_rate'] == 0]
    df1 = df[df["inversion_rate"]== 0.1]
    plt.plot(df0[n],df0[t],label="0")
    plt.plot(df1[n],df1[t],label="1.0")
    plt.xlabel("n-size")
    plt.ylabel("Average Time (s)")
    plt.legend()
    plt.show()

def plot_results(results):
    df = pd.DataFrame(results)
    plot_n_test(df)
    plot_rate_narrow(df)
    plot_pop_test(df)
    plot_rate(df)
   

if __name__ == "__main__":
    f = open("results.json", 'r')
    results = json.load(f)
    plot_results(results)