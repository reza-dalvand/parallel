import time
import threading
import io
import sys


def my_func(thread_number, output_buffer):
    message = f'my_func called by thread N°{thread_number}\n'
    output_buffer.write(message)


def scenario_1():
    output_buffer = io.StringIO()

    threads = []
    for i in range(10):
        t = threading.Thread(target=my_func, args=(i, output_buffer))
        threads.append(t)
        t.start()
        t.join()

    output = output_buffer.getvalue()
    output_buffer.close()

    explanation = """
در این سناریو ۱۰ نخ (Thread) ایجاد می‌شود،
اما به دلیل استفاده از دستور join() بلافاصله پس از start()،
هر نخ باید قبل از شروع نخ بعدی به پایان برسد.

در نتیجه پردازش به صورت ترتیبی انجام شده
و اجرای همزمان میان نخ‌ها رخ نمی‌دهد.

هدف این سناریو آشنایی با نحوه ایجاد، اجرا
و مدیریت Threadها است و تأثیر پردازش موازی
بر عملکرد سیستم را نشان نمی‌دهد.
    """

    return {
        'output': output.strip(),
        'explanation': explanation.strip(),
    }



def my_func2():
    print(threading.current_thread().getName(), 'Starting')
    time.sleep(1)
    print(threading.current_thread().getName(), 'Exiting')


def scenario_2():
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    threads = []

    for i in range(10):
        t = threading.Thread(target=my_func2)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    sys.stdout = sys.__stdout__
    output = output_buffer.getvalue()

    explanation = """
در این سناریو ۱۰ نخ به صورت همزمان
ایجاد و اجرا می‌شوند.

تمامی Threadها ابتدا با استفاده از start()
آغاز به کار کرده و سپس برنامه با join()
منتظر پایان آن‌ها می‌ماند.

از آنجا که وظایف به طور موازی اجرا می‌شوند،
زمان کلی پردازش کاهش می‌یابد و منابع سیستم
به شکل کارآمدتری مورد استفاده قرار می‌گیرند.

این روش نمونه‌ای از به‌کارگیری پردازش موازی
برای افزایش سرعت اجرای برنامه است.
    """

    return {
        'output': output,
        'explanation': explanation.strip()
    }



def my_func3(worker_name, delay, counter):
    print(f"{worker_name} started")
    time.sleep(delay)
    counter['completed'] += 1
    print(f"{worker_name} finished (total completed: {counter['completed']})")

def scenario_3():
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    counter = {'completed': 0}

    high_priority = [('Worker-HIGH-1', 0.2), ('Worker-HIGH-2', 0.2)]
    low_priority = [('Worker-LOW-1', 0.3), ('Worker-LOW-2', 0.3), ('Worker-LOW-3', 0.3)]

    start_time = time.time()

    print("=== High Priority Workers (start first) ===")
    high_threads = []
    for name, delay in high_priority:
        t = threading.Thread(target=my_func3, args=(name, delay, counter), name=name)
        high_threads.append(t)
        t.start()

    time.sleep(0.05)

    print("\n=== Low Priority Workers (start after) ===")
    low_threads = []
    for name, delay in low_priority:
        t = threading.Thread(target=my_func3, args=(name, delay, counter), name=name)
        low_threads.append(t)
        t.start()

    for t in high_threads + low_threads:
        t.join()

    sys.stdout = sys.__stdout__
    output = output_buffer.getvalue()

    explanation = """
در این سناریو وظایف به دو گروه
با اولویت بالا و پایین تقسیم شده‌اند.

ابتدا Threadهای با اولویت بالا اجرا می‌شوند
و پس از یک تأخیر کوتاه، Threadهای با اولویت پایین
آغاز به کار می‌کنند.

به دلیل شروع زودتر و زمان اجرای کمتر،
وظایف مهم‌تر سریع‌تر تکمیل می‌شوند.

این مدل شبیه‌سازی ساده‌ای از سیستم‌های
زمان‌بندی اولویت‌محور است که در آن منابع
ابتدا به پردازش‌های حیاتی اختصاص داده می‌شوند.
    """

    return {
        'output': output,
        'explanation': explanation.strip()
    }
