import threading
import time
import random
import io

# condition جهت جلوگیری از بن‌بست بعد از ورود نخ به فانکشن
def scenario_1():
    output_buffer = io.StringIO()

    items = []
    condition = threading.Condition()

    def producer():
        for i in range(5):

            time.sleep(2)

            item = random.randint(0, 100)

            with condition:
                items.append(item)

                output_buffer.write(
                    f'Producer notify: item {item} appended\n'
                )

                condition.notify()

    def consumer():

        for i in range(5):

            with condition:

                while len(items) == 0:

                    output_buffer.write(
                        'Consumer waiting...\n'
                    )

                    condition.wait()

                item = items.pop(0)

                output_buffer.write(
                    f'Consumer notify: {item} popped\n'
                )

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو یک Thread تولیدکننده
و یک Thread مصرف‌کننده وجود دارد.

مصرف‌کننده زمانی که لیست خالی باشد
با استفاده از Condition وارد حالت انتظار می‌شود.

پس از تولید یک آیتم توسط تولیدکننده،
تابع notify() اجرا شده و مصرف‌کننده
از حالت انتظار خارج می‌شود.

سپس آیتم تولیدشده از لیست برداشته شده
و پردازش ادامه پیدا می‌کند.

این الگو یکی از رایج‌ترین کاربردهای
Condition در مسئله Producer-Consumer است.
'''
    }

# 3 مصرف کننده 1 تولید کننده
def scenario_2():

    output_buffer = io.StringIO()

    items = []
    condition = threading.Condition()

    total_items = 9

    def producer(producer_id):

        for _ in range(3):

            time.sleep(random.uniform(0.5, 1.5))

            item = random.randint(0, 100)

            with condition:

                items.append(item)

                output_buffer.write(
                    f'Producer-{producer_id} produced {item}\n'
                )

                condition.notify()

    def consumer():

        consumed = 0

        while consumed < total_items:

            with condition:

                while len(items) == 0:

                    output_buffer.write(
                        'Consumer waiting...\n'
                    )

                    condition.wait()

                item = items.pop(0)

                consumed += 1

                output_buffer.write(
                    f'Consumer consumed {item}\n'
                )

    producers = []

    for i in range(3):
        t = threading.Thread(
            target=producer,
            args=(i + 1,)
        )
        producers.append(t)
        t.start()

    consumer_thread = threading.Thread(target=consumer)
    consumer_thread.start()

    for t in producers:
        t.join()

    consumer_thread.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو چند Thread تولیدکننده
به صورت همزمان آیتم تولید می‌کنند.

تمام آیتم‌ها در یک منبع مشترک ذخیره شده
و یک Thread مصرف‌کننده آن‌ها را دریافت می‌کند.

هر زمان که لیست خالی باشد،
مصرف‌کننده توسط Condition متوقف می‌شود.

پس از تولید یک آیتم جدید،
یکی از Threadهای منتظر با notify()
بیدار شده و پردازش ادامه پیدا می‌کند.

این الگو نمونه‌ای از صف‌های کاری
در سیستم‌های چندنخی است.
'''
    }

# 1 تولید کننده 1 مصرف کننده با بافر
def scenario_3():

    output_buffer = io.StringIO()

    BUFFER_SIZE = 3

    items = []

    condition = threading.Condition()

    def producer():

        for _ in range(8):

            item = random.randint(1, 100)

            with condition:

                while len(items) >= BUFFER_SIZE:

                    output_buffer.write(
                        'Buffer full -> Producer waiting\n'
                    )

                    condition.wait()

                items.append(item)

                output_buffer.write(
                    f'Produced {item} | Buffer={items}\n'
                )

                condition.notify_all()

            time.sleep(random.uniform(0.2, 0.8))

    def consumer():

        for _ in range(8):

            with condition:

                while len(items) == 0:

                    output_buffer.write(
                        'Buffer empty -> Consumer waiting\n'
                    )

                    condition.wait()

                item = items.pop(0)

                output_buffer.write(
                    f'Consumed {item} | Buffer={items}\n'
                )

                condition.notify_all()

            time.sleep(random.uniform(0.5, 1))

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
در این سناریو یک بافر با ظرفیت محدود
میان Producer و Consumer مشترک است.

اگر بافر پر شود،
تولیدکننده اجازه تولید بیشتر نداشته
و وارد حالت انتظار می‌شود.

اگر بافر خالی شود،
مصرف‌کننده نیز تا زمان ورود داده جدید
منتظر باقی می‌ماند.

Condition وظیفه هماهنگ‌سازی این دو Thread
را برعهده دارد و پس از هر تغییر وضعیت،
Threadهای منتظر را بیدار می‌کند.

این الگو یکی از مهم‌ترین کاربردهای
Condition در سیستم‌های واقعی محسوب می‌شود
و در صف‌های پیام، پردازش داده و شبکه
استفاده فراوانی دارد.
'''
    }