import experiment as ex

#Group 11, Viktor Tiger, Emil Anderö, Axel Lindh, Khishigdorj Batzorig

#To plot the results run "plot.py", Requires pandas and matplotlib

def demo():
    """Prints individual results and a summation from 5 test runs"""
    print("Swap Only")
    print(ex.solve_multiple(200,5,400,0,0,"SwapOnly"))
    print("Inversion and swap")
    print(ex.solve_multiple(200,5,400,0.1,0,"InversionSwap"))
    print("Crossover")
    print(ex.solve_multiple(60,5,400,0,0.1,"Crossover"))

def main():
    #Recommendation is to only run "demo" to test out the Evolutionary algorithm
    demo()
    #Note! running experiment reruns all experiments
    #This takes over an hour
    ex.experiment()

if __name__ == "__main__":
    main()