import multiprocessing
import time
import io


def my_func(output_queue):
    name = multiprocessing.current_process().name

    output_queue.put(f"Starting {name}")
    time.sleep(0.1) # جهت شبیه سازی خروجی مشابه کتاب

    if name == 'background_process':
        for i in range(0, 5):
            output_queue.put(f'---> {i}')
            time.sleep(0.5)
    else:
        for i in range(5, 10):
            output_queue.put(f'---> {i}')
            time.sleep(0.5)

    output_queue.put(f"Exiting {name}")

# 0-5, 1-6, 2-7, 3-8, 4-9
def scenario_1():
    output_buffer = io.StringIO()
    output_queue = multiprocessing.Queue()

    background_process = multiprocessing.Process(
        name='background_process',
        target=my_func,
        args=(output_queue,)
    )
    background_process.daemon = True

    no_background_process = multiprocessing.Process(
        name='NO_background_process',
        target=my_func,
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






def func2(output_queue):
    name = multiprocessing.current_process().name
    output_queue.put(f"Starting {name}")
    time.sleep(0.1) # جهت شبیه سازی خروجی مشابه کتاب

    if name == 'daemon_process':
        for i in range(0, 5):
            output_queue.put(f'---> {i}')
            time.sleep(0.15)  # تاخیر بیشتر جهت متوقف کردن پراسس قبل از اتمام کار
    else:
        for i in range(5, 10):
            output_queue.put(f'---> {i}')
            time.sleep(0.05)  # تاخیر کمتر برای non-daemon

    output_queue.put(f"Exiting {name}")

# نمایش عملکرد پراسس های بک گراند بعد از اتمام پراسس فور گراند
def scenario_2():
    output_queue = multiprocessing.Queue()

    daemon_process = multiprocessing.Process(
        name='daemon_process',
        target=func2,
        args=(output_queue,)
    )
    daemon_process.daemon = True  

    non_daemon_process = multiprocessing.Process(
        name='non_daemon_process',
        target=func2,
        args=(output_queue,)
    )
    non_daemon_process.daemon = False

    daemon_process.start()
    non_daemon_process.start()

    non_daemon_process.join()

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


def monitor_process(output_queue):

    name = multiprocessing.current_process().name

    counter = 0

    output_queue.put(
        f"{name} started"
    )

    while True:

        output_queue.put(
            f"{name} monitoring... check {counter}"
        )

        counter += 1

        time.sleep(0.5)



def main_task(output_queue):

    name = multiprocessing.current_process().name

    output_queue.put(
        f"{name} started"
    )

    for i in range(5):

        output_queue.put(
            f"{name} processing task {i}"
        )

        time.sleep(1)


    output_queue.put(
        f"{name} finished"
    )



def scenario_3():

    output_queue = multiprocessing.Queue()


    monitor = multiprocessing.Process(
        name="background_monitor",
        target=monitor_process,
        args=(output_queue,)
    )

    monitor.daemon = True


    worker = multiprocessing.Process(
        name="main_worker",
        target=main_task,
        args=(output_queue,)
    )

    worker.daemon = False



    monitor.start()

    worker.start()


    worker.join()


    outputs = []

    while not output_queue.empty():

        outputs.append(
            output_queue.get()
        )


    output_text = "\n".join(outputs)


    return {

        "output": output_text,

        "explanation": '''
سناریو ۳: Background Monitor Process

در این سناریو یک Process اصلی وظیفه انجام
کارهای اصلی برنامه را دارد.

همزمان یک Process دیگر به عنوان Background
Monitor اجرا می‌شود که وضعیت برنامه را
بررسی می‌کند.

Process مانیتور به صورت Daemon اجرا شده است،
بنابراین تا زمانی که Process اصلی فعال است
کار می‌کند.

پس از پایان Process اصلی، برنامه پایان یافته
و Process پس‌زمینه نیز به صورت خودکار
متوقف می‌شود.

این الگو در سیستم‌های واقعی برای کارهایی
مانند Logging، Monitoring و Health Check
استفاده می‌شود.
'''
    }


