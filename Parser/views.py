import os
from .FB import FacebookParser
from django.shortcuts import render

from .login_config import login, pswd
from .save import save_members


def index(request):
    path = os.getcwd() + '/Parser/chromedriver.exe'
    parser = FacebookParser(path)

    save_members(parser, 'https://www.facebook.com/groups/518856198557408', login, pswd)
    return render(request, 'index.html')
