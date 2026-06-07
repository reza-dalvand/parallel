import multiprocessing

class MyProcess(multiprocessing.Process):
    def run(self):
        return f'called run method by {self.name}'

def scenario_1():
    outputs = []

    processes = []
    for i in range(10):
        process = MyProcess()
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
        outputs.append(f'called run method by {process.name}')

    output_text = "\n".join(outputs)

    return {
        'output': output_text,
        'explanation': '''
        در این سناریو یک کلاس سفارشی از
multiprocessing.Process
ایجاد می‌شود و متد run() در آن
بازنویسی (Override) می‌گردد.

سپس ۱۰ Process از این کلاس ساخته شده
و به صورت مستقل اجرا می‌شوند.

هر Process هنگام اجرا، متد run()
خود را فراخوانی کرده و نام Process
را در خروجی نمایش می‌دهد.

پس از شروع اجرای Processها،
برنامه اصلی با استفاده از join()
منتظر پایان همه آن‌ها می‌ماند.

این سناریو نحوه ساخت Processهای سفارشی
و استفاده از برنامه‌نویسی شیءگرا
در multiprocessing را نشان می‌دهد.
        '''
    }


def scenario_2():
    outputs = []

    processes = []
    for i in range(5):
        process = MyProcess()
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()
        outputs.append(f'called run method by {process.name}')

    output_text = "\n".join(outputs)

    return {
        'output': output_text,
        'explanation': '''
        در این سناریو چند Process ایجاد می‌شوند،
اما برخلاف اجرای ترتیبی، ابتدا همه Processها
با استفاده از start() آغاز به کار می‌کنند.

پس از شروع اجرای تمامی Processها،
برنامه اصلی با استفاده از join()
منتظر پایان آن‌ها می‌ماند.

به دلیل اینکه همه Processها پیش از
فراخوانی join() اجرا شده‌اند،
امکان پردازش همزمان میان آن‌ها وجود دارد.

این روش یکی از رایج‌ترین الگوهای
اجرای موازی در multiprocessing است
و باعث استفاده بهتر از منابع سیستم می‌شود.

این سناریو تفاوت میان اجرای ترتیبی
و اجرای موازی Processها را نمایش می‌دهد.
        '''
    }


class MyProcessWithArg(multiprocessing.Process):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def run(self):
        return f'called run method by {self.name} with value {self.value}'


def scenario_3():
    outputs = []

    processes = []
    for i in range(10):
        value = (i + 1) * 100  # 100, 200, 300, ..., 1000
        process = MyProcessWithArg(value)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
        outputs.append(f'called run method by {process.name} with value {process.value}')

    output_text = "\n".join(outputs)

    return {
        'output': output_text,
        'explanation': '''
        در این سناریو یک کلاس سفارشی از Process
تعریف می‌شود که هنگام ایجاد، یک مقدار
به عنوان آرگومان دریافت می‌کند.

این مقدار در سازنده کلاس ذخیره شده
و هنگام اجرای متد run()
در اختیار Process قرار می‌گیرد.

سپس چندین Process با مقادیر مختلف
ایجاد و اجرا می‌شوند تا هر Process
بتواند داده مخصوص به خود را پردازش کند.

پس از پایان اجرای Processها،
برنامه اصلی با استفاده از join()
منتظر اتمام همه آن‌ها می‌ماند.

این سناریو نحوه ارسال داده به Processهای
سفارشی و استفاده از پارامترهای اختصاصی
در زمان ایجاد Process را نشان می‌دهد.
        '''
    }
