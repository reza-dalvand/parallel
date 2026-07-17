import multiprocessing
import time
import io


import multiprocessing
import time
import io

def foo(output_queue, task_name, duration):
    output_queue.put(f"{task_name}: Starting...")
    for i in range(duration):
        time.sleep(1)
        output_queue.put(f"{task_name}: Working... {i + 1}/{duration}")
    output_queue.put(f"{task_name}: Completed!")

def scenario_1():
    output_buffer = io.StringIO()
    ctx = multiprocessing.get_context('spawn')
    # بدلیل استفاده از جنگو خروجی مورد نظر تولید نمیشد 
    # برای رفع این مشکل تغییرات زیر اعمال شد
    output_queue = ctx.Queue()
    process = ctx.Process(
        target=foo,
        args=(output_queue, "TerminateProcess", 10),
        name='Terminate_Process'
    )

    output_buffer.write(f"Process before execution: {process} {process.is_alive()}\n") # initial
    
    process.start()
    output_buffer.write(f"Process running: {process} {process.is_alive()}\n") # started

    time.sleep(2) # صبر میکنیم یکم پراسس انجام بشه

    process.terminate() 
    output_buffer.write(f"Process terminated: {process} {process.is_alive()}\n") # started

    process.join()
    output_buffer.write(f"Process joined: {process} {process.is_alive()}\n") # stopped
    output_buffer.write(f"Process exit code: {process.exitcode}\n\n")

    while not output_queue.empty():
        output_buffer.write(output_queue.get() + '\n')

    return {"output": output_buffer.getvalue()}



def func2(duration):
    time.sleep(duration)

# متوقف کردن پراسس های معیوب
def scenario_2():

    output_buffer = io.StringIO()
    ctx = multiprocessing.get_context('spawn')
    # بدلیل استفاده از جنگو خروجی مورد نظر تولید نمیشد 
    # برای رفع این مشکل تغییرات زیر اعمال شد
    output_queue = ctx.Queue()

    processes = []

    durations = [2, 6, 3]

    for i, duration in enumerate(durations):

        process = ctx.Process(
            target=func2,
            args=(duration,),
            name=f"Process-{i+1}"
        )

        processes.append(process)

        output_buffer.write(
            f"Starting {process.name}\n"
        )

        process.start()

    time.sleep(4) # این زمان برای انجام پراسس 1 و 3 کافی است ولی 2 متوقف میشود

    output_buffer.write(
        "\nChecking running processes...\n"
    )

    for process in processes:

        if process.is_alive():

            output_buffer.write(
                f"{process.name} is still running -> terminate()\n"
            )

            process.terminate()

        else:

            output_buffer.write(
                f"{process.name} already finished\n"
            )

    output_buffer.write("\n")

    for process in processes:

        process.join()

        output_buffer.write(
            f"{process.name} | ExitCode={process.exitcode}\n"
        )

    output_buffer.write("\n")

    while not output_queue.empty():

        output_buffer.write(
            output_queue.get() + '\n'
        )

    output_text = output_buffer.getvalue()

    return {

        "output": output_text,

        "explanation": '''
سناریو ۳: Selective Process Termination

در این سناریو چند Process
به صورت همزمان اجرا می‌شوند.

مدت زمان اجرای هر Process
با دیگری متفاوت است.

پس از گذشت مدت زمان مشخص،
برنامه وضعیت تمامی Processها
را بررسی می‌کند.

Processهایی که کار خود را
به پایان رسانده‌اند بدون تغییر
باقی می‌مانند.

در مقابل، Processهایی که
هنوز در حال اجرا هستند،
با استفاده از terminate()
متوقف می‌شوند.

این روش زمانی کاربرد دارد
که تنها بخواهیم Processهای
طولانی یا گیرکرده را متوقف کنیم
و اجازه دهیم سایر Processها
به صورت عادی پایان یابند.
'''
    }

def func3(duration):
    time.sleep(duration)

# Timeout Process Termination
def scenario_3():

    output_buffer = io.StringIO()
    ctx = multiprocessing.get_context('spawn')
    # بدلیل استفاده از جنگو خروجی مورد نظر تولید نمیشد 
    # برای رفع این مشکل تغییرات زیر اعمال شد
    output_queue = ctx.Queue()

    process = ctx.Process(
        target=func3,
        args=(10),
        name="Timeout_Process"
    )

    output_buffer.write(
        f"Process before execution: {process} {process.is_alive()}\n"
    )

    process.start()

    output_buffer.write(
        f"Process running: {process} {process.is_alive()}\n"
    )

    process.join(timeout=3) #حداکثر 3 ثانیه منتظر می ماند تا پراسس به پایان برسد

    if process.is_alive():

        output_buffer.write(
            "Execution time exceeded -> Terminating process\n"
        )

        process.terminate()

        output_buffer.write(
            f"Process terminated: {process} {process.is_alive()}\n"
        )

        process.join() #اینجا دیگ پراسس تایم اپت شده تمام شده و منابع آزاد میشود

    output_buffer.write(
        f"Process joined: {process} {process.is_alive()}\n"
    )

    output_buffer.write(
        f"Process exit code: {process.exitcode}\n\n"
    )

    while not output_queue.empty():

        output_buffer.write(
            output_queue.get() + '\n'
        )

    output_text = output_buffer.getvalue()

    return {

        "output": output_text,

        "explanation": '''
سناریو ۲: Terminating Process after Timeout

در این سناریو یک Process ایجاد
و اجرا می‌شود.

برنامه با استفاده از
join(timeout)
مدت زمان مشخصی منتظر پایان اجرای
Process باقی می‌ماند.

اگر Process در این زمان
به پایان نرسد،
با استفاده از terminate()
به صورت اجباری متوقف می‌شود.

در پایان نیز با استفاده از
join()
منابع Process آزاد شده
و وضعیت نهایی آن بررسی می‌شود.

این روش برای جلوگیری از اجرای
بیش از حد Processها
و جلوگیری از گیر کردن برنامه
کاربرد دارد.
'''
    }