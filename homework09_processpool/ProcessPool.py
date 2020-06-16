import os
import multiprocessing as mp
import threading as th
import psutil


class ProcessPool():
    def __init__(self, min_workers, max_workers, mem_usage):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = self.mem_transformation(mem_usage)

        self.queue = mp.Queue()
        self.completed_queue = mp.Queue()

        self.workers = []


    def worker_function(self, function):
        while True:
            task = self.queue.get()

            job = function(task)

            self.completed_queue.put_nowait(job)


    def map(self, function, big_data):

        potok = th.Thread(target=self.mem_monitoring,
                          args=())
        potok.start()

        for data in big_data:
            self.queue.put(data)

        for i in range(self.max_workers):
            worker = mp.Process(target=self.worker_function,
                                args=(function, ))
            worker.start()
            self.workers.append(worker)

        results = []
        for i in range(len(big_data)):
            result = self.completed_queue.get()
            results.append(result)

        for w in self.workers:
            w.terminate()

        return results


    def mem_transformation(self, mem_usage):
        mem_number = ''
        mem_alph = ''
        k = 0
        for i in range(len(mem_usage)):
            if mem_usage[i].isdigit():
                mem_number += mem_usage[i]
            else:
                mem_alph += mem_usage[i]

        if mem_alph == 'Kb':
            k = 2 ** 13
        elif mem_alph == 'Mb':
            k = 2 ** 23
        elif mem_alph == 'Gb':
            k = 2 ** 33

        return int(mem_number) * k


    def mem_monitoring(self):
        while True:
            total_mem = 0
            for w in self.workers:
                pr = psutil.Process(w.pid)
                total_mem += pr.memory_info().rss

            if total_mem > self.mem_usage:
                for w in self.workers:
                    pr = psutil.Process(w.pid)
                    if pr.memory_info().rss > self.mem_usage/len(self.workers):
                        total_mem -= pr.memory_info().rss
                        w.terminate()
            else:
                for w in self.workers:
                    if w.is_alive:
                        w.start()
