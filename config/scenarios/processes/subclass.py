import multiprocessing

class MyProcess(multiprocessing.Process):
    def run(self):
        return f'called run method by {self.name}'

def scenario_1():
    """سناریو اول: Defining processes in a subclass"""
    outputs = []

    # ایجاد و اجرای 10 پراسس از نوع MyProcess
    processes = []
    for i in range(10):
        process = MyProcess()
        processes.append(process)
        process.start()

    # جمع‌آوری خروجی‌ها و join کردن پراسس‌ها
    for process in processes:
        process.join()
        outputs.append(f'called run method by {process.name}')

    # تبدیل لیست به رشته
    output_text = "\n".join(outputs)

    return {
        'output': output_text,
        'explanation': 'سناریو اول: ایجاد یک کلاس سفارشی از Process با override کردن متد run(). ده نمونه از این کلاس ساخته و به صورت موازی اجرا می‌شوند. هر پراسس نام خود را چاپ می‌کند.'
    }


def scenario_2():
    """سناریو دوم: تغییر ترتیب اجرا - ابتدا همه start، سپس همه join"""
    outputs = []

    # ایجاد 5 پراسس
    processes = []
    for i in range(5):
        process = MyProcess()
        processes.append(process)

    # ابتدا همه پراسس‌ها را start می‌کنیم
    for process in processes:
        process.start()

    # سپس همه را join می‌کنیم
    for process in processes:
        process.join()
        outputs.append(f'called run method by {process.name}')

    # تبدیل لیست به رشته
    output_text = "\n".join(outputs)

    return {
        'output': output_text,
        'explanation': 'سناریو دوم: پنج پراسس ایجاد می‌شوند. ابتدا همه پراسس‌ها start می‌شوند (اجرای موازی واقعی) و سپس همه join می‌شوند. این روش باعث می‌شود پراسس‌ها واقعاً به صورت همزمان اجرا شوند و ترتیب خروجی ممکن است متفاوت باشد.'
    }


class MyProcessWithArg(multiprocessing.Process):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def run(self):
        return f'called run method by {self.name} with value {self.value}'


def scenario_3():
    """سناریو سوم: ارسال آرگومان به پراسس"""
    outputs = []

    # ایجاد و اجرای 10 پراسس با مقادیر مختلف
    processes = []
    for i in range(10):
        value = (i + 1) * 100  # 100, 200, 300, ..., 1000
        process = MyProcessWithArg(value)
        processes.append(process)
        process.start()

    # جمع‌آوری خروجی‌ها و join کردن پراسس‌ها
    for process in processes:
        process.join()
        outputs.append(f'called run method by {process.name} with value {process.value}')

    # تبدیل لیست به رشته
    output_text = "\n".join(outputs)

    return {
        'output': output_text,
        'explanation': 'سناریو سوم: کلاس MyProcessWithArg از Process ارث‌بری می‌کند و یک پارامتر عددی دریافت می‌کند. ده پراسس با مقادیر 100 تا 1000 ایجاد می‌شوند. هر پراسس نام خود و مقدار دریافتی را چاپ می‌کند. این سناریو نحوه ارسال آرگومان به پراسس‌های سفارشی را نشان می‌دهد.'
    }
