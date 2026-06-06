import multiprocessing

def function_square(data):
    result = data * data
    return result

def scenario_1():
    """سناریو اول: استفاده از map() - blocking"""

    inputs = list(range(0, 100))

    pool = multiprocessing.Pool(processes=4)
    pool_outputs = pool.map(function_square, inputs)
    pool.close()
    pool.join()

    output = f"Pool : {pool_outputs}"

    return {
        'output': output,
        'explanation': (
            'سناریو اول: استفاده از Process Pool برای محاسبه موازی. '
            'یک pool با ۴ پراسس ایجاد می‌شود و تابع function_square روی اعداد ۰ تا ۹۹ '
            'به صورت موازی اجرا می‌شود. pool.map داده‌ها را بین پراسس‌ها توزیع می‌کند '
            'و نتیجه توان دوم هر عدد را برمی‌گرداند.'
        )
    }


def scenario_2():
    """سناریو دوم: استفاده از map_async() - non-blocking"""

    inputs = list(range(0, 100))

    pool = multiprocessing.Pool(processes=4)
    async_result = pool.map_async(function_square, inputs)
    pool.close()
    pool_outputs = async_result.get()
    pool.join()

    output = f"Pool : {pool_outputs}"

    return {
        'output': output,
        'explanation': (
            'سناریو دوم: استفاده از map_async() به جای map(). '
            'این متد بلافاصله یک AsyncResult برمی‌گرداند و پراسس اصلی بلاک نمی‌شود. '
            'در نهایت با .get() نتیجه نهایی دریافت می‌شود.'
        )
    }


def scenario_3():
    """سناریو سوم: استفاده از apply_async() با حلقه - non-blocking"""

    inputs = list(range(0, 100))

    pool = multiprocessing.Pool(processes=4)
    async_results = [pool.apply_async(function_square, args=(i,)) for i in inputs]
    pool.close()
    pool_outputs = [r.get() for r in async_results]
    pool.join()

    output = f"Pool : {pool_outputs}"

    return {
        'output': output,
        'explanation': (
            'سناریو سوم: استفاده از apply_async() در یک حلقه. '
            'برای هر عدد به صورت جداگانه apply_async() فراخوانی می‌شود و '
            'هر کدام یک AsyncResult برمی‌گردانند. '
            'در نهایت با .get() روی هر نتیجه، لیست نهایی ساخته می‌شود.'
        )
    }
