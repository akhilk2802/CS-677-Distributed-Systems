import threading
import queue

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = queue.Queue()
        self.threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)
            print(thread)

    def worker(self):
        while True:
            func, args = self.tasks.get()
            print(args)
            print(func)
            try:
                func(*args)
            finally:
                self.tasks.task_done()

    def add_task(self, func, *args):
        self.tasks.put((func, args))

    def wait_completion(self):
        self.tasks.join()