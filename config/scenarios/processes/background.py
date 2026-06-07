import multiprocessing
import time
import io


def foo(output_queue):
    name = multiprocessing.current_process().name

    output_queue.put(f"Starting {name}")

    if name == 'background_process':
        for i in range(0, 5):
            output_queue.put(f'---> {i}')
            time.sleep(1)
    else:
        for i in range(5, 10):
            output_queue.put(f'---> {i}')
            time.sleep(1)

    output_queue.put(f"Exiting {name}")


def scenario_1():
    output_buffer = io.StringIO()
    output_queue = multiprocessing.Queue()

    background_process = multiprocessing.Process(
        name='background_process',
        target=foo,
        args=(output_queue,)
    )
    background_process.daemon = True

    no_background_process = multiprocessing.Process(
        name='NO_background_process',
        target=foo,
        args=(output_queue,)
    )
    no_background_process.daemon = False

    background_process.start()
    no_background_process.start()

    no_background_process.join()

    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_buffer.write("\n".join(outputs))

    return {
        "output": output_buffer.getvalue(),
        "explanation": """
سناریو ۱: اجرای Processهای Daemon و Non-Daemon

در این سناریو دو Process به صورت همزمان اجرا می‌شوند.
Process اول به عنوان daemon اجرا می‌شود و با پایان برنامه اصلی متوقف می‌شود.
Process دوم به صورت Non-Daemon اجرا شده و برنامه تا پایان آن صبر می‌کند.

در نتیجه خروجی Process غیر دیمون کامل نمایش داده می‌شود،
اما Process دیمون ممکن است قبل از اتمام کامل متوقف شود
و فقط بخشی از خروجی آن دیده شود.
"""
    }

def foo_daemon(output_queue):
    name = multiprocessing.current_process().name
    output_queue.put(f"Starting {name}")

    if name == 'daemon_process':
        for i in range(0, 5):
            output_queue.put(f'---> {i}')
            time.sleep(0.15)  # تاخیر بیشتر برای daemon
    else:
        for i in range(5, 10):
            output_queue.put(f'---> {i}')
            time.sleep(0.05)  # تاخیر کمتر برای non-daemon

    output_queue.put(f"Exiting {name}")


def scenario_2():
    output_queue = multiprocessing.Queue()

    daemon_process = multiprocessing.Process(
        name='daemon_process',
        target=foo_daemon,
        args=(output_queue,)
    )
    daemon_process.daemon = True  # daemon است

    non_daemon_process = multiprocessing.Process(
        name='non_daemon_process',
        target=foo_daemon,
        args=(output_queue,)
    )
    non_daemon_process.daemon = False

    daemon_process.start()
    non_daemon_process.start()

    non_daemon_process.join()

    # a little wait for working daemon
    time.sleep(0.1)

    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': '''
        در این سناریو دو Process ایجاد می‌شوند
که یکی از آن‌ها به صورت Daemon و
دیگری به صورت عادی اجرا می‌شود.

Process عادی تا پایان کامل اجرای خود
به کار ادامه می‌دهد و Process اصلی
منتظر اتمام آن باقی می‌ماند.

در مقابل، Process Daemon وابسته به عمر
برنامه اصلی است و تضمینی برای تکمیل
تمام وظایف خود ندارد.

به محض پایان یافتن Processهای غیر Daemon
و خاتمه برنامه اصلی، Process Daemon
ممکن است متوقف شود.

این سناریو تفاوت میان Processهای عادی
و Daemon را نشان داده و کاربرد Daemonها
در وظایف پس‌زمینه را توضیح می‌دهد.
        '''
    }


def foo_lock(output_queue, lock):
    name = multiprocessing.current_process().name

    with lock:
        output_queue.put(f"Starting {name}")

        if name == 'process_A':
            for i in range(0, 5):
                output_queue.put(f'---> {i}')
                time.sleep(0.05)
        else:
            for i in range(5, 10):
                output_queue.put(f'---> {i}')
                time.sleep(0.05)

        output_queue.put(f"Exiting {name}")


def scenario_3():
    output_queue = multiprocessing.Queue()
    lock = multiprocessing.Lock()

    process_A = multiprocessing.Process(
        name='process_A',
        target=foo_lock,
        args=(output_queue, lock)
    )
    process_A.daemon = False

    process_B = multiprocessing.Process(
        name='process_B',
        target=foo_lock,
        args=(output_queue, lock)
    )
    process_B.daemon = False

    process_A.start()
    process_B.start()

    process_A.join()
    process_B.join()

    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': '''
        در این سناریو دو Process به صورت همزمان
ایجاد می‌شوند اما برای دسترسی به بخش
مشترک برنامه از یک Lock استفاده می‌کنند.

هر Process قبل از شروع عملیات خود
باید Lock را در اختیار بگیرد.

تا زمانی که یک Process مشغول اجرا است،
Process دیگر اجازه ورود به بخش محافظت‌شده
را نخواهد داشت.

در نتیجه خروجی هر Process به صورت کامل
و بدون تداخل با Process دیگر تولید می‌شود.

این روش برای جلوگیری از شرایط رقابتی
(Race Condition) و محافظت از منابع مشترک
در برنامه‌های چندپردازه‌ای مورد استفاده قرار می‌گیرد.
        '''
    }



