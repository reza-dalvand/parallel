import threading
import time
import io
import sys


def function_A():
    print(threading.currentThread().getName() + '--> starting')
    time.sleep(1)
    print(threading.currentThread().getName() + '--> exiting')


def function_B():
    print(threading.currentThread().getName() + '--> starting')
    time.sleep(1)
    print(threading.currentThread().getName() + '--> exiting')


def function_C():
    print(threading.currentThread().getName() + '--> starting')
    time.sleep(1)
    print(threading.currentThread().getName() + '--> exiting')


def scenario_1():
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    t1 = threading.Thread(name='function_A', target=function_A)
    t2 = threading.Thread(name='function_B', target=function_B)
    t3 = threading.Thread(name='function_C', target=function_C)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    sys.stdout = sys.__stdout__
    output = output_buffer.getvalue()

    explanation = """
در این سناریو برای هر Thread یک نام اختصاصی
در نظر گرفته می‌شود و با استفاده از متد
currentThread().getName() نام Thread در حال اجرا
نمایش داده می‌شود.

هر سه Thread به صورت همزمان شروع به کار می‌کنند
و عملیات خود را مستقل از یکدیگر انجام می‌دهند.

این روش برای شناسایی، مدیریت و ردیابی Threadها
در برنامه‌های چندنخی بسیار کاربردی است
و فرآیند دیباگ و ثبت گزارش‌ها را ساده‌تر می‌کند.
    """

    return {
        'output': output,
        'explanation': explanation.strip()
    }


def scenario_2():
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    def my_func(name, delay):
        print(f"[{name}] Starting (delay: {delay}s)")
        time.sleep(delay)
        print(f"[{name}] Finished")

    threads_info = [
        ('Thread-A', 1.0),
        ('Thread-B', 0.5),
        ('Thread-C', 1.5),
        ('Thread-D', 0.3),
        ('Thread-E', 1.0)
    ]

    for name, delay in threads_info:
        t = threading.Thread(target=my_func, args=(name, delay))
        t.start()
        t.join()

    sys.stdout = sys.__stdout__

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو هر Thread پس از ایجاد شدن
بلافاصله با دستور join() منتظر اتمام کار خود می‌ماند.

به همین دلیل تا زمانی که Thread فعلی پایان نیابد،
Thread بعدی اجرا نخواهد شد.

در نتیجه تمام وظایف به صورت ترتیبی انجام می‌شوند
و هیچ پردازش موازی واقعی رخ نمی‌دهد.

این روش زمانی مناسب است که اجرای هر مرحله
به نتیجه مرحله قبل وابسته باشد.
        '''
    }


def scenario_3():
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    def my_func(name, delay):
        print(f"[{name}] Starting (delay: {delay}s)")
        time.sleep(delay)
        print(f"[{name}] Finished")

    fast_tasks = [
        ('Fast-1', 0.3),
        ('Fast-2', 0.5),
        ('Fast-3', 0.4)
    ]

    slow_tasks = [
        ('Slow-1', 1.5),
        ('Slow-2', 1.8)
    ]

    fast_threads = []
    for name, delay in fast_tasks:
        t = threading.Thread(target=my_func, args=(name, delay))
        t.start()
        fast_threads.append(t)

    for t in fast_threads:
        t.join()


    slow_threads = []
    for name, delay in slow_tasks:
        t = threading.Thread(target=my_func, args=(name, delay))
        t.start()
        slow_threads.append(t)

    for t in slow_threads:
        t.join()

    sys.stdout = sys.__stdout__

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو وظایف در دو گروه مجزا سازمان‌دهی می‌شوند.
ابتدا Threadهای مربوط به کارهای سریع اجرا شده
و پس از اتمام کامل آن‌ها، گروه دوم آغاز می‌شود.

گروه دوم شامل وظایفی است که زمان اجرای بیشتری دارند
و به صورت موازی در همان دسته اجرا می‌شوند.

این ساختار باعث مدیریت بهتر منابع سیستم شده
و از ایجاد بار بیش از حد روی پردازنده جلوگیری می‌کند.

اجرای دسته‌ای در پروژه‌هایی که دارای وظایف
با اولویت یا حجم پردازشی متفاوت هستند
کارایی و کنترل بیشتری فراهم می‌کند.
        '''
    }
