import threading
import time
import random
import io
from datetime import datetime

def scenario_1():
    output_buffer = io.StringIO()

    semaphore = threading.Semaphore(0)
    item = [0]

    def log_message(thread_name, level, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
        output_buffer.write(f"{timestamp} {thread_name:<17} {level:<8} {message}\n")

    def consumer():
        thread_name = threading.current_thread().name
        log_message(thread_name, 'INFO', 'Consumer is waiting')
        semaphore.acquire()
        log_message(thread_name, 'INFO', f'Consumer notify: item number {item[0]}')

    def producer():
        thread_name = threading.current_thread().name
        time.sleep(3)
        item[0] = random.randint(0, 1000)
        log_message(thread_name, 'INFO', f'Producer notify: item number {item[0]}')
        semaphore.release()

    for i in range(10):
        t1 = threading.Thread(target=consumer)
        t2 = threading.Thread(target=producer)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو یک Thread تولیدکننده و یک Thread مصرف‌کننده
برای تبادل یک آیتم مشترک ایجاد می‌شوند.

برای هماهنگی بین این دو Thread از Semaphore با مقدار اولیه صفر
استفاده شده است تا مصرف‌کننده تا زمان تولید داده منتظر بماند.

ابتدا Thread مصرف‌کننده اجرا شده و در حالت انتظار قرار می‌گیرد.
سپس Thread تولیدکننده پس از ایجاد یک مقدار تصادفی،
سیگنال آزادسازی Semaphore را ارسال می‌کند.

در این لحظه مصرف‌کننده بیدار شده و مقدار تولیدشده را دریافت می‌کند.
این روند برای چندین جفت تولید و مصرف تکرار می‌شود.

'''
}


def scenario_2():
    output_buffer = io.StringIO()
    semaphore = threading.Semaphore(0)
    items = []
    items_lock = threading.Lock()

    def producer(producer_id):
        time.sleep(random.uniform(0.1, 0.5))
        item = random.randint(0, 1000)

        with items_lock:
            items.append(item)
            output_buffer.write(f"[Producer-{producer_id}] Produced item {item}\n")

        semaphore.release()  # به consumer اطلاع می‌دهد که یک آیتم جدید آماده است

    def consumer(total_items):
        consumed = 0
        output_buffer.write(f"[Consumer] Waiting for {total_items} items...\n")

        while consumed < total_items:
            semaphore.acquire()  # منتظر یک آیتم جدید

            with items_lock:
                if items:
                    item = items.pop(0)
                    consumed += 1
                    output_buffer.write(f"[Consumer] Consumed item {item} ({consumed}/{total_items})\n")

    num_producers = 5

    producer_threads = []
    for i in range(num_producers):
        t = threading.Thread(target=producer, args=(i+1,))
        producer_threads.append(t)
        t.start()

    consumer_thread = threading.Thread(target=consumer, args=(num_producers,))
    consumer_thread.start()

    for t in producer_threads:
        t.join()
    consumer_thread.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو چند Thread تولیدکننده به صورت همزمان
آیتم‌های مختلف تولید می‌کنند و یک Thread مصرف‌کننده
همه آیتم‌ها را از یک لیست مشترک دریافت می‌کند.

برای کنترل دسترسی به لیست مشترک از Lock استفاده شده
و برای اطلاع‌رسانی تولید آیتم جدید از Semaphore بهره گرفته شده است.

هر تولیدکننده پس از تولید یک مقدار، آن را در لیست مشترک
ذخیره کرده و Semaphore را آزاد می‌کند.

مصرف‌کننده نیز به تعداد آیتم‌های تولیدشده در حالت انتظار
قرار می‌گیرد و پس از دریافت سیگنال، آیتم‌ها را یکی‌یکی مصرف می‌کند.

این مدل نمونه‌ای از سیستم‌های صف (Queue) است
که در آن چند تولیدکننده به یک مصرف‌کننده سرویس می‌دهند.
        '''
    }


#Scenario 3: Bounded Buffer (Pool of Resources)

def scenario_3():
    output_buffer = io.StringIO()

    BUFFER_SIZE = 3
    buffer = []
    buffer_lock = threading.Lock()

    empty_slots = threading.Semaphore(BUFFER_SIZE)

    filled_slots = threading.Semaphore(0)

    def producer(producer_id, num_items):
        for i in range(num_items):
            item = random.randint(0, 100)

            output_buffer.write(f"[Producer-{producer_id}] Trying to produce item {item}...\n")
            empty_slots.acquire()  # منتظر یک فضای خالی

            with buffer_lock:
                buffer.append(item)
                output_buffer.write(f"[Producer-{producer_id}] Produced item {item}. Buffer: {buffer}\n")

            filled_slots.release()  # اعلام اینکه یک آیتم جدید اضافه شده
            time.sleep(random.uniform(0.1, 0.3))

    def consumer(consumer_id, num_items):
        for i in range(num_items):
            output_buffer.write(f"[Consumer-{consumer_id}] Waiting for an item...\n")
            filled_slots.acquire()  # منتظر یک آیتم پر

            with buffer_lock:
                if buffer:
                    item = buffer.pop(0)
                    output_buffer.write(f"[Consumer-{consumer_id}] Consumed item {item}. Buffer: {buffer}\n")

            empty_slots.release()  # اعلام اینکه یک فضا خالی شده
            time.sleep(random.uniform(0.2, 0.4))

    # 2 producer، هر کدام 4 آیتم تولید می‌کنند
    # 2 consumer، هر کدام 4 آیتم مصرف می‌کنند
    threads = []

    for i in range(2):
        t = threading.Thread(target=producer, args=(i+1, 4))
        threads.append(t)
        t.start()

    for i in range(2):
        t = threading.Thread(target=consumer, args=(i+1, 4))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو چند Thread تولیدکننده و مصرف‌کننده
روی یک بافر مشترک با ظرفیت محدود کار می‌کنند.

برای مدیریت ظرفیت از دو Semaphore استفاده شده است:
یکی برای تعداد فضاهای خالی و دیگری برای تعداد آیتم‌های موجود.

تولیدکننده قبل از افزودن آیتم باید از فضای خالی اطمینان حاصل کند
و مصرف‌کننده نیز قبل از برداشت آیتم باید از وجود داده مطمئن شود.

پس از تولید هر آیتم، شمارنده آیتم‌های موجود افزایش یافته
و پس از مصرف هر آیتم، یک فضای خالی آزاد می‌شود.

این ساختار نمونه‌ای کامل از مسئله کلاسیک Producer-Consumer
با بافر محدود است که در سیستم‌عامل‌ها و صف‌های پردازشی کاربرد دارد.

        '''
    }