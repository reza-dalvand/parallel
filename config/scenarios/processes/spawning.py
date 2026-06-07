import multiprocessing
import io


def myFunc(i, queue):
    output = f'calling myFunc from process n°: {i}\n'

    for j in range(0, i):
        output += f'output from myFunc is :{j}\n'

    queue.put(output)


def scenario_1():
    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    for i in range(6):
        process = multiprocessing.Process(
            target=myFunc,
            args=(i, queue)
        )

        process.start()

        process.join()

        if not queue.empty():
            output_buffer.write(queue.get())

    output_buffer.write('Processing complete!\n')

    result = output_buffer.getvalue()
    output_buffer.close()

    return {
        'output': result,
        'explanation': '''
سناریو ۱: اجرای ترتیبی Processها

در این سناریو شش Process مستقل ایجاد می‌شود.

به دلیل استفاده از دستور join() بلافاصله
پس از start()، هر Process باید ابتدا
به پایان برسد تا Process بعدی آغاز شود.

در نتیجه تمامی Processها به صورت ترتیبی
اجرا می‌شوند و پردازش همزمانی میان آن‌ها
اتفاق نمی‌افتد.

این سناریو برای آشنایی با نحوه ایجاد،
اجرا، همگام‌سازی و پایان یافتن Processها
مورد استفاده قرار می‌گیرد.

همچنین نشان می‌دهد که استفاده از Process
به تنهایی به معنای اجرای موازی نیست و
نحوه مدیریت آن‌ها تعیین‌کننده رفتار برنامه است.
'''
    }


def scenario_2():
    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    output_buffer.write(
        'START: 2 PARENTS AND 3 CHILDREN\n\n'
    )

    output_buffer.write(
        '[Parent 1] Starting work - Creating Child 0 and Child 1\n'
    )

    for i in range(2):
        output_buffer.write(
            f'[Parent 1] Creating Child {i}...\n'
        )

        process = multiprocessing.Process(
            target=myFunc,
            args=(i, queue)
        )

        process.start()
        process.join()

        if not queue.empty():
            output_buffer.write(queue.get())

        output_buffer.write(
            f'[Parent 1] Child {i} completed ✓\n\n'
        )

    output_buffer.write(
        '[Parent 1] Finished all tasks!\n\n'
    )

    output_buffer.write(
        '[Parent 2] Starting work - Creating Child 2\n'
    )

    output_buffer.write(
        '[Parent 2] Creating Child 2...\n'
    )

    process = multiprocessing.Process(
        target=myFunc,
        args=(2, queue)
    )

    process.start()
    process.join()

    if not queue.empty():
        output_buffer.write(queue.get())

    output_buffer.write(
        '[Parent 2] Child 2 completed ✓\n\n'
    )

    output_buffer.write(
        '[Parent 2] Finished all tasks!\n\n'
    )

    result = output_buffer.getvalue()
    output_buffer.close()

    return {
        'output': result,
        'explanation': '''
سناریو ۲: دو والد و سه فرزند

در این سناریو ساختار اجرای برنامه به صورت
دو والد و سه فرزند سازمان‌دهی شده است.

والد اول دو Process فرزند ایجاد می‌کند
و پس از پایان هر فرزند، فرزند بعدی را
راه‌اندازی می‌کند.

پس از اتمام کار والد اول، والد دوم
یک Process فرزند دیگر ایجاد کرده و
منتظر پایان اجرای آن می‌ماند.

استفاده از join() باعث می‌شود هر فرزند
قبل از ادامه اجرای والد به پایان برسد.

این سناریو نحوه مدیریت چند Process فرزند
توسط یک Process والد و کنترل ترتیب اجرای
آن‌ها را نمایش می‌دهد.
'''
    }


def scenario_3():
    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    output_buffer.write(
        'START: 3 PARENTS AND 3 CHILDREN \n\n'
    )

    for parent_id in range(3):

        child_id = parent_id

        output_buffer.write(
            f'[Parent {parent_id + 1}] Starting work - Creating Child {child_id}\n'
        )

        process = multiprocessing.Process(
            target=myFunc,
            args=(child_id, queue)
        )

        process.start()
        process.join()

        if not queue.empty():
            output_buffer.write(queue.get())

        output_buffer.write(
            f'[Parent {parent_id + 1}] Child {child_id} completed ✓\n'
        )

        output_buffer.write(
            f'[Parent {parent_id + 1}] Finished all tasks!\n\n'
        )

    result = output_buffer.getvalue()
    output_buffer.close()

    return {
        'output': result,
        'explanation': '''
سناریو ۳: سه والد و سه فرزند

در این سناریو سه والد مستقل در نظر گرفته شده‌اند
که هر کدام مسئول ایجاد یک Process فرزند هستند.

هر والد ابتدا Process فرزند خود را ایجاد کرده،
سپس با استفاده از join() منتظر پایان اجرای
آن باقی می‌ماند.

پس از اتمام فرزند، والد کار خود را
به پایان رسانده و نوبت به والد بعدی
می‌رسد.

این ساختار یک رابطه یک‌به‌یک میان والد
و فرزند را شبیه‌سازی می‌کند و نحوه
مدیریت و همگام‌سازی Processها را نشان می‌دهد.

این سناریو برای درک بهتر مفهوم ایجاد،
اجرا و کنترل Processهای فرزند توسط
Processهای والد کاربرد دارد.
'''
    }