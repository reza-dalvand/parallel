import time
import os
from random import randint
import io
from threading import Thread, Lock


class MyThreadClass(Thread):
    def __init__(self, name, duration, output_buffer, thread_lock):
        Thread.__init__(self)
        self.name = name
        self.duration = duration
        self.output_buffer = output_buffer
        self.thread_lock = thread_lock

    def run(self):
        # Acquire the Lock
        self.thread_lock.acquire()
        self.output_buffer.write("---> " + self.name +
              " running, belonging to process ID " +
              str(os.getpid()) + "\n")
        time.sleep(self.duration)
        self.output_buffer.write("---> " + self.name + " over\n")
        # Release the Lock
        self.thread_lock.release()


def scenario_1():
    output_buffer = io.StringIO()
    thread_lock = Lock()

    # Thread Creation
    thread1 = MyThreadClass("Thread#1", randint(1, 3), output_buffer, thread_lock)
    thread2 = MyThreadClass("Thread#2", randint(1, 3), output_buffer, thread_lock)
    thread3 = MyThreadClass("Thread#3", randint(1, 3), output_buffer, thread_lock)
    thread4 = MyThreadClass("Thread#4", randint(1, 3), output_buffer, thread_lock)
    thread5 = MyThreadClass("Thread#5", randint(1, 3), output_buffer, thread_lock)
    thread6 = MyThreadClass("Thread#6", randint(1, 3), output_buffer, thread_lock)
    thread7 = MyThreadClass("Thread#7", randint(1, 3), output_buffer, thread_lock)
    thread8 = MyThreadClass("Thread#8", randint(1, 3), output_buffer, thread_lock)
    thread9 = MyThreadClass("Thread#9", randint(1, 3), output_buffer, thread_lock)

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
در این سناریو از مکانیزم Lock
برای کنترل دسترسی Threadها استفاده می‌شود.

هر Thread قبل از اجرای عملیات خود
باید قفل را دریافت کند و پس از اتمام کار
آن را آزاد نماید.

به همین دلیل در هر لحظه تنها یک Thread
اجازه اجرا دارد و سایر Threadها
در انتظار آزاد شدن قفل باقی می‌مانند.

این روش از تداخل داده‌ها جلوگیری کرده
و اجرای ایمن وظایف مشترک را تضمین می‌کند.
        '''
    }


class MyThreadClassPartialLock(Thread):
    def __init__(self, name, duration, output_buffer, thread_lock):
        Thread.__init__(self)
        self.name = name
        self.duration = duration
        self.output_buffer = output_buffer
        self.thread_lock = thread_lock

    def run(self):
        self.output_buffer.write("---> " + self.name +
              " running, belonging to process ID " +
              str(os.getpid()) + "\n")
        time.sleep(self.duration)

        self.thread_lock.acquire()
        self.output_buffer.write("---> " + self.name + " over\n")
        self.thread_lock.release()


def scenario_2():
    output_buffer = io.StringIO()
    thread_lock = Lock()

    thread1 = MyThreadClassPartialLock("Thread#1", randint(1, 3), output_buffer, thread_lock)
    thread2 = MyThreadClassPartialLock("Thread#2", randint(1, 3), output_buffer, thread_lock)
    thread3 = MyThreadClassPartialLock("Thread#3", randint(1, 3), output_buffer, thread_lock)
    thread4 = MyThreadClassPartialLock("Thread#4", randint(1, 3), output_buffer, thread_lock)
    thread5 = MyThreadClassPartialLock("Thread#5", randint(1, 3), output_buffer, thread_lock)
    thread6 = MyThreadClassPartialLock("Thread#6", randint(1, 3), output_buffer, thread_lock)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو تنها بخش حساس برنامه
توسط Lock محافظت می‌شود.

عملیات اصلی هر Thread به صورت موازی
انجام می‌شود و فقط هنگام ثبت نتیجه نهایی
قفل دریافت می‌شود.

این رویکرد باعث می‌شود بخش عمده پردازش
به صورت همزمان اجرا شده و در عین حال
از تداخل در داده‌های مشترک جلوگیری شود.

در نتیجه تعادل مناسبی بین سرعت اجرا
و ایمنی داده‌ها برقرار می‌شود.
        '''
    }


class MyThreadClassWithCounter(Thread):
    def __init__(self, name, duration, output_buffer, thread_lock, shared_counter):
        Thread.__init__(self)
        self.name = name
        self.duration = duration
        self.output_buffer = output_buffer
        self.thread_lock = thread_lock
        self.shared_counter = shared_counter

    def run(self):
        self.output_buffer.write("---> " + self.name +
              " running, belonging to process ID " +
              str(os.getpid()) + "\n")
        time.sleep(self.duration)

        self.thread_lock.acquire()
        self.shared_counter['value'] += 1
        current_count = self.shared_counter['value']
        self.output_buffer.write("---> " + self.name +
                                f" over (Total completed: {current_count})\n")
        self.thread_lock.release()


def scenario_3():
    output_buffer = io.StringIO()

    thread_lock = Lock()

    shared_counter = {'value': 0}

    threads = []
    for i in range(1, 9):
        thread = MyThreadClassWithCounter(
            f"Thread#{i}",
            randint(1, 3),
            output_buffer,
            thread_lock,
            shared_counter
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو چند Thread به یک شمارنده مشترک
دسترسی دارند و مقدار آن را به‌روزرسانی می‌کنند.

برای جلوگیری از ایجاد خطا و تداخل اطلاعات،
عملیات تغییر مقدار شمارنده درون یک Lock
قرار داده شده است.

به این ترتیب در هر لحظه فقط یک Thread
می‌تواند شمارنده را تغییر دهد و سایر Threadها
منتظر آزاد شدن قفل می‌مانند.

این روش از بروز Race Condition جلوگیری کرده
و صحت داده‌های مشترک را در محیط چندنخی
تضمین می‌کند.
        '''
    }
