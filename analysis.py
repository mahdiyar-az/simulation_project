import copy
import json

import matplotlib.pyplot as plt

def average_waiting_time(requests):
    # print(len(requests))
    waits = []
    for r in requests:
        if r.start_time:
            waits.append(r.start_time - r.arrival_time)
        else:
            waits.append(r.deadline - r.arrival_time)

    return sum(waits) / len(waits)

def average_response_time(requests):
    responses = []
    for r in requests:
        if r.finish_time:
            responses.append(r.finish_time - r.arrival_time)
        else:
            responses.append(r.deadline - r.arrival_time)

    return sum(responses) / len(responses)


def throughput(requests):
    completed = sum(1 for r in requests if r.finish_time)
    return completed / len(requests)

def renewable_usage(energy_usage, renewable_names):
    renewable = sum(energy_usage[name] for name in renewable_names if name in energy_usage)
    total = sum(energy_usage.values())
    return (renewable / total * 100)

def requests_to_json(requests):
    data = []
    for r in requests:
        data.append({
            "arrival_time": r.arrival_time,
            "amount": r.amount,
            "consumer": r.consumer.name,
            "deadline": r.deadline,
            "start_time": r.start_time,
            "finish_time": r.finish_time,
            "status": r.status
        })
    return json.dumps(data, indent=4)
def compare_algorithms(sim, algorithms, lambda1, lambda2):
    results = {}
    sim.requests = []
    sim.generate_requests(chi=2)
    asly_requests = copy.deepcopy(sim.requests)
    asly__producer = copy.deepcopy(sim.producers)
    for algo in algorithms:
        sim.producers = copy.deepcopy(asly__producer)
        sim.requests = copy.deepcopy(asly_requests)
        res = sim.run(algorithm=algo, lambda1=lambda1, lambda2=lambda2)
        json_output = requests_to_json(res)

        with open("./output/"+algo+".json", "w") as f:
            f.write(json_output)
        results[algo] = {
            "avg_wait": average_waiting_time(res),
            "avg_resp": average_response_time(res),
            "throughput": throughput(res),
            "energy_usage": sim.energy_usage.copy()
        }

    return results

def plot_comparison(results):
    algos = list(results.keys())
    waits = [results[a]["avg_wait"] for a in algos]
    resps = [results[a]["avg_resp"] for a in algos]
    thrpts = [results[a]["throughput"] for a in algos]

    plt.figure(figsize=(12,4))

    plt.subplot(1,3,1)
    plt.bar(algos, waits)
    plt.title("average waiting time")

    plt.subplot(1,3,2)
    plt.bar(algos, resps)
    plt.title("average response time")

    plt.subplot(1,3,3)
    plt.bar(algos, thrpts)
    plt.title("throughput")

    plt.show()
