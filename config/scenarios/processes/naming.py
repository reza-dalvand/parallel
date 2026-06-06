import multiprocessing
import random
import time


def myFunc(output_queue):
    """
    تابع ساده که نام پراسس رو به Queue می‌فرسته
    """
    name = multiprocessing.current_process().name
    output_queue.put(f'Starting process name = {name}')
    time.sleep(0.5)  # شبیه‌سازی کار
    output_queue.put(f'Exiting process name = {name}')


def scenario_1():
    """
    سناریو 1: نام‌گذاری پراسس‌ها با اجرای موازی

    ساختار:
    - پراسس اول: نام دلخواه "myFunc process"
    - پراسس دوم: نام پیش‌فرض "Process-2"
    - اجرای موازی (همه start بعد همه join)
    - استفاده از Queue برای جمع‌آوری خروجی
    """
    output_queue = multiprocessing.Queue()

    # ساخت پراسس‌ها
    p1 = multiprocessing.Process(name='myFunc process', target=myFunc, args=(output_queue,))
    p2 = multiprocessing.Process(target=myFunc, args=(output_queue,))

    # شروع همزمان همه پراسس‌ها
    p1.start()
    p2.start()

    # منتظر اتمام همه
    p1.join()
    p2.join()

    # جمع‌آوری خروجی‌ها
    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': 'پراسس اول نام دلخواه دارد، پراسس دوم نام پیش‌فرض - اجرای موازی با Queue'
    }


def myFunc2(i, output_queue):
    """
    تابع با تاخیر تصادفی برای نشان دادن موازی بودن واقعی
    """
    # تاخیر تصادفی برای شبیه‌سازی کار واقعی
    delay = random.uniform(0.1, 0.5)

    output_queue.put(f'calling myFunc from process n°: {i}')
    time.sleep(delay)  # هر پراسس زمان متفاوتی طول می‌کشه
    output_queue.put(f'output from myFunc is :{i}')


def scenario_2():
    """
    سناریو 2: اجرای کاملاً موازی (واقعاً بی‌ترتیب)

    ساختار:
    - 4 پراسس
    - همه با start() شروع می‌شن (موازی)
    - بعد همه با join() منتظر می‌مونیم
    - زمان اجرا: max(T_i) ≈ 0.1~0.5s
    - خروجی: کاملاً interleaved و غیرقابل پیش‌بینی
    """
    output_queue = multiprocessing.Queue()

    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=myFunc2, args=(i, output_queue))
        processes.append(p)

    # شروع همزمان همه پراسس‌ها
    for p in processes:
        p.start()

    # منتظر اتمام همه
    for p in processes:
        p.join()

    # جمع‌آوری خروجی‌ها
    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': 'همه پراسس‌ها همزمان شروع می‌شن - ترتیب اتمام غیرقابل پیش‌بینی - خروجی‌ها واقعاً interleaved'
    }


def myFunc3(i, output_queue):
    """
    تابع ساده که خروجی رو به queue می‌فرسته
    """
    output_queue.put(f'calling myFunc from process n°: {i}')
    time.sleep(0.5)  # شبیه‌سازی کار
    output_queue.put(f'output from myFunc is :{i}')


def scenario_3():
    """
    سناریو 3: اجرای دسته‌ای

    ساختار:
    - 6 پراسس در 3 دسته (هر دسته 2 تایی)
    - هر دسته به صورت موازی اجرا می‌شه
    - دسته‌ها به صورت ترتیبی اجرا می‌شن
    - زمان اجرا: 3 × 0.5s = 1.5s
    - خروجی: داخل هر دسته interleaved، بین دسته‌ها ترتیبی
    """
    BATCH_SIZE = 2
    output_queue = multiprocessing.Queue()

    all_indices = list(range(6))  # [0, 1, 2, 3, 4, 5]

    # اجرای دسته‌ای
    for i in range(0, len(all_indices), BATCH_SIZE):
        batch_indices = all_indices[i:i + BATCH_SIZE]
        batch_processes = []

        # ساخت و شروع همزمان پراسس‌های این دسته
        for idx in batch_indices:
            p = multiprocessing.Process(target=myFunc3, args=(idx, output_queue))
            batch_processes.append(p)
            p.start()

        # منتظر اتمام این دسته
        for p in batch_processes:
            p.join()

    # جمع‌آوری خروجی‌ها
    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': 'هر دسته 2 تایی موازی اجرا می‌شه - دسته‌ها ترتیبی هستن - زمان کل ≈ 1.5s'
    }