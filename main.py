from models import Producer, Consumer, Controller
from simulation import Simulation
from analysis import compare_algorithms, plot_comparison, renewable_usage



producers = [
    Producer("Solar", 0.2, capacity=80, p_type='renewable'),
    Producer("Battery", 0.4, capacity=50, p_type='renewable'),
    Producer("Diesel", 0.4, capacity=5000, p_type='nonrenewable'),
]
if (sum(p.prob for p in producers) !=1):
    raise ValueError("sum of prob is not valid")

consumers = [
    Consumer("House1", priority=2, weight=5),
    Consumer("House2", priority=1, weight=1),
    Consumer("House3", priority=3, weight=3),
]

controller = Controller()
sim = Simulation(producers, consumers, controller, sim_time=40)
algorithms = ["FIFO", "NPPS", "WRR", "EDF"]

results = compare_algorithms(sim, algorithms, lambda1=1.5, lambda2=2.0)

for algo, metrics in results.items():
    print(f"\nalgorithm: {algo}")
    print(f"\tavg Waiting Time: {metrics['avg_wait']:.2f}")
    print(f"\tavg Response Time: {metrics['avg_resp']:.2f}")
    print(f"\tthroughput: {metrics['throughput']:.2f} req/unit time")
    renew_pct = renewable_usage(metrics["energy_usage"], ["Solar", "Battery"])
    print(f"\trenewable Usage: {renew_pct:.2f}%")

plot_comparison(results)

