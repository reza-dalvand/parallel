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
        'explanation': '''
        در این سناریو چهار Process به صورت همزمان
ایجاد و اجرا می‌شوند.

دو Process اول از یک Barrier مشترک
استفاده می‌کنند و پس از رسیدن به نقطه تعیین‌شده،
منتظر Process دیگر باقی می‌مانند.

تنها زمانی که هر دو Process به Barrier برسند،
مانع برداشته شده و هر دو به صورت همزمان
به اجرای ادامه برنامه می‌پردازند.

در مقابل، دو Process دیگر هیچ Barrierای
ندارند و بدون انتظار برای سایر Processها
اجرای خود را ادامه می‌دهند.

این سناریو نشان می‌دهد که چگونه Barrier
می‌تواند برای هماهنگ‌سازی چند Process
در یک نقطه مشخص از اجرای برنامه مورد استفاده قرار گیرد.
        '''
    }


# Semaphore

def access_shared_resource(semaphore, output_queue):
    name = multiprocessing.current_process().name
    semaphore.acquire()
    now = time()
    line = "process %s ----> %s  [ENTERED]" % (name, datetime.fromtimestamp(now))
    output_queue.put(line)
    sleep(2)  # شبیه‌سازی کار روی منبع مشترک
    semaphore.release()


def scenario_2():
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
        'explanation': '''
        در این سناریو چهار Process به صورت همزمان
برای دسترسی به یک منبع مشترک تلاش می‌کنند.

برای مدیریت این دسترسی از یک Semaphore
با ظرفیت دو استفاده شده است.

در نتیجه حداکثر دو Process می‌توانند
به طور همزمان وارد بخش بحرانی برنامه شوند
و از منبع مشترک استفاده کنند.

سایر Processها تا زمانی که یکی از
Processهای فعال منبع را آزاد نکند،
در حالت انتظار باقی می‌مانند.

این روش برای محدود کردن تعداد دسترسی‌های همزمان
به منابعی مانند پایگاه داده، فایل‌ها،
اتصالات شبکه یا سرویس‌های اشتراکی کاربرد دارد.
        '''
    }


# Event

def producer(event, output_queue):
    name = multiprocessing.current_process().name
    now = time()
    output_queue.put("process %s ----> %s  [started, preparing data...]" % (
        name, datetime.fromtimestamp(now)))
    sleep(2)
    event.set()  # send signals to consumers
    now = time()
    output_queue.put("process %s ----> %s  [signal sent]" % (
        name, datetime.fromtimestamp(now)))


def consumer(event, output_queue):
    name = multiprocessing.current_process().name
    event.wait()  # block and wait to receive signale
    now = time()
    output_queue.put("process %s ----> %s  [received signal, started]" % (
        name, datetime.fromtimestamp(now)))


def scenario_3():
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
        'explanation': '''
        در این سناریو یک Process در نقش Producer
و سه Process در نقش Consumer اجرا می‌شوند.

Consumerها در ابتدای کار با استفاده از Event
در حالت انتظار قرار می‌گیرند و اجازه ادامه اجرا ندارند.

Producer ابتدا بخشی از پردازش خود را انجام داده
و پس از آماده شدن داده‌ها،
با فراخوانی متد set() سیگنالی برای سایر Processها ارسال می‌کند.

پس از دریافت این سیگنال،
تمام Consumerها به صورت همزمان از حالت انتظار خارج شده
و اجرای خود را آغاز می‌کنند.

این سناریو کاربرد Event را در هماهنگ‌سازی Processها
و اطلاع‌رسانی وقوع یک رویداد مشترک نمایش می‌دهد
و برای پیاده‌سازی الگوهای Producer-Consumer،
آماده‌سازی داده و شروع هماهنگ وظایف بسیار مناسب است.
        '''
    }

