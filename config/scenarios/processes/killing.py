import multiprocessing
import time


def foo(output_queue, task_name, duration):
    output_queue.put(f"{task_name}: Starting...")
    for i in range(duration):
        time.sleep(1)
        output_queue.put(f"{task_name}: Working... {i + 1}/{duration}")
    output_queue.put(f"{task_name}: Completed!")


def scenario_1():
    output_queue = multiprocessing.Queue()
    outputs = []

    p = multiprocessing.Process(
        target=foo,
        args=(output_queue, "TerminateDemo", 10),
        name="Process-1"
    )
    p.daemon = False

    outputs.append(f"Process before execution: {p} {p.is_alive()}")

    p.start()
    outputs.append(f"Process running: {p} {p.is_alive()}")

    time.sleep(2)

    p.terminate()
    outputs.append(f"Process terminated: {p} {p.is_alive()}")

    p.join()
    outputs.append(f"Process joined: {p} {p.is_alive()}")

    outputs.append(f"Process exit code: {p.exitcode}")

    queue_outputs = []
    while not output_queue.empty():
        queue_outputs.append(output_queue.get())

    queue_text = "\n".join(queue_outputs)

    return {
        'queue_output': queue_text,
        'explanation': '''
        در این سناریو یک Process ایجاد می‌شود
و پس از شروع اجرا، برای مدت کوتاهی
به فعالیت خود ادامه می‌دهد.

بعد از چند ثانیه، Process با استفاده از
دستور terminate() به صورت اجباری
متوقف می‌شود و فرصت تکمیل وظیفه خود
را نخواهد داشت.

پس از توقف، با استفاده از join()
منتظر پایان کامل Process می‌مانیم
و وضعیت نهایی آن بررسی می‌شود.

در انتها مقدار exitcode نمایش داده می‌شود
تا مشخص شود Process به صورت طبیعی
خاتمه یافته یا به شکل اجباری متوقف شده است.

این سناریو نحوه مدیریت چرخه حیات Process
و متوقف کردن دستی آن را نمایش می‌دهد.
        '''
    }


def scenario_2():
    output_queue = multiprocessing.Queue()
    outputs = []

    p_daemon = multiprocessing.Process(
        target=foo,
        args=(output_queue, "DaemonProcess", 5),
        name="Process-Daemon"
    )
    p_daemon.daemon = True

    p_normal = multiprocessing.Process(
        target=foo,
        args=(output_queue, "NormalProcess", 3),
        name="Process-Normal"
    )
    p_normal.daemon = False

    outputs.append(f"Daemon process before execution: {p_daemon} daemon={p_daemon.daemon} alive={p_daemon.is_alive()}")
    outputs.append(f"Normal process before execution: {p_normal} daemon={p_normal.daemon} alive={p_normal.is_alive()}")

    p_daemon.start()
    p_normal.start()

    outputs.append(f"Daemon process started: {p_daemon} alive={p_daemon.is_alive()}")
    outputs.append(f"Normal process started: {p_normal} alive={p_normal.is_alive()}")

    p_normal.join()

    outputs.append(f"Normal process finished: {p_normal} alive={p_normal.is_alive()} exitcode={p_normal.exitcode}")

    outputs.append(f"Daemon process status: {p_daemon} alive={p_daemon.is_alive()}")

    queue_outputs = []
    while not output_queue.empty():
        queue_outputs.append(output_queue.get())

    queue_text = "\n".join(queue_outputs)

    return {
        'queue_output': queue_text,
        'explanation': '''
        در این سناریو دو Process به صورت همزمان
ایجاد و اجرا می‌شوند.

یکی از Processها به عنوان Daemon
و دیگری به عنوان Process عادی
تعریف شده است.

Process عادی به صورت کامل اجرا شده
و برنامه اصلی منتظر پایان آن می‌ماند،
اما Process Daemon وابسته به
عمر برنامه اصلی است.

در صورتی که برنامه اصلی خاتمه یابد،
Process Daemon نیز به صورت خودکار
متوقف خواهد شد، حتی اگر هنوز
کار آن به پایان نرسیده باشد.

این سناریو تفاوت میان Processهای
Daemon و Non-Daemon را در نحوه
مدیریت و خاتمه اجرا نشان می‌دهد.
        '''
    }


def scenario_3():
    output_queue = multiprocessing.Queue()
    outputs = []

    p_fast = multiprocessing.Process(
        target=foo,
        args=(output_queue, "FastProcess", 2),
        name="Process-Fast"
    )
    p_fast.daemon = False

    outputs.append(f"Fast process before execution: {p_fast} {p_fast.is_alive()}")

    p_fast.start()
    outputs.append(f"Fast process started: {p_fast} {p_fast.is_alive()}")

    p_fast.join(timeout=5)

    if p_fast.is_alive():
        outputs.append(f"Fast process timeout: {p_fast} still alive, terminating...")
        p_fast.terminate()
        p_fast.join()
    else:
        outputs.append(f"Fast process completed: {p_fast} alive={p_fast.is_alive()} exitcode={p_fast.exitcode}")

    # when the process will have timeout
    p_slow = multiprocessing.Process(
        target=foo,
        args=(output_queue, "SlowProcess", 10),
        name="Process-Slow"
    )
    p_slow.daemon = False

    outputs.append(f"Slow process before execution: {p_slow} {p_slow.is_alive()}")

    p_slow.start()
    outputs.append(f"Slow process started: {p_slow} {p_slow.is_alive()}")

    p_slow.join(timeout=3)

    if p_slow.is_alive():
        outputs.append(f"Slow process timeout: {p_slow} still alive, terminating...")
        p_slow.terminate()
        p_slow.join()
        outputs.append(f"Slow process terminated: {p_slow} alive={p_slow.is_alive()} exitcode={p_slow.exitcode}")
    else:
        outputs.append(f"Slow process completed: {p_slow} alive={p_slow.is_alive()} exitcode={p_slow.exitcode}")

    queue_outputs = []
    while not output_queue.empty():
        queue_outputs.append(output_queue.get())

    queue_text = "\n".join(queue_outputs)

    return {
        'queue_output': queue_text,
        'explanation': '''
        در این سناریو برای کنترل مدت زمان اجرای
Processها از دستور join(timeout)
استفاده می‌شود.

ابتدا یک Process با زمان اجرای کوتاه
ایجاد می‌شود و برنامه برای مدت مشخصی
منتظر پایان آن می‌ماند.

در صورتی که Process در زمان تعیین‌شده
به پایان برسد، اجرای آن به صورت طبیعی
خاتمه پیدا می‌کند.

سپس یک Process دیگر با زمان اجرای طولانی‌تر
راه‌اندازی می‌شود و در صورت عبور از
حد مجاز زمانی، با استفاده از terminate()
متوقف می‌گردد.

این روش برای مدیریت وظایف زمان‌حساس
و جلوگیری از اشغال طولانی‌مدت منابع سیستم
کاربرد فراوانی دارد.
        '''
    }

