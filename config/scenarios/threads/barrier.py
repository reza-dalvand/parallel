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
        'explanation': 'سناریو ۱: الگوی پایه Barrier - مسابقه دو'
    }


# ==================== Scenario 2: Multiple Phases with Barrier ====================



# ==================== Scenario 3: Barrier with Action ====================

def scenario_3():
    """
    سناریو ۳: Barrier با Action - جمع‌آوری نتایج

    Barrier می‌تواند یک تابع action داشته باشد که وقتی همه threadها
    به barrier رسیدند، یکبار اجرا می‌شود (توسط آخرین thread).
    """
    output_buffer = io.StringIO()

    num_workers = 3
    results = []
    results_lock = threading.Lock()

    def collect_results():
        """این تابع وقتی همه به barrier رسیدند، اجرا می‌شود"""
        with results_lock:
            total = sum(results)
            avg = total / len(results)
            output_buffer.write(f'\n--- Barrier Action ---\n')
            output_buffer.write(f'Total: {total}, Average: {avg:.2f}\n')
            output_buffer.write(f'--- End Action ---\n\n')
            results.clear()

    # Barrier با action
    barrier = threading.Barrier(num_workers, action=collect_results)

    def worker(worker_id):
        for round_num in range(3):
            # انجام محاسبه
            time.sleep(random.uniform(0.3, 1.0))
            result = random.randint(10, 100)

            with results_lock:
                results.append(result)

            timestamp = time.strftime('%H:%M:%S')
            output_buffer.write(f'[{timestamp}] Worker-{worker_id} Round-{round_num + 1}: {result}\n')

            # منتظر بقیه - action اجرا می‌شود
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
        'explanation': 'سناریو ۳: Barrier با Action'
    }
