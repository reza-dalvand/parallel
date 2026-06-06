import multiprocessing
import time


def foo(output_queue, task_name, duration):
    """تابع worker که خروجی‌ها را به queue می‌فرستد"""
    output_queue.put(f"{task_name}: Starting...")
    for i in range(duration):
        time.sleep(1)
        output_queue.put(f"{task_name}: Working... {i + 1}/{duration}")
    output_queue.put(f"{task_name}: Completed!")


def scenario_1():
    """سناریو اول: Killing a Process"""
    output_queue = multiprocessing.Queue()
    outputs = []

    # ایجاد پراسس
    p = multiprocessing.Process(
        target=foo,
        args=(output_queue, "TerminateDemo", 10),
        name="Process-1"
    )
    p.daemon = False

    # قبل از اجرا
    outputs.append(f"Process before execution: {p} {p.is_alive()}")

    # شروع پراسس
    p.start()
    outputs.append(f"Process running: {p} {p.is_alive()}")

    # اجازه اجرا برای مدت کوتاه
    time.sleep(2)

    # terminate کردن پراسس
    p.terminate()
    outputs.append(f"Process terminated: {p} {p.is_alive()}")

    # join کردن پراسس
    p.join()
    outputs.append(f"Process joined: {p} {p.is_alive()}")

    # نمایش exit code
    outputs.append(f"Process exit code: {p.exitcode}")

    # جمع‌آوری خروجی‌های queue
    queue_outputs = []
    while not output_queue.empty():
        queue_outputs.append(output_queue.get())

    # تبدیل لیست‌ها به رشته
    output_text = "\n".join(outputs)
    queue_text = "\n".join(queue_outputs)

    return {
        'output': output_text,
        'queue_output': queue_text,
        'explanation': 'سناریو اول: نمایش چرخه حیات پراسس و terminate کردن دستی آن. پراسس قبل از اتمام کار، با terminate() متوقف می‌شود و exitcode برابر -15 (SIGTERM) است.'
    }


def scenario_2():
    """سناریو دوم: Daemon Process"""
    output_queue = multiprocessing.Queue()
    outputs = []

    # ایجاد دو پراسس: daemon و non-daemon
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

    # نمایش وضعیت اولیه
    outputs.append(f"Daemon process before execution: {p_daemon} daemon={p_daemon.daemon} alive={p_daemon.is_alive()}")
    outputs.append(f"Normal process before execution: {p_normal} daemon={p_normal.daemon} alive={p_normal.is_alive()}")

    # شروع هر دو پراسس
    p_daemon.start()
    p_normal.start()

    outputs.append(f"Daemon process started: {p_daemon} alive={p_daemon.is_alive()}")
    outputs.append(f"Normal process started: {p_normal} alive={p_normal.is_alive()}")

    # فقط منتظر non-daemon می‌مانیم
    p_normal.join()

    outputs.append(f"Normal process finished: {p_normal} alive={p_normal.is_alive()} exitcode={p_normal.exitcode}")

    # daemon process هنوز در حال اجراست اما برنامه اصلی تمام می‌شود
    outputs.append(f"Daemon process status: {p_daemon} alive={p_daemon.is_alive()}")

    # جمع‌آوری خروجی‌های queue
    queue_outputs = []
    while not output_queue.empty():
        queue_outputs.append(output_queue.get())

    # تبدیل لیست‌ها به رشته
    output_text = "\n".join(outputs)
    queue_text = "\n".join(queue_outputs)

    return {
        'output': output_text,
        'queue_output': queue_text,
        'explanation': 'سناریو دوم: مقایسه daemon و non-daemon process. پراسس daemon به محض اتمام برنامه اصلی، خودکار terminate می‌شود بدون نیاز به join() یا terminate(). پراسس normal باید به صورت صریح join شود.'
    }


def scenario_3():
    """سناریو سوم: Process with Timeout"""
    output_queue = multiprocessing.Queue()
    outputs = []

    # حالت اول: پراسسی که در timeout تمام می‌شود
    p_fast = multiprocessing.Process(
        target=foo,
        args=(output_queue, "FastProcess", 2),
        name="Process-Fast"
    )
    p_fast.daemon = False

    outputs.append(f"Fast process before execution: {p_fast} {p_fast.is_alive()}")

    p_fast.start()
    outputs.append(f"Fast process started: {p_fast} {p_fast.is_alive()}")

    # منتظر می‌مانیم با timeout 5 ثانیه
    p_fast.join(timeout=5)

    if p_fast.is_alive():
        outputs.append(f"Fast process timeout: {p_fast} still alive, terminating...")
        p_fast.terminate()
        p_fast.join()
    else:
        outputs.append(f"Fast process completed: {p_fast} alive={p_fast.is_alive()} exitcode={p_fast.exitcode}")

    # حالت دوم: پراسسی که timeout می‌شود
    p_slow = multiprocessing.Process(
        target=foo,
        args=(output_queue, "SlowProcess", 10),
        name="Process-Slow"
    )
    p_slow.daemon = False

    outputs.append(f"Slow process before execution: {p_slow} {p_slow.is_alive()}")

    p_slow.start()
    outputs.append(f"Slow process started: {p_slow} {p_slow.is_alive()}")

    # منتظر می‌مانیم با timeout 3 ثانیه
    p_slow.join(timeout=3)

    if p_slow.is_alive():
        outputs.append(f"Slow process timeout: {p_slow} still alive, terminating...")
        p_slow.terminate()
        p_slow.join()
        outputs.append(f"Slow process terminated: {p_slow} alive={p_slow.is_alive()} exitcode={p_slow.exitcode}")
    else:
        outputs.append(f"Slow process completed: {p_slow} alive={p_slow.is_alive()} exitcode={p_slow.exitcode}")

    # جمع‌آوری خروجی‌های queue
    queue_outputs = []
    while not output_queue.empty():
        queue_outputs.append(output_queue.get())

    # تبدیل لیست‌ها به رشته
    output_text = "\n".join(outputs)
    queue_text = "\n".join(queue_outputs)

    return {
        'output': output_text,
        'queue_output': queue_text,
        'explanation': 'سناریو سوم: مدیریت پراسس با timeout. از join(timeout) برای تعیین حداکثر زمان انتظار استفاده می‌شود. اگر پراسس در زمان مشخص تمام نشود، با terminate() متوقف می‌شود. این الگو برای taskهای time-sensitive مناسب است.'
    }

