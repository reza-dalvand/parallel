import multiprocessing
import time


def foo(q):
    """
    تابع اصلی که توسط هر پراسس اجرا می‌شود
    """
    name = multiprocessing.current_process().name

    # ارسال پیام شروع
    q.put(f'Starting {name}')

    # تاخیر کوچک تا هر دو پراسس پیام Starting را ارسال کنند
    time.sleep(0.1)

    # تعیین محدوده اعداد بر اساس نام پراسس
    if name == 'background_process':
        numbers = range(0, 5)
    else:  # NO_background_process
        numbers = range(5, 10)

    # چاپ اعداد
    for i in numbers:
        q.put(f'---> {i}')
        time.sleep(0.01)

    # ارسال پیام پایان
    q.put(f'Exiting {name}')


def scenario_1():
    """
    سناریو 1: اجرای پراسس‌های Background و Foreground
    """
    output_queue = multiprocessing.Queue()

    # ساخت پراسس‌ها
    NO_background_process = multiprocessing.Process(
        name='NO_background_process',
        target=foo,
        args=(output_queue,)
    )
    NO_background_process.daemon = False

    background_process = multiprocessing.Process(
        name='background_process',
        target=foo,
        args=(output_queue,)
    )
    background_process.daemon = False

    # شروع همزمان
    NO_background_process.start()
    background_process.start()

    # چاپ real-time
    outputs = []
    while NO_background_process.is_alive() or background_process.is_alive() or not output_queue.empty():
        try:
            msg = output_queue.get(timeout=0.01)
            print(msg)
            outputs.append(msg)
        except:
            continue

    # منتظر اتمام
    NO_background_process.join()
    background_process.join()

    return {
        'output': '\n'.join(outputs),
        'explanation': 'دو پراسس به صورت موازی اجرا می‌شوند'
    }



def foo_daemon(output_queue):
    """
    تابع برای سناریو daemon که بسته به نوع پراسس
    اعداد متفاوتی چاپ می‌کند
    """
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
    """
    سناریو 2: تأثیر daemon=True

    ساختار:
    - پراسس اول: daemon_process (daemon=True)
    - پراسس دوم: non_daemon_process (daemon=False)
    - daemon_process اعداد 0-4 را با تاخیر بیشتر چاپ می‌کند
    - non_daemon_process اعداد 5-9 را با تاخیر کمتر چاپ می‌کند
    - daemon_process با اتمام برنامه اصلی قطع می‌شود
    """
    output_queue = multiprocessing.Queue()

    # ساخت پراسس‌ها
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

    # شروع همزمان
    daemon_process.start()
    non_daemon_process.start()

    # فقط منتظر non-daemon می‌مانیم
    non_daemon_process.join()

    # کمی صبر می‌کنیم تا daemon هم کمی کار کند
    time.sleep(0.1)

    # جمع‌آوری خروجی‌ها
    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': 'daemon_process با اتمام برنامه اصلی قطع می‌شود و کارش ناقص می‌ماند، در حالی که non_daemon_process کامل اجرا می‌شود'
    }


def foo_lock(output_queue, lock):
    """
    تابع برای سناریو Lock که از قفل برای همگام‌سازی استفاده می‌کند
    """
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
    """
    سناریو 3: استفاده از Lock برای همگام‌سازی

    ساختار:
    - پراسس اول: process_A (daemon=False)
    - پراسس دوم: process_B (daemon=False)
    - استفاده از Lock برای اطمینان از اجرای ترتیبی
    - process_A اعداد 0-4 را چاپ می‌کند
    - process_B اعداد 5-9 را چاپ می‌کند
    - خروجی‌ها بدون تداخل و پشت سر هم هستند
    """
    output_queue = multiprocessing.Queue()
    lock = multiprocessing.Lock()

    # ساخت پراسس‌ها
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

    # شروع همزمان
    process_A.start()
    process_B.start()

    # منتظر اتمام همه
    process_A.join()
    process_B.join()

    # جمع‌آوری خروجی‌ها
    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': 'با استفاده از Lock، هر پراسس تمام کارش را قبل از شروع پراسس دیگر انجام می‌دهد - خروجی‌ها بدون تداخل هستند'
    }



