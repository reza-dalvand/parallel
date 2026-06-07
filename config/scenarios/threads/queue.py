import threading
import time
import random
import queue
import io


def scenario_1():

    output_buffer = io.StringIO()

    q = queue.Queue()

    def producer():

        for _ in range(5):

            time.sleep(2)

            item = random.randint(0, 100)

            q.put(item)

            output_buffer.write(
                f'Producer produced {item}\n'
            )

    def consumer():

        for _ in range(5):

            item = q.get()

            output_buffer.write(
                f'Consumer consumed {item}\n'
            )

            q.task_done()

    producer_thread = threading.Thread(
        target=producer
    )

    consumer_thread = threading.Thread(
        target=consumer
    )

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو یک Thread تولیدکننده
و یک Thread مصرف‌کننده وجود دارد.

تولیدکننده داده‌ها را داخل Queue قرار می‌دهد
و مصرف‌کننده آن‌ها را از Queue دریافت می‌کند.

اگر Queue خالی باشد،
تابع get() به صورت خودکار منتظر می‌ماند
تا داده جدید وارد صف شود.

Queue عملیات همگام‌سازی را به صورت داخلی
مدیریت می‌کند و نیازی به Lock یا Condition نیست.

این ساده‌ترین الگوی Producer-Consumer
با استفاده از Queue است.
'''
    }


def scenario_2():

    output_buffer = io.StringIO()

    q = queue.Queue()

    def producer():

        for _ in range(5):

            time.sleep(2)

            item = random.randint(0, 100)

            q.put(item)

            output_buffer.write(
                f'Producer produced {item}\n'
            )

    def consumer():

        for _ in range(5):

            item = q.get()

            output_buffer.write(
                f'Consumer consumed {item}\n'
            )

            q.task_done()

    producer_thread = threading.Thread(
        target=producer
    )

    consumer_thread = threading.Thread(
        target=consumer
    )

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو یک Thread تولیدکننده
و یک Thread مصرف‌کننده وجود دارد.

تولیدکننده داده‌ها را داخل Queue قرار می‌دهد
و مصرف‌کننده آن‌ها را از Queue دریافت می‌کند.

اگر Queue خالی باشد،
تابع get() به صورت خودکار منتظر می‌ماند
تا داده جدید وارد صف شود.

Queue عملیات همگام‌سازی را به صورت داخلی
مدیریت می‌کند و نیازی به Lock یا Condition نیست.

این ساده‌ترین الگوی Producer-Consumer
با استفاده از Queue است.
'''
    }


def scenario_3():

    output_buffer = io.StringIO()

    q = queue.Queue()

    num_workers = 3

    def worker(worker_id):

        while True:

            task = q.get()

            if task is None:

                q.task_done()

                output_buffer.write(
                    f'Worker-{worker_id} stopped\n'
                )

                break

            output_buffer.write(
                f'Worker-{worker_id} processing task {task}\n'
            )

            time.sleep(
                random.uniform(0.5, 1.5)
            )

            output_buffer.write(
                f'Worker-{worker_id} finished task {task}\n'
            )

            q.task_done()

    workers = []

    for i in range(num_workers):

        t = threading.Thread(
            target=worker,
            args=(i + 1,)
        )

        workers.append(t)
        t.start()

    for task in range(1, 11):

        q.put(task)

    q.join()

    for _ in range(num_workers):
        q.put(None)

    for t in workers:
        t.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو چند Worker به صورت همزمان
وظایف موجود در Queue را پردازش می‌کنند.

وظایف توسط Thread اصلی داخل Queue
قرار داده می‌شوند و هر Worker
یک وظیفه را دریافت و اجرا می‌کند.

پس از پایان تمام وظایف،
یک مقدار ویژه (None) به Queue ارسال می‌شود
تا Workerها متوقف شوند.

این الگو پایه بسیاری از سیستم‌های
پردازش موازی، سرورها و صف‌های کاری است.

Queue وظیفه توزیع کار میان Workerها
را به صورت ایمن و خودکار انجام می‌دهد.
'''
    }