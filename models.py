import random

class Producer:
    def __init__(self, name,prob, capacity, p_type="renewable"):
        self.name = name
        self.capacity = capacity
        self.available = capacity
        self.type = p_type   # "renewable" یا "nonrenewable"
        self.prob = prob

    def provide(self, amount):
        if self.available >= amount:
            self.available -= amount
            return amount
        else:
            taken = self.available
            self.available = 0
            return taken

    def reset(self):
        self.available = self.capacity


class Consumer:
    def __init__(self, name, priority=1, weight=1):
        self.name = name
        self.priority = priority
        self.weight = weight
        self.available_weight = weight
    def __str__(self):
        return self.name+'-'+str(self.weight)+'-'+str(self.priority)+'-'+str(self.available_weight)

    def reset_available_weight(self):
        self.available_weight=self.weight

class Request:
    def __init__(self, consumer, amount, arrival_time, deadline=None):
        self.consumer = consumer
        self.amount = amount
        self.arrival_time = arrival_time
        self.deadline = deadline
        self.start_time = None
        self.finish_time = None
        self.status = "pending"


    def __str__(self):
        return self.consumer.name+'-'+str(self.consumer.weight)+'-'+str(self.consumer.priority)+'-'+str(self.start_time)+'-'+str(self.arrival_time)+'-'+str(self.deadline)
class Controller:
    def __init__(self):
        self.queue = []

    def add_request(self, request):
        self.queue.append(request)

    def clear(self):
        self.queue = []
