import threading
import time
import random
import io

#این سناریو به صورت پینگ ‌پنگی کار میکنه یعنی ابتدا یک آیتم اضافه میشه و سپس یک آیتم حذف می‌شود
class Box:
    def __init__(self, output_buffer):
        self.lock = threading.RLock()
        self.total_items = 0
        self.output_buffer = output_buffer

    def execute(self, value):
        with self.lock:
            self.total_items += value

    def add(self):
        with self.lock:
            self.execute(1)

    def remove(self):
        with self.lock:
            self.execute(-1)


def adder(box, items):
    box.output_buffer.write(f"N° {items} items to ADD\n")
    while items:
        box.add()
        time.sleep(1)
        items -= 1
        box.output_buffer.write(f"ADDED one item -->{items} item to ADD\n")


def remover(box, items):
    box.output_buffer.write(f"N° {items} items to REMOVE\n")
    while items:
        box.remove()
        time.sleep(1)
        items -= 1
        box.output_buffer.write(f"REMOVED one item -->{items} item to REMOVE\n")


def scenario_1():
    output_buffer = io.StringIO()
    box = Box(output_buffer)

    add_count = random.randint(10, 20)
    remove_count = random.randint(1, 10)

    t1 = threading.Thread(target=adder, args=(box, add_count))
    t2 = threading.Thread(target=remover, args=(box, remove_count))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    output_buffer.write(f"\n=== Final total items in box: {box.total_items} ===\n")

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
این سناریو به صورت پینگ‌پنگی کار می‌کند؛ یعنی ابتدا یک آیتم اضافه میشه و
سپس یک آیتم حذف می‌شود. اما از آنجا که تعداد افزودن‌ها مثلا (۱۶) بیشتر از حذف‌ها
است، به محض اینکه عملیات حذف تمام می‌شود، ترد حذف‌کننده به ترد افزاینده سیگنال
می‌دهد تا بدون معطل شدن برای نوبت، تمام ۱۵ آیتم باقی‌مانده را یک‌جا و بدون
قفل شدن (بن‌بست) وارد جعبه کند.
            '''
    }






# توی این سناریو 2 آیتم اضافه سپس 2 ایتم حذف میشه و این چرخه تا زمان تموم شدن آیتم ها ادامه داره

class BoxAlternating:
    def __init__(self, output_buffer):
        self.lock = threading.RLock()
        self.total_items = 0
        self.output_buffer = output_buffer
        self.turn = 'add'
        self.add_count = 0
        self.remove_count = 0

    def execute(self, value):
        with self.lock:
            self.total_items += value

    def add(self):
        with self.lock:
            self.execute(1)
            self.add_count += 1
            if self.add_count >= 2:
                self.add_count = 0
                self.turn = 'remove'

    def remove(self):
        with self.lock:
            self.execute(-1)
            self.remove_count += 1
            if self.remove_count >= 2:
                self.remove_count = 0
                self.turn = 'add'


def adder_alternating(box, items):
    while items:
        if box.turn == 'add':
            box.add()
            time.sleep(0.5)
            items -= 1
            box.output_buffer.write(f"ADDED one item --> {items} item to ADD\n")


def remover_alternating(box, items):
    while items:
        if box.turn == 'remove':
            box.remove()
            time.sleep(0.5)
            items -= 1
            box.output_buffer.write(f"REMOVED one item --> {items} item to REMOVE\n")

def scenario_2():
    output_buffer = io.StringIO()
    box = BoxAlternating(output_buffer)

    add_count = 10
    remove_count = 10

    t1 = threading.Thread(target=adder_alternating, args=(box, add_count))
    t2 = threading.Thread(target=remover_alternating, args=(box, remove_count))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو عملیات افزودن و حذف
به صورت نوبتی و کنترل‌شده انجام می‌شوند.

پس از هر دو عملیات افزودن، نوبت به
دو عملیات حذف داده می‌شود و این روند
تا پایان اجرای برنامه ادامه پیدا می‌کند.

این روش باعث ایجاد تعادل میان عملیات تولید
و مصرف شده و از اجرای نامنظم Threadها
جلوگیری می‌کند.
        '''
    }

# در این سناریو از event استفاده شده
# اول سناریو ادد کارش رو شروع میکنه 10 ایتم اضافه و بعد با کمک event عملیات حذف کامل کارش رو انجام میده

class BoxSequential:
    def __init__(self, output_buffer):
        self.lock = threading.RLock()
        self.total_items = 0
        self.output_buffer = output_buffer
        self.add_done = threading.Event()

    def execute(self, value):
        with self.lock:
            self.total_items += value

    def add(self):
        with self.lock:
            self.execute(1)

    def remove(self):
        with self.lock:
            self.execute(-1)


def adder_sequential(box, items):
    while items:
        box.add()
        time.sleep(0.3)
        items -= 1
        box.output_buffer.write(f"ADDED one item --> {items} item to ADD\n")

    box.output_buffer.write("\nAll ADD operations completed\n\n")
    box.add_done.set()


def remover_sequential(box, items):
    box.add_done.wait() # Wait for the adder to finish adding items
    while items:
        box.remove()
        time.sleep(0.3)
        items -= 1
        box.output_buffer.write(f"REMOVED one item --> {items} item to REMOVE\n")

def scenario_3():
    output_buffer = io.StringIO()
    box = BoxSequential(output_buffer)

    add_count = 10
    remove_count = 10

    t1 = threading.Thread(target=adder_sequential, args=(box, add_count))
    t2 = threading.Thread(target=remover_sequential, args=(box, remove_count))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو ابتدا تمامی عملیات افزودن
به طور کامل اجرا می‌شوند.

پس از پایان این مرحله، یک سیگنال
از طریق Event ارسال می‌شود تا
عملیات حذف آغاز گردد.

Thread حذف‌کننده تا دریافت این سیگنال
در حالت انتظار باقی می‌ماند.

این مدل برای پردازش‌های مرحله‌ای مناسب است؛
جایی که شروع یک مرحله به اتمام کامل
مرحله قبلی وابسته است.
        '''
    }