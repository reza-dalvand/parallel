import io
import multiprocessing


class MyProcess(multiprocessing.Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        self.queue.put(f'called run method by {self.name}')


def scenario_1():
    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    for i in range(10):
        process = MyProcess(queue)
        process.start()
        process.join()      # اجرای ترتیبی

        if not queue.empty():
            output_buffer.write(queue.get() + "\n")

    return {
        "output": output_buffer.getvalue(),
        "explanation": ''' در این سناریو یک کلاس سفارشی از
multiprocessing.Process
تعریف شده و متد run() در آن
بازنویسی (Override) می‌شود.

هر Process هنگام اجرای متد start()
به صورت خودکار متد run() خود را
در Process فرزند اجرا می‌کند.

در این مثال پس از ایجاد هر Process،
بلافاصله متد join() فراخوانی می‌شود.
به همین دلیل برنامه اصلی تا پایان
اجرای همان Process منتظر می‌ماند و
سپس Process بعدی را ایجاد می‌کند.

در نتیجه Processها به صورت ترتیبی
و بدون اجرای همزمان اجرا می‌شوند.

این سناریو نشان می‌دهد که Override
کردن متد run() روشی شیءگرا برای
تعریف رفتار Process است و همچنین
استفاده از join() پس از start()
باعث اجرای ترتیبی Processها می‌شود.'''
    }



# Run as parallel processes, then waited for all to finish

def scenario_2():

    output_buffer = io.StringIO()
    queue = multiprocessing.Queue()

    processes = []

    for i in range(5):
        process = MyProcess(queue)
        processes.append(process)

    # شروع همه Processها
    for process in processes:
        process.start()

    # انتظار برای پایان همه
    for process in processes:
        process.join()

    # دریافت خروجی همه Processها
    while not queue.empty():
        output_buffer.write(queue.get() + "\n")

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
        در این سناریو نیز از همان کلاس
سفارشی مشتق‌شده از
multiprocessing.Process
استفاده می‌شود و رفتار Process
در متد run() تعریف شده است.

ابتدا تمامی Processها ایجاد شده و
با استفاده از start() اجرا می‌شوند.
در این مرحله هر Process به صورت
مستقل متد run() خود را اجرا می‌کند.

پس از شروع اجرای همه Processها،
برنامه اصلی با استفاده از join()
منتظر پایان آن‌ها می‌ماند.

از آنجا که فراخوانی join() تا
پس از start() همه Processها به
تعویق افتاده است، Processها امکان
اجرای همزمان را خواهند داشت.

این سناریو تفاوت میان اجرای ترتیبی
و اجرای موازی Processها را نشان
می‌دهد و یکی از رایج‌ترین الگوهای
استفاده از multiprocessing است.
        '''
    }

class MessageProcess(multiprocessing.Process):

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        self.queue.put(f'[{self.name}] Sending message')


class NumberProcess(multiprocessing.Process):

    def __init__(self, number, queue):
        super().__init__()
        self.number = number
        self.queue = queue

    def run(self):
        self.queue.put(
            f'[{self.name}] Square of {self.number} = {self.number ** 2}'
        )

# ارث بری پراسس ها از کلاس های متفاوت
def scenario_3():

    output = io.StringIO()
    queue = multiprocessing.Queue()

    processes = [
        MessageProcess(queue),
        NumberProcess(5, queue),
        NumberProcess(10, queue)
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    while not queue.empty():
        output.write(queue.get() + "\n")

    return {
        "output": output.getvalue(),
        "explanation": """
در این سناریو دو Subclass مختلف از
multiprocessing.Process
تعریف شده‌اند.

هر Subclass متد run() مخصوص
به خود را پیاده‌سازی می‌کند و
رفتار متفاوتی دارد.

MessageProcess تنها یک پیام
نمایش می‌دهد، در حالی که
NumberProcess یک عملیات محاسباتی
روی عدد ورودی انجام می‌دهد.

این سناریو نشان می‌دهد که با
ایجاد Subclassهای مختلف می‌توان
Processهایی با رفتارهای متفاوت
طراحی کرد، در حالی که همگی از
کلاس Process ارث‌بری می‌کنند و
با استفاده از start() اجرا می‌شوند.
"""
    }