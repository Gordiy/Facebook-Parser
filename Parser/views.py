import os
from .FB import FacebookParser
from django.http import JsonResponse
from threading import Thread

from .save import save_members, get_credentials


def index(request, group_url):
    group_url = group_url.replace('_', '/')

    login_creds = get_credentials()
    path = os.getcwd() + '/Parser/chromedriver.exe'

    if login_creds:
        parser = FacebookParser(path)

        th = Thread(target=save_members, args=[parser, group_url, login_creds['login'], login_creds['password']])
        th.start()
        return JsonResponse({'process': 'started'})
    else:
        return JsonResponse({"error": 'set login credentials in db'})
