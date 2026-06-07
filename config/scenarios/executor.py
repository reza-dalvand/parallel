import inspect

from scenarios.threads import (
    defining_thread,
    current_thread,
    thread_subclass,
    lock,
    rlock,
    semaphore,
    barrier,
    event,
    condition,
    queue
)

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

SCENARIOS_MAP = {
    'thread': {
        'defining_thread': defining_thread,
        'current_thread': current_thread,
        'thread_subclass': thread_subclass,
        'lock': lock,
        'rlock': rlock,
        'semaphore': semaphore,
        'barrier': barrier,
        'event': event,
        'condition': condition,
        'queue': queue
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
    if method not in SCENARIOS_MAP:
        raise ValueError(f"روش نامعتبر: {method}")

    if tool not in SCENARIOS_MAP[method]:
        raise ValueError(f"ابزار نامعتبر: {tool}")

    module = SCENARIOS_MAP[method][tool]

    scenario_func_name = f'scenario_{scenario_num}'
    if not hasattr(module, scenario_func_name):
        raise ValueError(f"سناریو {scenario_num} برای {tool} وجود ندارد")

    scenario_func = getattr(module, scenario_func_name)

    code = inspect.getsource(scenario_func)

    try:
        result = scenario_func()

        if isinstance(result, dict):
            output = result.get('output', '')
            explanation = result.get('explanation', scenario_func.__doc__ or "توضیحی موجود نیست")
        else:
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
