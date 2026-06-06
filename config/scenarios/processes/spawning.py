import multiprocessing
import io
import time


def myFunc(i, queue):
    """
    تابعی که توسط هر پراسس فرزند اجرا می‌شه
    اعداد از 0 تا i-1 رو چاپ می‌کنه
    """
    output = f'calling myFunc from process n°: {i}\n'
    for j in range(0, i):
        output += f'output from myFunc is :{j}\n'
    queue.put(output)


def scenario_1():
    """
    سناریو ۱: اجرای ترتیبی پراسس‌ها

    این کد مشابه الگوی Barrier است اما با multiprocessing:
    - 6 پراسس به صورت ترتیبی اجرا می‌شوند
    - هر پراسس باید تمام شود تا بعدی شروع شود
    - خروجی همه پراسس‌ها جمع‌آوری می‌شود
    """
    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    output_buffer.write('START SEQUENTIAL PROCESSING!!!!\n')

    # ساخت و اجرای 6 پراسس به صورت ترتیبی
    for i in range(6):
        # تعریف پراسس با تابع هدف و آرگومان
        process = multiprocessing.Process(target=myFunc, args=(i, queue))

        # شروع پراسس (spawning)
        process.start()

        # منتظر ماندن تا پراسس تمام شود
        process.join()

        # دریافت خروجی از queue
        if not queue.empty():
            output_buffer.write(queue.get())

    output_buffer.write('Processing complete!\n')

    result = output_buffer.getvalue()
    output_buffer.close()

    return {
        'output': result,
        'explanation': 'سناریو ۱: اجرای ترتیبی - هر پراسس بعد از اتمام پراسس قبلی شروع می‌شود'
    }


def myFunc2(i, queue):
    """تابعی که توسط هر پراسس فرزند اجرا می‌شه"""
    output = f'calling myFunc from process n°: {i}\n'
    for j in range(0, i):
        output += f'output from myFunc is :{j}\n'
    queue.put(output)


def scenario_2():
    """
    سناریو: 2 والد و 3 فرزند

    ساختار:
    - والد اول: 2 فرزند می‌سازه (فرزند 0 و 1)
    - والد دوم: 1 فرزند می‌سازه (فرزند 2)
    """
    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    output_buffer.write('=== START: 2 والد و 3 فرزند ===\n\n')

    # والد اول: می‌سازه فرزند 0 و 1
    output_buffer.write('[والد 1] شروع کار - می‌سازم فرزند 0 و 1\n')
    for i in range(2):
        output_buffer.write(f'[والد 1] دارم فرزند {i} رو می‌سازم...\n')
        process = multiprocessing.Process(target=myFunc, args=(i, queue))
        process.start()
        process.join()
        if not queue.empty():
            output_buffer.write(queue.get())
        output_buffer.write(f'[والد 1] فرزند {i} تموم شد ✓\n\n')

    output_buffer.write('[والد 1] کارم تموم شد!\n\n')

    # والد دوم: می‌سازه فرزند 2
    output_buffer.write('[والد 2] شروع کار - می‌سازم فرزند 2\n')
    output_buffer.write(f'[والد 2] دارم فرزند 2 رو می‌سازم...\n')
    process = multiprocessing.Process(target=myFunc, args=(2, queue))
    process.start()
    process.join()
    if not queue.empty():
        output_buffer.write(queue.get())
    output_buffer.write(f'[والد 2] فرزند 2 تموم شد ✓\n\n')

    output_buffer.write('[والد 2] کارم تموم شد!\n\n')
    output_buffer.write('=== همه کارها تموم شد! ===\n')

    result = output_buffer.getvalue()
    output_buffer.close()

    return {
        'output': result,
        'explanation': '2 والد: اولی 2 فرزند می‌سازه، دومی 1 فرزند'
    }


def scenario_3():
    """
    سناریو: 3 والد و 3 فرزند

    ساختار:
    - والد اول: فرزند 0 رو می‌سازه
    - والد دوم: فرزند 1 رو می‌سازه
    - والد سوم: فرزند 2 رو می‌سازه
    """
    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    output_buffer.write('=== START: 3 والد و 3 فرزند ===\n\n')

    # هر والد یک فرزند می‌سازه
    for parent_id in range(3):
        child_id = parent_id
        output_buffer.write(f'[والد {parent_id + 1}] شروع کار - می‌سازم فرزند {child_id}\n')

        process = multiprocessing.Process(target=myFunc, args=(child_id, queue))
        process.start()
        process.join()

        if not queue.empty():
            output_buffer.write(queue.get())

        output_buffer.write(f'[والد {parent_id + 1}] فرزند {child_id} تموم شد ✓\n')
        output_buffer.write(f'[والد {parent_id + 1}] کارم تموم شد!\n\n')

    output_buffer.write('=== همه کارها تموم شد! ===\n')

    result = output_buffer.getvalue()
    output_buffer.close()

    return {
        'output': result,
        'explanation': '3 والد: هر کدوم یک فرزند می‌سازن'
    }