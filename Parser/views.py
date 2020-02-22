import os
from .FB import FacebookParser
from django.http import JsonResponse
import threading

from .save import save_members, get_credentials, send_msg


def index(request, group_url):
    group_url = group_url.replace('_', '/')

    login_creds = get_credentials()
    print('\n\n\n', login_creds, '\n\n\n')
    path = os.getcwd() + '/Parser/chromedriver'

    if login_creds:
        parser = FacebookParser(path)

        th = threading.Thread(target=save_members, args=[parser, group_url, login_creds['login'], login_creds['password']])
        th.start()
        return JsonResponse({'process': 'started'})
    else:
        return JsonResponse({"error": 'set login credentials in db'})


def send_messages(request, msg):
    login_creds = get_credentials()
    path = os.getcwd() + '/Parser/chromedriver'

    msg = msg.replace('+', ' ')

    if login_creds:
        parser = FacebookParser(path)

        th = threading.Thread(target=send_msg, args=[parser, login_creds['login'], login_creds['password'], msg])
        th.start()

        return JsonResponse({'process': 'started'})
    else:
        return JsonResponse({"error": 'set login credentials in db'})
