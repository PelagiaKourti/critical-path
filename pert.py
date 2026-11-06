import numpy as np 
from cpm import cpm

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

def scenario(pert_tasks):
    tasks = {}
    for name in pert_tasks:
        o, m, p, preds = pert_tasks[name]
        alpha = 1 + 4*(m - o)/(p - o)
        beta = 1 + 4*(p - m)/(p - o)
        duration =  o + (p - o)*np.random.beta(alpha, beta)
        tasks[name] = (duration, preds)
    return tasks

s = scenario(pert_tasks)
print(s)
print(cpm(s)["critical"])


N = 10000
durations = []
critical_count = {name: 0 for name in pert_tasks}

for n in range(N):
    n_scenario = scenario(pert_tasks)
    n_results = cpm(n_scenario)
    durations.append(n_results["project_end"])
    for task in n_results["critical"]:
        critical_count[task] += 1

mean_duration = np.mean(durations)
p = 0
for d in durations:
    if d <= 20:
        p+=1

percentage = (p / N)*100
percentile_dur = np.percentile(durations, 90)

print("Mean duration:", mean_duration)
print("%", " of cases project ends in <=20 days:", f"{percentage:.1f}", "%")
for task in pert_tasks:
    print(task, critical_count[task] / N)
print("Percentile duration by 90%:", percentile_dur)