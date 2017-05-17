import json

import requests
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from compilio.compiler.models import Compiler
from compilio.compiler.models import Task


def validate_post_arg(request, *keys):
    if request.method != 'POST':
        raise Exception('Use Method POST')

    arguments = []
    for key in keys:
        argument = request.POST.get(key)
        if argument is None:
            raise Exception(key + ' is None')
        arguments.append(argument)
        print(argument)

    if len(keys) == 1:
        return arguments[0]

    return arguments


@csrf_exempt
def init(request):
    try:
        command = validate_post_arg(request, 'command')
    except Exception as e:
        return HttpResponse(e, status=400)

    compiler_name = command.split(' ')[0]

    try:
        compiler_object = Compiler.objects.get(name=compiler_name)
    except Compiler.DoesNotExist:
        print('No compiler found')
        return HttpResponse('No compiler found', status=404)

    task = Task(command=command, compiler=compiler_object)
    task.save()

    # TODO : Task status to 'Waiting for input_files'

    input_files = compiler_object.get_input_files(command)

    return JsonResponse({'input_files': input_files, 'task_id': task.id})


def save_files(request, task_id, folder):
    file = request.FILES['0']  # TODO : hardcoded key
    fs = FileSystemStorage()
    filename = fs.save('uploads/tasks/' + task_id + '/' + folder + '/' + file.name, file)
    uploaded_file_url = fs.url(filename)
    return uploaded_file_url


@csrf_exempt
def upload(request):
    try:
        task_id = validate_post_arg(request, 'task_id')
    except Exception as e:
        return HttpResponse(e, status=400)

    try:
        task_object = Task.objects.get(id=task_id)
    except Compiler.DoesNotExist:
        print('No Task found')
        return HttpResponse('No Task found', status=404)

    uploaded_file_url = save_files(request, task_id, 'input_files')

    # TODO : Find the correct runner
    res = requests.post("http://localhost:7894/compile",
                        data={'task_id': task_id, 'bash': task_object.command}, files={'0': open(
                            uploaded_file_url, 'rb')})
    print(json.loads(res.text)['output'])

    # TODO : param task_id, input_files

    # TODO : Create files rows in bd and attach it to Task object
    # TODO : Get build process (here or in 'init' endpoint)
    # TODO : Send process_build and input files to compiler-runner
    # TODO : Task status to 'Sent to runner'

    return JsonResponse({'ok': uploaded_file_url})


@csrf_exempt
def status(request):
    # TODO : param task_id
    # TODO : Get status from db
    # TODO : OR
    # TODO : Query compiler-runner to get status
    # TODO : Update status
    return JsonResponse({'ok': 'ok'})


@csrf_exempt
def receive_output_files(request):
    # TODO : Called by compiler_runner
    # TODO : param task_id, output_files

    # TODO : Store output_files in /task_id/input_files
    # TODO : Change status

    return JsonResponse({'ok': 'ok'})
