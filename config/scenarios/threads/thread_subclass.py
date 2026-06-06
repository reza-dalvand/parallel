import time
import os
from random import randint
import io
from threading import Thread


class MyThreadClass(Thread):
    def __init__(self, name, duration, output_buffer):
        Thread.__init__(self)
        self.name = name
        self.duration = duration
        self.output_buffer = output_buffer

    def run(self):
        self.output_buffer.write("---> " + self.name +
              " running, belonging to process ID " +
              str(os.getpid()) + "\n")
        time.sleep(self.duration)
        self.output_buffer.write("---> " + self.name + " over\n")


def scenario_1():
    output_buffer = io.StringIO()

    # Thread Creation
    thread1 = MyThreadClass("Thread#1", randint(1, 3), output_buffer)
    thread2 = MyThreadClass("Thread#2", randint(1, 3), output_buffer)
    thread3 = MyThreadClass("Thread#3", randint(1, 3), output_buffer)
    thread4 = MyThreadClass("Thread#4", randint(1, 3), output_buffer)
    thread5 = MyThreadClass("Thread#5", randint(1, 3), output_buffer)
    thread6 = MyThreadClass("Thread#6", randint(1, 3), output_buffer)
    thread7 = MyThreadClass("Thread#7", randint(1, 3), output_buffer)
    thread8 = MyThreadClass("Thread#8", randint(1, 3), output_buffer)
    thread9 = MyThreadClass("Thread#9", randint(1, 3), output_buffer)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
    thread9.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو یک کلاس سفارشی از کلاس Thread
ارث‌بری می‌کند و منطق اجرای هر Thread
در متد run() پیاده‌سازی می‌شود.

۹ Thread با زمان‌های اجرای تصادفی ایجاد شده
و همگی به صورت همزمان شروع به کار می‌کنند.

هر Thread به طور مستقل وظیفه خود را انجام داده
و پس از پایان عملیات خاتمه می‌یابد.

این روش برای طراحی Threadهای سفارشی،
مدیریت بهتر کد و توسعه برنامه‌های چندنخی
بسیار مناسب است.
        '''
    }


def scenario_2():
    output_buffer = io.StringIO()

    threads = []
    for i in range(1, 6):
        duration = randint(1, 2)
        thread = MyThreadClass(f"Thread#{i}", duration, output_buffer)
        threads.append(thread)

    for thread in threads:
        thread.start()
        thread.join()


    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو Threadها با استفاده از کلاس سفارشی
ایجاد می‌شوند اما اجرای آن‌ها به صورت ترتیبی است.

پس از شروع هر Thread، دستور join() اجرا می‌شود
و برنامه تا پایان همان Thread منتظر می‌ماند.

در نتیجه Thread بعدی تنها پس از اتمام
Thread قبلی اجرا خواهد شد.

این ساختار زمانی کاربرد دارد که ترتیب اجرای وظایف
اهمیت داشته باشد و هر مرحله به نتیجه
مرحله قبل وابسته باشد.
        '''
    }


def scenario_3():
    output_buffer = io.StringIO()

    fast_threads = []
    slow_threads = []

    for i in range(1, 4):
        duration = randint(1, 2)
        fast_thread = MyThreadClass(f"FastThread#{i}", duration, output_buffer)
        fast_threads.append(fast_thread)

    for i in range(1, 4):
        duration = randint(2, 3)
        slow_thread = MyThreadClass(f"SlowThread#{i}", duration, output_buffer)
        slow_threads.append(slow_thread)

    for thread in fast_threads:
        thread.start()

    for thread in fast_threads:
        thread.join()

    for thread in slow_threads:
        thread.start()

    for thread in slow_threads:
        thread.join()
    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو Threadها بر اساس نوع وظیفه
به دو دسته سریع و کند تقسیم می‌شوند.

ابتدا تمامی Threadهای سریع به صورت همزمان
اجرا شده و پس از اتمام کامل آن‌ها،
Threadهای کند آغاز به کار می‌کنند.

در هر دسته پردازش به صورت موازی انجام می‌شود
اما بین دسته‌ها ترتیب اجرا حفظ می‌گردد.

این روش باعث مدیریت بهتر منابع سیستم شده
و امکان سازمان‌دهی وظایف بر اساس
نوع یا اولویت پردازش را فراهم می‌کند.
        '''
    }
