import multiprocessing

def function_square(data):
    result = data * data
    return result

def scenario_1():
    inputs = list(range(0, 100))

    pool = multiprocessing.Pool(processes=4)
    pool_outputs = pool.map(function_square, inputs)
    pool.close()
    pool.join()

    output = f"Pool : {pool_outputs}"

    return {
        'output': output,
        'explanation': '''
        در این سناریو یک Process Pool شامل
چهار Process کاری ایجاد می‌شود.

سپس مجموعه‌ای از اعداد از ۰ تا ۹۹
به متد map() ارسال می‌شوند تا تابع
function_square روی هر یک از آن‌ها اجرا شود.

Pool وظیفه تقسیم داده‌ها میان Processهای موجود
و اجرای موازی محاسبات را بر عهده دارد.

متد map() یک عملیات Blocking است؛
به این معنا که Process اصلی تا زمان
پایان پردازش تمامی داده‌ها منتظر می‌ماند.

پس از اتمام همه محاسبات،
نتایج به همان ترتیبی که داده‌ها ارسال شده‌اند
بازگردانده می‌شوند.

این روش برای انجام پردازش‌های یکسان
روی حجم زیادی از داده‌ها بسیار مناسب است.
        '''
    }










def scenario_2():
    inputs = list(range(0, 100))

    pool = multiprocessing.Pool(processes=4)
    async_result = pool.map_async(function_square, inputs)
    pool.close()
    pool_outputs = async_result.get()
    pool.join()

    output = f"Pool : {pool_outputs}"

    return {
        'output': output,
        'explanation': '''
        در این سناریو نیز از یک Process Pool
شامل چهار Process استفاده می‌شود،
اما به جای map() از متد map_async() استفاده شده است.

برخلاف map()، این متد بلافاصله پس از ارسال وظایف
یک شیء AsyncResult بازمی‌گرداند
و Process اصلی را متوقف نمی‌کند.

در این مدت Processهای موجود در Pool
به صورت موازی وظایف خود را اجرا می‌کنند.

پس از نیاز به نتایج نهایی،
با فراخوانی متد get() خروجی تمامی پردازش‌ها
دریافت می‌شود.

این الگو زمانی مفید است که Process اصلی
در حین اجرای محاسبات موازی
کارهای دیگری نیز برای انجام داشته باشد.
        '''
    }


def scenario_3():
    inputs = list(range(0, 100))

    pool = multiprocessing.Pool(processes=4)
    async_results = [pool.apply_async(function_square, args=(i,)) for i in inputs]
    pool.close()
    pool_outputs = [r.get() for r in async_results]
    pool.join()

    output = f"Pool : {pool_outputs}"

    return {
        'output': output,
        'explanation': '''
        در این سناریو برای هر داده
به صورت جداگانه یک وظیفه جدید
با استفاده از apply_async() به Pool ارسال می‌شود.

هر فراخوانی apply_async()
یک شیء AsyncResult مستقل ایجاد می‌کند
که نماینده نتیجه همان وظیفه است.

Processهای موجود در Pool
وظایف را به صورت موازی دریافت و اجرا می‌کنند.

پس از پایان پردازش‌ها،
نتایج هر وظیفه از طریق متد get()
بازیابی شده و در یک لیست نهایی قرار می‌گیرند.

این روش انعطاف‌پذیری بیشتری نسبت به map_async()
فراهم می‌کند و برای مواقعی مناسب است
که هر وظیفه دارای پارامترها، زمان اجرا
یا منطق متفاوتی باشد.

این سناریو نحوه مدیریت مستقل وظایف
و دریافت جداگانه نتایج در Process Pool
را نمایش می‌دهد.
        '''
    }
