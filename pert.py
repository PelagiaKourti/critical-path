#PERT: Program evaluation and review technique

import numpy as np 
from cpm import cpm
import matplotlib.pyplot as plt

pert_tasks = {
    "A": (3, 4, 6, []),
    "B": (2, 3, 5, []),
    "C": (4, 5, 8, ["A", "B"]),
    "D": (4, 5, 7, ["C"]),
    "E": (5, 6, 9, ["C"]),
    "F": (2, 3, 5, ["D", "E"]),
    "G": (3, 4, 8, ["B"]),
    "H": (1, 1, 2, ["F", "G"]),
}

def scenario(pert_tasks):   #scenario of a possible case
    tasks = {}
    for name in pert_tasks:
        o, m, p, preds = pert_tasks[name]
        alpha = 1 + 4*(m - o)/(p - o)
        beta = 1 + 4*(p - m)/(p - o)
        duration =  o + (p - o)*np.random.beta(alpha, beta)  #Beta-PERT distribution
        tasks[name] = (duration, preds)
    return tasks

#for a random case:
s = scenario(pert_tasks)
print(s)
print(cpm(s)["critical"])

#we run it 10,000 times, to see the distribution of the durations
N = 10000
durations = []
critical_count = {name: 0 for name in pert_tasks}  #counts in how many scenarios each task was critical

for n in range(N):
    n_scenario = scenario(pert_tasks)  #each current scenario
    n_results = cpm(n_scenario)         #results of this scenario
    durations.append(n_results["project_end"])    # total project duration in this scenario
    for task in n_results["critical"]:          #for task in this current critical path
        critical_count[task] += 1

mean_duration = np.mean(durations)      #mean value of all durations of the N cases
p = 0
for d in durations:
    if d <= 20:
        p+=1    #to see then how many cases are completed within to 20 days

percentage = (p / N)*100       #how many cases are completed within 20 days
percentile_dur = np.percentile(durations, 90)  #the 90th percentile duration


def hist(data, p90, cpm_dur):   #histogram
    plt.hist(data, bins=50)  #bins = how many bars
    plt.axvline(p90, color="red", linestyle="--", label = "Percentile duration by 90%")
    plt.axvline(cpm_dur, color="green", label = f"CPM ({cpm_dur:.0f} days)")
    plt.legend()
    plt.xlabel("Project duration (days)")
    plt.ylabel("Number of scenarios")
    plt.title(f"Monte Carlo: {N} scenarios")
    plt.show()


def most_likely(pert_tasks):  #the cpm duration
    tasks = {}
    for name in pert_tasks:
        o, m, p, preds = pert_tasks[name]
        tasks[name] = (m, preds)        #m is the duration
    
    results = cpm(tasks)
    return results["project_end"]


print("Mean duration:", mean_duration)
print("%", " of cases project ends in <=20 days:", f"{percentage:.1f}", "%")
for task in pert_tasks:
    print(task, critical_count[task] / N)
print("Percentile duration by 90%:", percentile_dur)


cpm_duration = most_likely(pert_tasks)
print("CPM duration: ", cpm_duration)

hist(data = durations, p90 = percentile_dur, cpm_dur = cpm_duration)