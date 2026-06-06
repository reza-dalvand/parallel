import threading
import time
import io

class Box:
    def __init__(self, output_buffer):
        self.lock = threading.RLock()
        self.total_items = 0
        self.output_buffer = output_buffer
        self.turn = 'add'  # 'add' or 'remove'
        self.condition = threading.Condition(self.lock)
        self.remover_done = False  # پرچم برای اعلام اتمام remover

    def execute(self, value):
        with self.lock:
            self.total_items += value

    def add(self):
        with self.condition:
            while self.turn != 'add' and not self.remover_done:
                self.condition.wait()

            self.execute(1)
            self.turn = 'remove'
            self.condition.notify_all()

    def remove(self):
        with self.condition:
            while self.turn != 'remove':
                self.condition.wait()

            self.execute(-1)
            self.turn = 'add'
            self.condition.notify_all()

    def mark_remover_done(self):
        with self.condition:
            self.remover_done = True
            self.condition.notify_all()


def adder(box, items):
    box.output_buffer.write(f"N° {items} items to ADD\n")
    while items:
        box.add()
        time.sleep(0.1)
        items -= 1
        box.output_buffer.write(f"ADDED one item -->{items} item to ADD\n")


def remover(box, items):
    box.output_buffer.write(f"N° {items} items to REMOVE\n")
    while items:
        box.remove()
        time.sleep(0.1)
        items -= 1
        box.output_buffer.write(f"REMOVED one item -->{items} item to REMOVE\n")

    # work done
    box.mark_remover_done()


def scenario_1():
    output_buffer = io.StringIO()
    box = Box(output_buffer)

    add_count = 16
    remove_count = 1

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
در این سناریو دو Thread مستقل برای افزودن
و حذف آیتم‌ها از یک منبع مشترک ایجاد می‌شوند.

برای مدیریت دسترسی همزمان به داده‌ها
از RLock و Condition استفاده شده است.

ابتدا عملیات افزودن انجام می‌شود و سپس
Thread حذف‌کننده اجازه اجرا پیدا می‌کند.

پس از پایان عملیات حذف، Thread افزودن
بدون ایجاد بن‌بست به کار خود ادامه می‌دهد.

این ساختار نمونه‌ای از الگوی Producer-Consumer
برای هماهنگی بین وظایف تولید و مصرف داده است.

'''
}


class BoxAlternating:
    def __init__(self, output_buffer):
        self.lock = threading.RLock()
        self.total_items = 0
        self.output_buffer = output_buffer
        self.turn = 'add'
        self.add_count = 0
        self.remove_count = 0
        self.condition = threading.Condition(self.lock)

    def execute(self, value):
        with self.lock:
            self.total_items += value

    def add(self):
        with self.condition:
            while self.turn != 'add':
                self.condition.wait()

            self.execute(1)
            self.add_count += 1

            if self.add_count >= 2:
                self.add_count = 0
                self.turn = 'remove'
                self.condition.notify_all()

    def remove(self):
        with self.condition:
            while self.turn != 'remove':
                self.condition.wait()

            self.execute(-1)
            self.remove_count += 1

            if self.remove_count >= 2:
                self.remove_count = 0
                self.turn = 'add'
                self.condition.notify_all()


def adder_alternating(box, items):
    box.output_buffer.write(f"N° {items} items to ADD\n")
    while items:
        box.add()
        time.sleep(0.5)
        items -= 1
        box.output_buffer.write(f"ADDED one item --> {items} item to ADD\n")


def remover_alternating(box, items):
    box.output_buffer.write(f"N° {items} items to REMOVE\n")
    while items:
        box.remove()
        time.sleep(0.5)
        items -= 1
        box.output_buffer.write(f"REMOVED one item --> {items} item to REMOVE\n")


def scenario_2():
    output_buffer = io.StringIO()
    box = BoxAlternating(output_buffer)

    # تعداد زوج برای الگوی 2-2
    add_count = 10
    remove_count = 10

    t1 = threading.Thread(target=adder_alternating, args=(box, add_count))
    t2 = threading.Thread(target=remover_alternating, args=(box, remove_count))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    output_buffer.write(f"\n=== Final total items in box: {box.total_items} ===\n")

    return {
        'output': output_buffer.getvalue(),
        'explanation': '''
در این سناریو عملیات افزودن و حذف
به صورت نوبتی و کنترل‌شده انجام می‌شوند.

پس از هر دو عملیات افزودن، نوبت به
دو عملیات حذف داده می‌شود و این روند
تا پایان اجرای برنامه ادامه پیدا می‌کند.

برای کنترل ترتیب اجرا از Condition
و متغیرهای شمارنده استفاده شده است.

این روش باعث ایجاد تعادل میان عملیات تولید
و مصرف شده و از اجرای نامنظم Threadها
جلوگیری می‌کند.
        '''
    }


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
    box.output_buffer.write(f"N° {items} items to ADD\n")
    while items:
        box.add()
        time.sleep(0.3)
        items -= 1
        box.output_buffer.write(f"ADDED one item --> {items} item to ADD\n")

    box.output_buffer.write("\nAll ADD operations completed\n\n")
    box.add_done.set()


def remover_sequential(box, items):
    # منتظر بمان تا همه addها تمام شوند
    box.add_done.wait()

    box.output_buffer.write(f"N° {items} items to REMOVE\n")
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

    output_buffer.write(f"\n=== Final total items in box: {box.total_items} ===\n")

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
