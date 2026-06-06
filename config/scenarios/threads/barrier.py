import threading
import time
import random
import io

def scenario_1():
    output_buffer = io.StringIO()

    num_runners = 3
    finish_line = threading.Barrier(num_runners)
    runners = ['Huey', 'Dewey', 'Louie']

    def runner():
        name = runners.pop()
        sleep_time = random.randrange(2, 5)
        time.sleep(sleep_time)
        arrival_time = time.strftime('%a %b %d %H:%M:%S %Y')
        message = f'{name} reached the barrier at: {arrival_time}'
        output_buffer.write(message + '\n')
        finish_line.wait()

    output_buffer.write('START RACE!!!!\n')

    threads = []
    for i in range(num_runners):
        t = threading.Thread(target=runner)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    output_buffer.write('Race over!\n')

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
        در این سناریو سه Thread به صورت همزمان
شروع به اجرا می‌کنند و هر کدام پس از
انجام بخشی از کار خود به یک Barrier می‌رسند.

Barrier باعث می‌شود هیچ Threadی نتواند
به مرحله بعد وارد شود تا زمانی که
همه Threadها به نقطه تعیین‌شده برسند.

پس از رسیدن آخرین Thread، مانع برداشته شده
و همه Threadها به صورت همزمان ادامه می‌دهند.

این روش برای هماهنگ‌سازی چند وظیفه موازی
و اطمینان از تکمیل یک مرحله مشترک
قبل از شروع مرحله بعد کاربرد دارد.
        '''
    }


#Scenario 2: Multiple Phases with Barrier
def scenario_2():
    output_buffer = io.StringIO()

    num_workers = 3
    num_phases = 3

    barrier = threading.Barrier(num_workers)

    def worker(worker_id):
        for phase in range(num_phases):

            output_buffer.write(
                f'Worker-{worker_id} started Phase-{phase + 1}\n'
            )

            time.sleep(random.uniform(0.5, 2))

            output_buffer.write(
                f'Worker-{worker_id} finished Phase-{phase + 1}\n'
            )

            output_buffer.write(
                f'Worker-{worker_id} waiting at Barrier\n'
            )

            barrier.wait()

            output_buffer.write(
                f'Worker-{worker_id} entering next phase\n'
            )

    output_buffer.write(
        '=== Starting Multi-Phase Processing ===\n\n'
    )

    threads = []

    for i in range(num_workers):
        t = threading.Thread(target=worker, args=(i + 1,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    output_buffer.write(
        '\n=== All Phases Completed ===\n'
    )

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
سناریو ۲: پردازش چندمرحله‌ای با Barrier

در این سناریو چند Thread به صورت موازی
در چند مرحله مختلف فعالیت می‌کنند.

هر Thread پس از اتمام یک مرحله به Barrier
می‌رسد و تا رسیدن سایر Threadها منتظر می‌ماند.

تنها زمانی که همه Threadها مرحله جاری را
به پایان برسانند، Barrier آزاد شده و
مرحله بعدی آغاز می‌شود.

این فرآیند برای تمامی مراحل تکرار می‌شود
تا هماهنگی کامل میان Threadها حفظ گردد.

این روش در سیستم‌های پردازش موازی کاربرد دارد؛
جایی که شروع هر مرحله وابسته به اتمام
مرحله قبل توسط تمامی پردازش‌ها است.
'''
    }


#Scenario 3: Barrier with Action

def scenario_3():
    output_buffer = io.StringIO()

    num_workers = 3
    results = []
    results_lock = threading.Lock()

    def collect_results():
        with results_lock:
            total = sum(results)
            avg = total / len(results)
            output_buffer.write(f'\n--- Barrier Action ---\n')
            output_buffer.write(f'Total: {total}, Average: {avg:.2f}\n')
            output_buffer.write(f'--- End Action ---\n\n')
            results.clear()

    barrier = threading.Barrier(num_workers, action=collect_results)

    def worker(worker_id):
        for round_num in range(3):
            time.sleep(random.uniform(0.3, 1.0))
            result = random.randint(10, 100)

            with results_lock:
                results.append(result)

            timestamp = time.strftime('%H:%M:%S')
            output_buffer.write(f'[{timestamp}] Worker-{worker_id} Round-{round_num + 1}: {result}\n')

            barrier.wait()

    output_buffer.write('=== Starting Computation ===\n\n')

    threads = []
    for i in range(num_workers):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    output_buffer.write('=== Computation Completed ===\n')

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
        در این سناریو چند Thread به صورت موازی
محاسبات خود را انجام داده و نتایج را
در یک منبع مشترک ذخیره می‌کنند.

پس از رسیدن همه Threadها به Barrier،
یک تابع Action به صورت خودکار اجرا می‌شود
و نتایج تولیدشده را جمع‌آوری و پردازش می‌کند.

بعد از اجرای Action، Barrier آزاد شده
و همه Threadها وارد مرحله بعدی می‌شوند.

این فرآیند در چند مرحله متوالی تکرار می‌شود
و در پایان هر مرحله، نتایج به صورت متمرکز
محاسبه و آماده استفاده می‌شوند.

این الگو برای پردازش‌های گروهی، تحلیل داده
و هماهنگ‌سازی محاسبات موازی بسیار مناسب است.
        '''
    }
