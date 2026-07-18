import multiprocessing
import random
import time


class Producer(multiprocessing.Process):
    def __init__(self, queue, output_queue, count=10):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.output_queue = output_queue
        self.count = count

    def run(self):
        for i in range(self.count):
            item = random.randint(0, 256)
            self.queue.put(item)

            time.sleep(0.1)
            self.output_queue.put(
                f"Process Producer : item {item} appended to queue {self.name}"
            )
            self.output_queue.put(
                f"The size of queue is {self.queue.qsize()}"
            )


class Consumer(multiprocessing.Process):
    def __init__(self, queue, output_queue, expected_items=10):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.output_queue = output_queue
        self.expected_items = expected_items

    def run(self):
        consumed = 0
        while consumed < self.expected_items:
            if not self.queue.empty():
                time.sleep(0.2)
                item = self.queue.get()
                self.output_queue.put(
                    f"Process Consumer : item {item} popped from by {self.name}"
                )
                consumed += 1
        self.output_queue.put("the queue is empty")


def scenario_1():
    queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    process_producer = Producer(queue, output_queue, count=10)
    process_consumer = Consumer(queue, output_queue, expected_items=10)

    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()

    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())

    return {
        "output": "\n".join(output_lines),
        "explanation": '''در این سناریو دو کلاس producer و consumer
از multiprocessing.Process ارث‌بری می‌کنند.

برای دریافت خروجی از subprocess‌ها از یک
Queue دوم به نام output_queue استفاده شده.
چون subprocess‌ها حافظه جداگانه دارند،
نوشتن مستقیم به StringIO کار نمی‌کند.

producer هر ۰.۱ ثانیه یک آیتم تصادفی
تولید کرده و در queue اصلی قرار می‌دهد.

consumer هر ۰.۲ ثانیه یک آیتم برمی‌دارد
و تا مصرف ۱۰ آیتم ادامه می‌دهد.

هر دو Process همزمان اجرا می‌شوند و
پیام‌های خود را در output_queue می‌ریزند.
پس از join() هر دو، برنامه اصلی
پیام‌ها را از output_queue می‌خواند.'''
    }



def worker(worker_id, task_queue, result_queue):
    while True:
        task = task_queue.get()
        if task is None:
            result_queue.put(f"Worker {worker_id} : Exiting.")
            break
        time.sleep(0.15)
        result_queue.put(f"Worker {worker_id} : Computed {task}")


def scenario_2():
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()
    
    num_workers = 3
    workers = []
    
    for i in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(i, task_queue, result_queue))
        workers.append(p)
        p.start()
        
    # اضافه کردن ۱۰ وظیفه به صف
    for i in range(1, 11):
        task_queue.put(i)
        
    # اضافه کردن این مقدار برای پایان دادن به کار پراسس ها
    for i in range(num_workers):
        task_queue.put(None)
        
    for p in workers:
        p.join()
        
    output_lines = []
    while not result_queue.empty():
        output_lines.append(result_queue.get())
        
    return {
        "output": "\n".join(output_lines),
        "explanation": '''در این سناریو از صف برای "توزیع بار" (Load Balancing) استفاده شده است.

به جای یک مصرف‌کننده، ۳ کارگر (Worker) همزمان به یک صف گوش می‌دهند.
این کار سرعت پردازش را بالا می‌برد چون هر کارگر که بی‌کار شود، 
سریعاً وظیفه بعدی را از صف برمی‌دارد.

نکته مهم این سناریو تکنیک Poison Pill (ارسال مقدار None) است. 
چون کارگرها در یک حلقه بی‌نهایت (while True) هستند، 
برنامه اصلی با فرستادن None به تعداد کارگرها، به آن‌ها می‌فهماند 
که کار تمام شده و باید بسته شوند.'''
    }



def daemon_processor(job_queue, output_queue):
    # چون پراسس از نوع دیمن است بعد از پردازش صف خودکار از بین میرود و حلقه قطع میشود
    while True:
        job = job_queue.get()
        
        time.sleep(0.2)
        output_queue.put(f"Job '{job}' is successfully processed.")
        
        # به صف اطلاع می‌دهیم که پردازش این آیتم تمام شده است
        job_queue.task_done()

def scenario_3():
    job_queue = multiprocessing.JoinableQueue()  # استفاده از صف پیوسته به جای صف معمولی
    output_queue = multiprocessing.Queue()
    
    p = multiprocessing.Process(target=daemon_processor, args=(job_queue, output_queue))
    p.daemon = True
    p.start()
    
    jobs = ["Update_DB", "Send_Emails", "Clear_Cache", "Generate_Report"]
    for job in jobs:
        output_queue.put(f"Main: Submitting job '{job}' to queue...")
        job_queue.put(job)
            
    # این دستور برنامه اصلی را متوقف می‌کند تا زمانی که به ازای هر پوت
    # یک بار دستور تسک دان توسط کارگرها صدا زده شود
    job_queue.join()
    
    output_queue.put("Main: All jobs completed! Moving forward.")
    
    output_lines = []
    while not output_queue.empty():
        output_lines.append(output_queue.get())
        
    return {
        "output": "\n".join(output_lines),
        "explanation": '''این سناریو تفاوت JoinableQueue با صف معمولی را نشان می‌دهد.

در اینجا ما نیازی نداریم که منتظر اتمام خودِ پردازش (process.join) بمانیم،
بلکه منتظر اتمام "آیتم‌های داخل صف" (job_queue.join) می‌مانیم.

هر بار که پردازشگر یک کار را تمام می‌کند، متد task_done() را صدا می‌زند.
وقتی تعداد task_done ها با تعداد آیتم‌هایی که در صف گذاشته بودیم برابر شود،
job_queue.join() در برنامه اصلی آزاد شده و برنامه ادامه پیدا می‌کند.

همچنین از daemon=True استفاده شده تا پردازشگر مثل یک سرویس پس‌زمینه
عمل کند و نیازی به ارسال سیگنال پایان (مثل سناریو ۲) نداشته باشد.'''
    }