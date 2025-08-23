import random
import numpy as np
from rich import print

from models import Producer, Consumer, Request, Controller


def exponential_distribution(lmbda, size):
    return np.random.exponential(1/lmbda, size)

def poisson_distribution(lmbda, size):
    return np.random.poisson(lmbda, size)
class Simulation:
    def __init__(self, producers, consumers, controller, sim_time=50):
        self.producers = producers
        self.consumers = consumers
        self.controller = controller
        self.sim_time = sim_time
        self.requests = []
        self.energy_usage = {p.name: 0 for p in producers}

    def generate_requests(self, chi=2):
        arrival_times = poisson_distribution(chi, int(self.sim_time/1))
        for t in range(self.sim_time):
            num_reqs = arrival_times[t]
            # print(t,num_reqs)
            for _ in range(num_reqs):
                consumer = random.choice(self.consumers)
                amount = random.randint(1, 5)
                deadline = t + random.randint(5, 15)
                req = Request(consumer, amount, t, deadline)
                self.requests.append(req)

    def run(self, algorithm, lambda1, lambda2, t_delay=0, C=0):

        print(f"algorithm : {algorithm} ")

        current_time = 0
        processed_requests = []
        pending = []
        all_requests = sorted(self.requests, key=lambda r: r.arrival_time)
        # for t in all_requests:
        #     print(t)

        for r in all_requests:
            r.start_time = None
            r.finish_time = None
            r.status = "pending"

        while (all_requests or pending) and current_time <= self.sim_time:
            # print(len(all_requests),len(pending),len(processed_requests))
            while all_requests and all_requests[0].arrival_time <= current_time:
                pending.append(all_requests.pop(0))

            for r in pending:
                # print(r.deadline)
                if  r.deadline <= current_time:
                    r.status = "dropped_deadline"
                    if r not in processed_requests:
                        processed_requests.append(r)
                        # print("injaaaaaaaaaaaaaa")

            pending = [r for r in pending if r.status == "pending"]

            if pending:
                if algorithm == "FIFO":
                    req = min(pending, key=lambda r: r.arrival_time)
                elif algorithm == "NPPS":
                    req = max(pending, key=lambda r: r.consumer.priority)
                elif algorithm == "EDF":
                    req = min(pending, key=lambda r: r.deadline)
                elif algorithm == "WRR":
                    valid_requests = [r for r in pending if r.consumer.available_weight > 0]
                    if not valid_requests:
                        # print('injaaaa')
                        for c in pending:
                            c.consumer.reset_available_weight()
                        continue

                    req = max(valid_requests, key=lambda r: r.consumer.available_weight)
                    req.consumer.available_weight -= 1
                pending.remove(req)
                available_producers = [p for p in self.producers if p.available >= req.amount]
                if not available_producers:
                    req.status = "dropped_no_capacity"
                    processed_requests.append(req)
                    continue

                weights_prods = [p.prob for p in available_producers]
                producer = random.choices(available_producers, weights=weights_prods, k=1)[0]

                service_time_ctrl = exponential_distribution(lambda1, 1)[0]
                start_ctrl = max(req.arrival_time, current_time)
                finish_ctrl = start_ctrl + service_time_ctrl + t_delay
                # print(producer.type)
                if producer.type == "renewable":
                    service_time_src = exponential_distribution(lambda2, 1)[0]
                else:
                    service_time_src = 0.001

                start_src = finish_ctrl + C
                finish_src = start_src + service_time_src

                if finish_src > self.sim_time:
                    req.status = "dropped_sim_time"
                    processed_requests.append(req)
                    continue

                producer.available = producer.available - req.amount
                self.energy_usage[producer.name] = self.energy_usage[producer.name] + req.amount

                req.start_time = start_src
                req.finish_time = finish_src
                req.status = "processed"
                current_time = finish_src
                processed_requests.append(req)

            else:
                current_time = current_time + 1

        for r in pending:
            if r.status == "pending":
                r.status = "dropped_remaining"
            if r not in processed_requests:
                processed_requests.append(r)
        for r in all_requests:
            if r.status == "pending":
                r.status = "dropped_remaining"
            if r not in processed_requests:
                processed_requests.append(r)
        return processed_requests

