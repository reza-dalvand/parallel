import multiprocessing
import io


def myFunc(i, queue):
    output = f'calling myFunc from process n°: {i}\n'
    queue.put(output)

# Sequential 
def scenario_1():
    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    for i in range(6): #spawining 6 processes
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



# Parallel execution
# 1 Parent - 3 Children

def scenario_2():

    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    processes = []

    output_buffer.write(
        '[Main Parent] Creating 3 children\n\n'
    )

    for i in range(3):

        process = multiprocessing.Process(
            target=myFunc,
            args=(i + 1, queue)
        )

        processes.append(process)

        process.start()

    output_buffer.write(
        '[Main Parent] All children started\n\n'
    )

    # Wait for all children
    for process in processes:
        process.join()


    while not queue.empty():
        output_buffer.write(queue.get())


    output_buffer.write(
        '\n[Main Parent] All children completed ✓\n'
    )


    result = output_buffer.getvalue()
    output_buffer.close()

    return {
        'output': result,
        'explanation': '''
سناریو ۲: اجرای موازی چند Process

در این سناریو یک Parent Process
سه Child Process ایجاد می‌کند.

بر خلاف سناریو ۱، تمام Childها ابتدا
با start() اجرا می‌شوند و سپس Parent
با استفاده از join() منتظر پایان همه
آن‌ها می‌ماند.

بنابراین Child Processها می‌توانند
به صورت همزمان اجرا شوند.

این سناریو تفاوت اجرای ترتیبی و موازی
در multiprocessing را نشان می‌دهد.
'''
    }

def parent_process(parent_id, children, queue):

    output = ""

    output += (
        f'[Parent-{parent_id}] Started\n'
    )

    processes = []


    for child_id in children:

        p = multiprocessing.Process(
            target=myFunc,
            args=(child_id, queue)
        )

        processes.append(p)
        p.start()


    for p in processes:
        p.join()


    output += (
        f'[Parent-{parent_id}] All children finished ✓\n'
    )

    queue.put(output)


# 2 parent create 3 children
def scenario_3():

    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()


    parent1 = multiprocessing.Process(
        target=parent_process,
        args=(1, [1,2], queue)
    )


    parent2 = multiprocessing.Process(
        target=parent_process,
        args=(2, [3], queue)
    )


    output_buffer.write(
        'MAIN PROCESS STARTED\n\n'
    )


    parent1.start()
    parent2.start()


    parent1.join()
    parent2.join()


    while not queue.empty():
        output_buffer.write(queue.get())


    output_buffer.write(
        '\nMAIN PROCESS FINISHED ✓\n'
    )


    result = output_buffer.getvalue()
    output_buffer.close()


    return {
        'output': result,
        'explanation': '''
سناریو ۳: چند Parent و چند Child واقعی

در این سناریو Main Process
دو Parent Process ایجاد می‌کند.

هر Parent مسئول ساخت Childهای خودش است.

Parent اول دو Child ایجاد می‌کند
و Parent دوم یک Child ایجاد می‌کند.

در نتیجه یک Process Tree ایجاد می‌شود:

Main
 |
 |-- Parent 1
 |       |-- Child 1
 |       |-- Child 2
 |
 |-- Parent 2
         |-- Child 3

این سناریو مفهوم Process hierarchy
و رابطه والد و فرزند در multiprocessing
را نمایش می‌دهد.
'''
    }
