"""
اجراکننده مرکزی تمام سناریوها
"""
import inspect

# Import thread scenarios
from scenarios.threads import (
    defining_thread,
    current_thread,
    thread_subclass,
    lock,
    rlock,
    semaphore,
    barrier
)

# Import processes scenarios
from scenarios.processes import (
    spawning,
    naming,
    background,
    killing,
    subclass,
    queue,
    synchronization,
    pool
)

# نقشه سناریوها
SCENARIOS_MAP = {
    'thread': {
        'defining_thread': defining_thread,
        'current_thread': current_thread,
        'thread_subclass': thread_subclass,
        'lock': lock,
        'rlock': rlock,
        'semaphore': semaphore,
        'barrier': barrier,
    },
    'processes': {
        'spawning': spawning,
        'naming': naming,
        'background': background,
        'killing': killing,
        'subclass': subclass,
        'queue': queue,
        'synchronization': synchronization,
        'pool': pool,
    }
}


def execute_scenario(method, tool, scenario_num):
    """
    اجرای یک سناریوی خاص

    Args:
        method: 'thread' یا 'processes'
        tool: نام ابزار (مثلاً 'lock', 'semaphore')
        scenario_num: شماره سناریو (1، 2 یا 3)

    Returns:
        dict با کلیدهای 'code', 'output', 'explanation'
    """

    # پیدا کردن ماژول مربوط
    if method not in SCENARIOS_MAP:
        raise ValueError(f"روش نامعتبر: {method}")

    if tool not in SCENARIOS_MAP[method]:
        raise ValueError(f"ابزار نامعتبر: {tool}")

    module = SCENARIOS_MAP[method][tool]

    # پیدا کردن تابع سناریو
    scenario_func_name = f'scenario_{scenario_num}'
    if not hasattr(module, scenario_func_name):
        raise ValueError(f"سناریو {scenario_num} برای {tool} وجود ندارد")

    scenario_func = getattr(module, scenario_func_name)

    # گرفتن کد سورس
    code = inspect.getsource(scenario_func)

    # اجرای سناریو و گرفتن نتیجه
    try:
        result = scenario_func()

        # اگر سناریو دیکشنری برگرداند، از آن استفاده کن
        if isinstance(result, dict):
            output = result.get('output', '')
            explanation = result.get('explanation', scenario_func.__doc__ or "توضیحی موجود نیست")
        else:
            # اگر چیز دیگری برگرداند، آن را به string تبدیل کن
            output = str(result) if result is not None else ''
            explanation = scenario_func.__doc__ or "توضیحی موجود نیست"

    except Exception as e:
        output = f"خطا در اجرا: {str(e)}"
        explanation = scenario_func.__doc__ or "توضیحی موجود نیست"

    return {
        'code': code,
        'output': output.strip(),
        'explanation': explanation.strip()
    }
