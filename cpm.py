import matplotlib.pyplot as plt

tasks = {
        "G": (4, ["B"]),
        "A": (4, []),
        "H": (1, ["F", "G"]),
        "B": (3, []),
        "C": (5, ["A", "B"]),
        "D": (5, ["C"]),
        "E": (6, ["C"]),
        "F": (3, ["D", "E"]),
}

def cpm(tasks):
    order = kahn(tasks)
    ES = {} ; EF = {}
    
    for name in order:
        duration, preds = tasks[name]   #predecessors
        if not preds: #if preds is empty, that is, this node has no preds
            ES[name] = 0
        else:
            ES[name] = max(EF[k] for k in preds)
            
        EF[name] = ES[name] + duration
    
    project_end = max(EF.values())
    
    LS = {} ; LF = {}
    succ = successors(tasks)
    
    for name in reversed(order): #i go from the end to the beginning
        duration, preds = tasks[name]
        if not succ[name]:
            LF[name] = project_end
        else:
            LF[name] = min(LS[k] for k in succ[name])
        LS[name] = LF[name] - duration
    
    slack = {}
    for name in order:
        slack[name] = LS[name] - ES[name]
    
    critical = []
    for name in order:
        if slack[name] == 0:
            critical.append(name)
        
    return {"ES": ES, "EF": EF, "LS": LS, "LF": LF,
            "slack": slack, "critical": critical}


def successors(tasks):
    succ = {}       #successors
    for name in tasks:
        succ[name] = []
        
        for m in tasks:
            duration, preds = tasks[m]
            if name in preds:
                succ[name].append(m)
    return succ

    # Or we can just write the above as:
    # succ = {n: [m for m in tasks if n in tasks[m][1]] for n in tasks}


#Gantt chart
def gantt(tasks, results):
    ES = results['ES']
    EF = results['EF']
    ES_order = sorted(tasks, key=ES.get)
    slack = results['slack']
    critical = results['critical']
    
    for name in ES_order:
        duration, preds = tasks[name]
        if name in critical:    
            mycolor = "red"
        else:
            mycolor = "green"
        plt.barh(name, duration, left=ES[name], color=mycolor)
        plt.barh(name, slack[name], left=EF[name], color="palegreen")
        
    plt.gca().invert_yaxis()
    plt.xlabel("Days")
    plt.title("Gantt chart")
    plt.show()


def kahn(tasks):
    succ = successors(tasks)
    pred_sums = {}
    queue = []
    ordering = []
    for name in tasks:
        duration, preds = tasks[name]
        pred_sums[name] = len(preds)
    
    for name in tasks:
        if pred_sums[name] == 0:
            queue.append(name)
    
    while queue:  #while queue isn't empty
        name = queue.pop(0)   #take out first element
        ordering.append(name) #append it to kahn list
        for m in succ[name]:   #reduce all the tasks that have "name" as pred
            pred_sums[m] -= 1
            if pred_sums[m] == 0:
                queue.append(m)
    
    if len(ordering) != len(tasks):
        raise ValueError("The project is not acyclic.")
    return ordering




if __name__=="__main__":
    results = cpm(tasks)
    print("ES =", results["ES"])
    print("Critical path:", results["critical"])
    gantt(tasks, results) 
    
    tasks2 = dict(tasks)
    tasks2["D"] = (6, ["C"])
    print("Critical (D=6):", cpm(tasks2)["critical"])
    print("Topological ordering:", kahn(tasks))