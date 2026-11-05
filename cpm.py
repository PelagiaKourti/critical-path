import matplotlib.pyplot as plt

tasks = {
        "A": (4, []),
        "B": (3, []),
        "C": (5, ["A", "B"]),
        "D": (5, ["C"]),
        "E": (6, ["C"]),
        "F": (3, ["D", "E"]),
        "G": (4, ["B"]),
        "H": (1, ["F", "G"]),
}

def cpm(tasks):
    ES = {}
    EF = {}

    for name in tasks:
        duration, preds = tasks[name]   #predecessors
        if not preds: #if preds is empty, that is, this node has no preds
            ES[name] = 0
        else:
            ES[name] = max(EF[k] for k in preds)
            
        EF[name] = ES[name] + duration

    project_end = max(EF.values())

    LS = {}
    LF = {}


    succ = {}       #successors
    for name in tasks:
        succ[name] = []
        
        for m in tasks:
            duration, preds = tasks[m]
            if name in preds:
                succ[name].append(m)

    # Or we can just write the above as:
    # succ = {n: [m for m in tasks if n in tasks[m][1]] for n in tasks}


    for name in reversed(list(tasks)): #i go from the end to the beginning
        duration, preds = tasks[name]
        if not succ[name]:
            LF[name] = project_end
        else:
            LF[name] = min(LS[k] for k in succ[name])
        LS[name] = LF[name] - duration
        
    slack = {}
    for name in tasks:
        slack[name] = LS[name] - ES[name]
    
    
    critical = []
    for name in tasks:
        if slack[name] == 0:
            critical.append(name)
        
    return {"ES": ES, "EF": EF, "LS": LS, "LF": LF,
            "slack": slack, "critical": critical}


#Gantt chart
def gantt(tasks, results):
    ES = results['ES']
    EF = results['EF']
    slack = results['slack']
    critical = results['critical']
    
    for name in tasks:
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

if __name__=="__main__":
    results = cpm(tasks)
    print("ES =", results["ES"])
    print("Critical path:", results["critical"])
    gantt(tasks, results) 
    
    tasks2 = dict(tasks)
    tasks2["D"] = (6, ["C"])
    print("Critical (D=6):", cpm(tasks2)["critical"])