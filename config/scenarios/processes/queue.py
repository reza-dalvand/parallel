import multiprocessing
import random
import time


class Producer(multiprocessing.Process):
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

# 1 producer - 1 consumer
# هر دو ثانیه 2 تا تولید سومی هم تولید هم مصرف همزمان
def scenario_1():
    queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    process_producer = Producer(queue, output_queue, count=5)
    process_consumer = Consumer(queue, output_queue, expected_items=5)

    process_producer.start()
    process_consumer.start()

    process_producer.join()
    process_consumer.join()

    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    output = "\n".join(output_lines)

    return {
        'output': output,
        'explanation': '''
        در این سناریو یک Process تولیدکننده (Producer)
و یک Process مصرف‌کننده (Consumer)
به صورت همزمان ایجاد و اجرا می‌شوند.

Producer تعدادی داده تصادفی تولید کرده
و آن‌ها را در یک Queue مشترک قرار می‌دهد.

Consumer به صورت مداوم Queue را بررسی کرده
و پس از دریافت هر داده، آن را از Queue خارج می‌کند.

در طول اجرا، Producer مسئول افزودن داده‌ها
و Consumer مسئول پردازش و حذف آن‌ها است.

این سناریو ساده‌ترین شکل استفاده از Queue
برای تبادل داده میان Processها را نمایش می‌دهد
و مفهوم Producer-Consumer را در سطح Processها
معرفی می‌کند.
        '''
    }

# 1 producer - 3 consumer
# دور اول 3 تولید بعد 3 مصرف دور دوم 2 تولید 2 مصرف دور سوم تا اخر 1 تولید 1 مصرف
def scenario_2():
    queue = multiprocessing.Queue()

    output_queue = multiprocessing.Queue()

    process_producer = Producer(queue, output_queue, count=15)
    process_consumer1 = Consumer(queue, output_queue, expected_items=5)
    process_consumer2 = Consumer(queue, output_queue, expected_items=5)
    process_consumer3 = Consumer(queue, output_queue, expected_items=5)

    process_producer.start()
    process_consumer1.start()
    process_consumer2.start()
    process_consumer3.start()

    process_producer.join()
    process_consumer1.join()
    process_consumer2.join()
    process_consumer3.join()

    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    output = "\n".join(output_lines)

    return {
        'output': output,
        'explanation': '''
        در این سناریو یک Process تولیدکننده
و سه Process مصرف‌کننده به صورت همزمان اجرا می‌شوند.

Producer مجموعه‌ای از داده‌ها را تولید کرده
و در Queue مشترک قرار می‌دهد.

هر Consumer به صورت مستقل از Queue
داده دریافت کرده و آن را پردازش می‌کند.

به دلیل استفاده از Queue مشترک،
داده‌ها میان Consumerها تقسیم شده
و هر آیتم تنها توسط یکی از آن‌ها مصرف می‌شود.

در نتیجه بار پردازش میان چند Consumer
توزیع شده و سرعت انجام کار افزایش می‌یابد.

این الگو در سیستم‌های پردازش موازی،
سامانه‌های صف پیام و معماری‌های توزیع‌شده
برای متعادل‌سازی بار پردازشی کاربرد فراوان دارد.
        '''
    }

# 3 producer - 1 consumer
# اول 9 آیتم تولید بعدی یکی مصرف سپس 6 آیتم تولید بعد دونه دونه مصرف میشن
def scenario_3():
    queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    process_producer1 = Producer(queue, output_queue, count=5)
    process_producer2 = Producer(queue, output_queue, count=5)
    process_producer3 = Producer(queue, output_queue, count=5)
    process_consumer = Consumer(queue, output_queue, expected_items=15)

    process_producer1.start()
    process_producer2.start()
    process_producer3.start()
    process_consumer.start()

    process_producer1.join()
    process_producer2.join()
    process_producer3.join()
    process_consumer.join()

    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    output = "\n".join(output_lines)

    return {
        'output': output,
        'explanation': '''
        در این سناریو سه Process تولیدکننده
و یک Process مصرف‌کننده به صورت همزمان اجرا می‌شوند.

هر Producer داده‌های مخصوص به خود را تولید کرده
و در Queue مشترک قرار می‌دهد.

تمام داده‌های تولیدشده توسط Producerهای مختلف
در یک صف واحد جمع‌آوری می‌شوند.

Consumer تمامی داده‌های موجود در Queue را
به ترتیب دریافت و پردازش می‌کند.

این ساختار امکان تجمیع داده‌های تولیدشده
از چند منبع مختلف را فراهم می‌کند
و Consumer نقش نقطه مرکزی پردازش را بر عهده دارد.

این الگو در سامانه‌های جمع‌آوری لاگ،
پردازش رویدادها، دریافت داده از چند حسگر
و سیستم‌های پردازش متمرکز بسیار رایج است.
        '''
    }

