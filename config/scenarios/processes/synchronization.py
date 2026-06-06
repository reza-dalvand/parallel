import multiprocessing
from multiprocessing import Barrier, Lock, Process, Semaphore, Event
from time import time, sleep
from datetime import datetime

def test_with_barrier(synchronizer, serializer, output_queue):
    name = multiprocessing.current_process().name
    synchronizer.wait()
    now = time()
    with serializer:
        line = "process %s ----> %s" % (name, datetime.fromtimestamp(now))
        output_queue.put(line)


def test_without_barrier(output_queue):
    name = multiprocessing.current_process().name
    now = time()
    line = "process %s ----> %s" % (name, datetime.fromtimestamp(now))
    output_queue.put(line)


def scenario_1():
    """سناریو اول: Barrier - همگام‌سازی دو پراسس با Barrier"""

    output_queue = multiprocessing.Queue()
    synchronizer = Barrier(2)
    serializer = Lock()

    processes = [
        Process(name='p1 - test_with_barrier', target=test_with_barrier,
                args=(synchronizer, serializer, output_queue)),
        Process(name='p2 - test_with_barrier', target=test_with_barrier,
                args=(synchronizer, serializer, output_queue)),
        Process(name='p3 - test_without_barrier', target=test_without_barrier,
                args=(output_queue,)),
        Process(name='p4 - test_without_barrier', target=test_without_barrier,
                args=(output_queue,)),
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    return {
        'output': "\n".join(output_lines),
        'explanation': (
            'سناریو اول: همگام‌سازی با Barrier. '
            'پراسس‌های p1 و p2 با Barrier منتظر هم می‌مانند و همزمان آزاد می‌شوند، '
            'در حالی که p3 و p4 بدون هیچ همگام‌سازی‌ای اجرا می‌شوند.'
        )
    }


# ─────────────────────────────────────────
# سناریو ۲: Semaphore
# ─────────────────────────────────────────

def access_shared_resource(semaphore, output_queue):
    name = multiprocessing.current_process().name
    semaphore.acquire()
    now = time()
    line = "process %s ----> %s  [ENTERED]" % (name, datetime.fromtimestamp(now))
    output_queue.put(line)
    sleep(2)  # شبیه‌سازی کار روی منبع مشترک
    semaphore.release()


def scenario_2():
    """سناریو دوم: Semaphore - محدود کردن دسترسی همزمان به حداکثر ۲ پراسس"""

    output_queue = multiprocessing.Queue()
    semaphore = Semaphore(2)  # حداکثر ۲ پراسس همزمان

    processes = [
        Process(name='p1', target=access_shared_resource, args=(semaphore, output_queue)),
        Process(name='p2', target=access_shared_resource, args=(semaphore, output_queue)),
        Process(name='p3', target=access_shared_resource, args=(semaphore, output_queue)),
        Process(name='p4', target=access_shared_resource, args=(semaphore, output_queue)),
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    return {
        'output': "\n".join(output_lines),
        'explanation': (
            'سناریو دوم: همگام‌سازی با Semaphore. '
            'حداکثر ۲ پراسس می‌توانند همزمان به منبع مشترک دسترسی داشته باشند. '
            'p1 و p2 همزمان وارد می‌شوند؛ p3 و p4 باید صبر کنند تا یکی از آن‌ها آزاد شود.'
        )
    }


# ─────────────────────────────────────────
# سناریو ۳: Event
# ─────────────────────────────────────────

def producer(event, output_queue):
    name = multiprocessing.current_process().name
    now = time()
    output_queue.put("process %s ----> %s  [started, preparing data...]" % (
        name, datetime.fromtimestamp(now)))
    sleep(2)  # شبیه‌سازی آماده‌سازی داده
    event.set()  # سیگنال به همه consumers
    now = time()
    output_queue.put("process %s ----> %s  [signal sent]" % (
        name, datetime.fromtimestamp(now)))


def consumer(event, output_queue):
    name = multiprocessing.current_process().name
    event.wait()  # بلاک تا دریافت سیگنال
    now = time()
    output_queue.put("process %s ----> %s  [received signal, started]" % (
        name, datetime.fromtimestamp(now)))


def scenario_3():
    """سناریو سوم: Event - سیگنال‌دهی از یک پراسس به بقیه"""

    output_queue = multiprocessing.Queue()
    event = Event()

    processes = [
        Process(name='p1 - producer', target=producer, args=(event, output_queue)),
        Process(name='p2 - consumer', target=consumer, args=(event, output_queue)),
        Process(name='p3 - consumer', target=consumer, args=(event, output_queue)),
        Process(name='p4 - consumer', target=consumer, args=(event, output_queue)),
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    return {
        'output': "\n".join(output_lines),
        'explanation': (
            'سناریو سوم: همگام‌سازی با Event. '
            'p1 به عنوان producer داده را آماده می‌کند و سیگنال می‌دهد. '
            'p2، p3 و p4 به عنوان consumer منتظر سیگنال می‌مانند و پس از دریافت آن همزمان شروع می‌کنند.'
        )
    }

