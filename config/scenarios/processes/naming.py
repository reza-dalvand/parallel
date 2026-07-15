import multiprocessing
import random
import time


def myFunc(output_queue):
    name = multiprocessing.current_process().name
    output_queue.put(f'Starting process name = {name}')
    time.sleep(0.5)
    output_queue.put(f'Exiting process name = {name}')


def scenario_1():
    output_queue = multiprocessing.Queue()

    p1 = multiprocessing.Process(name='myFunc process', target=myFunc, args=(output_queue,))
    p2 = multiprocessing.Process(target=myFunc, args=(output_queue,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': '''
        در این سناریو دو Process مستقل ایجاد می‌شوند،
Process اول دارای یک نام سفارشی بوده و
Process دوم از نام پیش‌فرض سیستم استفاده می‌کند.

هر دو Process به صورت همزمان آغاز شده
و به طور مستقل وظایف خود را اجرا می‌کنند.

پس از شروع اجرا، Process اصلی با استفاده
از دستور join() منتظر پایان یافتن هر دو
Process باقی می‌ماند.

برای انتقال خروجی از Processهای فرزند
به Process اصلی از Queue استفاده شده است.

این سناریو نحوه نام‌گذاری Processها،
اجرای همزمان آن‌ها و تبادل داده میان
Processها را نمایش می‌دهد.
        '''
    }





def myFunc2(i, output_queue):
    delay = random.uniform(0.1, 0.5)

    output_queue.put(f'calling myFunc from process n°: {i}')
    time.sleep(delay)
    output_queue.put(f'output from myFunc is :{i}')


def scenario_2():
    output_queue = multiprocessing.Queue()

    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=myFunc2, args=(i, output_queue))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': '''
        در این سناریو چهار Process به صورت
همزمان ایجاد و اجرا می‌شوند.

ابتدا تمامی Processها با start()
آغاز به کار کرده و سپس Process اصلی
منتظر پایان همه آن‌ها می‌ماند.

از آنجا که هر Process دارای زمان اجرای
متفاوت و تصادفی است، ترتیب پایان یافتن
آن‌ها قابل پیش‌بینی نخواهد بود.

به همین دلیل خروجی Processها ممکن است
به صورت درهم‌آمیخته و با ترتیب‌های مختلف
در هر بار اجرا مشاهده شود.

این سناریو نمونه‌ای از اجرای موازی واقعی
در سطح Processها را نشان می‌دهد.
        '''
    }


def myFunc3(i, output_queue):
    output_queue.put(f'calling myFunc from process n°: {i}')
    time.sleep(0.5)
    output_queue.put(f'output from myFunc is :{i}')


def scenario_3():
    BATCH_SIZE = 2
    output_queue = multiprocessing.Queue()

    all_indices = list(range(6))  # [0, 1, 2, 3, 4, 5]

    for i in range(0, len(all_indices), BATCH_SIZE):
        batch_indices = all_indices[i:i + BATCH_SIZE]
        batch_processes = []

        for idx in batch_indices:
            p = multiprocessing.Process(target=myFunc3, args=(idx, output_queue))
            batch_processes.append(p)
            p.start()

        for p in batch_processes:
            p.join()

    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())

    output_text = '\n'.join(outputs)

    return {
        'output': output_text,
        'explanation': '''
        در این سناریو شش Process در قالب
سه دسته دو‌تایی اجرا می‌شوند.

در هر مرحله، دو Process به صورت
همزمان شروع به کار می‌کنند.

پس از پایان اجرای هر دو Process،
دسته بعدی آغاز می‌شود.

بنابراین درون هر دسته اجرای موازی وجود دارد،
اما بین دسته‌ها ترتیب اجرا حفظ می‌شود.

این روش باعث می‌شود تعداد Processهای فعال
در هر لحظه کنترل شده و مصرف منابع سیستم
مدیریت گردد.

این الگو در پردازش‌های گروهی و سیستم‌هایی
که محدودیت منابع دارند بسیار کاربردی است.
        '''
    }