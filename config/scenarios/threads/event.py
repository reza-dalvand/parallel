import random
import time
import threading
import io

# +1 +1 +1...
# -1 -1 -1 ...
def scenario_1():
    output_buffer = io.StringIO()

    items = []

    event = threading.Event()

    def producer():

        for i in range(5):

            time.sleep(2)

            item = random.randint(0, 100)

            items.append(item)

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            output_buffer.write(
                f'{timestamp} Producer INFO '
                f'Producer notify: item {item} appended\n'
            )

            event.set()

            event.clear()

    def consumer():

        for i in range(5):

            event.wait()

            item = items.pop()

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            output_buffer.write(
                f'{timestamp} Consumer INFO '
                f'Consumer notify: {item} popped\n'
            )

    producer_thread = threading.Thread(
        target=producer,
        name='Thread-1'
    )

    consumer_thread = threading.Thread(
        target=consumer,
        name='Thread-2'
    )

    producer_thread.start()

    consumer_thread.start()

    producer_thread.join()

    consumer_thread.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو یک Thread تولیدکننده
و یک Thread مصرف‌کننده ایجاد می‌شوند.

تولیدکننده پس از تولید هر آیتم،
Event را فعال کرده و مصرف‌کننده
را از وجود داده جدید مطلع می‌کند.

مصرف‌کننده تا زمان دریافت سیگنال
در حالت انتظار باقی می‌ماند و سپس
داده تولیدشده را پردازش می‌کند.

Event در اینجا نقش یک مکانیزم
اعلان (Notification) را بر عهده دارد
و ارتباط میان دو Thread را برقرار می‌کند.
'''
    }


# 3 producer 1 consumer 
# +1 +1 +1 ...
# -1 -1 -1 ...
def scenario_2():
    output_buffer = io.StringIO()

    items = []

    lock = threading.Lock()

    event = threading.Event()

    def producer(worker_id):
        for i in range(3):
            time.sleep(random.uniform(0.5, 1.5)) # مثلا ممکن نخ 2 از 1 زودتر آیتم تولید کنه
            item = random.randint(1, 100)

            with lock:
                items.append(item)
                output_buffer.write(f'Producer-{worker_id} produced {item}\n')

            event.set()

    def consumer():
        consumed = 0
        while consumed < 9:
            event.wait()
            with lock:
                while items:
                    item = items.pop(0)
                    consumed += 1
                    output_buffer.write(f'Consumer consumed {item}\n')
                event.clear()

    threads = []

    for i in range(3):
        t = threading.Thread(target=producer, args=(i + 1,))
        threads.append(t)
        t.start()

    consumer_thread = threading.Thread(target=consumer)
    consumer_thread.start()

    for t in threads:
        t.join()

    consumer_thread.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو چند Thread تولیدکننده
به صورت همزمان داده تولید می‌کنند.

هر تولیدکننده پس از افزودن داده
رویداد Event را فعال می‌کند.

مصرف‌کننده با دریافت سیگنال
آیتم‌های موجود را پردازش می‌کند.

استفاده از Lock نیز باعث می‌شود
دسترسی همزمان به لیست مشترک
بدون بروز خطا انجام شود.

این الگو نمونه‌ای از سیستم‌های
چندتولیدکننده و یک مصرف‌کننده است.
'''
    }

# 1 producer 1 consumer
# +1 +1 +1 -1 -1 -1
def scenario_3():
    output_buffer = io.StringIO()

    event = threading.Event()

    results = []

    def producer():

        output_buffer.write('Preparing data...\n')

        time.sleep(3)

        for i in range(5):

            results.append(i)

        output_buffer.write('Data preparation completed\n')

        event.set()

    def consumer():
        output_buffer.write('Waiting for data...\n')
        event.wait()
        output_buffer.write('Processing data...\n')

        for item in results:
            output_buffer.write(f'Processed item {item}\n')

    producer_thread = threading.Thread(target=producer)

    consumer_thread = threading.Thread(target=consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو عملیات در دو مرحله
مجزا انجام می‌شود.

ابتدا Thread اول داده‌های مورد نیاز
را آماده‌سازی می‌کند.

پس از اتمام این مرحله،
یک Event فعال می‌شود.

Thread دوم تا دریافت این سیگنال
در حالت انتظار باقی می‌ماند.

پس از فعال شدن Event،
مرحله پردازش داده‌ها آغاز می‌شود.

این روش برای اجرای مرحله‌ای
و وابستگی بین وظایف مختلف
بسیار مناسب است.
'''
    }