import multiprocessing
import random
import time


class Producer(multiprocessing.Process):
    """کلاس تولیدکننده که آیتم‌ها را به صف اضافه می‌کند"""

    def __init__(self, queue, output_queue, count=5):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.output_queue = output_queue
        self.count = count

    def run(self):
        for i in range(self.count):
            item = random.randint(0, 256)
            self.queue.put(item)
            self.output_queue.put(f"Process Producer : item {item} appended to queue {self.name}")
            self.output_queue.put(f"The size of queue is {self.queue.qsize()}")
            time.sleep(1)


class Consumer(multiprocessing.Process):
    """کلاس مصرف‌کننده که آیتم‌ها را از صف خارج می‌کند"""

    def __init__(self, queue, output_queue, expected_items=5):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.output_queue = output_queue
        self.expected_items = expected_items

    def run(self):
        items_consumed = 0
        while items_consumed < self.expected_items:
            if not self.queue.empty():
                time.sleep(2)
                item = self.queue.get()
                self.output_queue.put(f"Process Consumer : item {item} popped from by {self.name}")
                items_consumed += 1

        if self.queue.empty():
            self.output_queue.put("the queue is empty")


def scenario_1():
    """سناریو اول: یک Producer و یک Consumer - الگوی پایه"""

    # ایجاد صف مشترک برای داده‌ها
    queue = multiprocessing.Queue()

    # ایجاد صف برای جمع‌آوری خروجی‌ها
    output_queue = multiprocessing.Queue()

    # ایجاد یک تولیدکننده و یک مصرف‌کننده
    process_producer = Producer(queue, output_queue, count=5)
    process_consumer = Consumer(queue, output_queue, expected_items=5)

    # شروع پراسس‌ها
    process_producer.start()
    process_consumer.start()

    # انتظار برای اتمام پراسس‌ها
    process_producer.join()
    process_consumer.join()

    # جمع‌آوری تمام خروجی‌ها از صف
    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    # ترکیب خروجی‌ها به صورت رشته
    output = "\n".join(output_lines)

    return {
        'output': output,
        'explanation': 'سناریو اول: الگوی پایه Producer-Consumer. یک Producer پنج آیتم تولید می‌کند و یک Consumer آن‌ها را مصرف می‌کند.'
    }


def scenario_2():
    """سناریو دوم: چند Consumer با یک Producer - الگوی توزیع کار"""

    # ایجاد صف مشترک برای داده‌ها
    queue = multiprocessing.Queue()

    # ایجاد صف برای جمع‌آوری خروجی‌ها
    output_queue = multiprocessing.Queue()

    # ایجاد یک تولیدکننده و سه مصرف‌کننده
    process_producer = Producer(queue, output_queue, count=15)
    process_consumer1 = Consumer(queue, output_queue, expected_items=5)
    process_consumer2 = Consumer(queue, output_queue, expected_items=5)
    process_consumer3 = Consumer(queue, output_queue, expected_items=5)

    # شروع پراسس‌ها
    process_producer.start()
    process_consumer1.start()
    process_consumer2.start()
    process_consumer3.start()

    # انتظار برای اتمام پراسس‌ها
    process_producer.join()
    process_consumer1.join()
    process_consumer2.join()
    process_consumer3.join()

    # جمع‌آوری تمام خروجی‌ها از صف
    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    # ترکیب خروجی‌ها به صورت رشته
    output = "\n".join(output_lines)

    return {
        'output': output,
        'explanation': 'سناریو دوم: الگوی توزیع کار (Load Balancing). یک Producer پانزده آیتم تولید می‌کند و سه Consumer به صورت موازی آیتم‌ها را مصرف می‌کنند.'
    }


def scenario_3():
    """سناریو سوم: چند Producer با یک Consumer - الگوی جمع‌آوری"""

    # ایجاد صف مشترک برای داده‌ها
    queue = multiprocessing.Queue()

    # ایجاد صف برای جمع‌آوری خروجی‌ها
    output_queue = multiprocessing.Queue()

    # ایجاد سه تولیدکننده و یک مصرف‌کننده
    process_producer1 = Producer(queue, output_queue, count=5)
    process_producer2 = Producer(queue, output_queue, count=5)
    process_producer3 = Producer(queue, output_queue, count=5)
    process_consumer = Consumer(queue, output_queue, expected_items=15)

    # شروع پراسس‌ها
    process_producer1.start()
    process_producer2.start()
    process_producer3.start()
    process_consumer.start()

    # انتظار برای اتمام پراسس‌ها
    process_producer1.join()
    process_producer2.join()
    process_producer3.join()
    process_consumer.join()

    # جمع‌آوری تمام خروجی‌ها از صف
    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    # ترکیب خروجی‌ها به صورت رشته
    output = "\n".join(output_lines)

    return {
        'output': output,
        'explanation': 'سناریو سوم: الگوی جمع‌آوری (Aggregation). سه Producer هر کدام پنج آیتم تولید می‌کنند و یک Consumer همه پانزده آیتم را پردازش می‌کند.'
    }

