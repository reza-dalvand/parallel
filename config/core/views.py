import traceback
from django.shortcuts import render
from scenarios.executor import execute_scenario


def index(request):
    return render(request, 'index.html')


def run_scenario(request):
    if request.method == 'POST':
        try:
            method = request.POST.get('method')
            tool = request.POST.get('tool')
            scenario_num = int(request.POST.get('scenario_num'))

            result = execute_scenario(method, tool, scenario_num)
            return render(request, 'result.html', {
                'method': method,
                'tool': tool,
                'scenario_num': scenario_num,
                'code': result['code'],
                'output': result['output'],
                'explanation': result['explanation'],
                'success': True
            })

        except Exception as e:
            return render(request, 'result.html', {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            })

    return render(request, 'index.html')
