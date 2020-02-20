import os
from .FB import FacebookParser
from django.http import JsonResponse
from threading import Thread
from .login_config import login, pswd
from .save import save_members


def index(request, group_url):
    group_url = group_url.replace('_', '/')

    path = os.getcwd() + '/Parser/chromedriver.exe'
    parser = FacebookParser(path)

    th = Thread(target=save_members, args=[parser, group_url, login, pswd])
    th.start()
    return JsonResponse({'process': 'started'})
