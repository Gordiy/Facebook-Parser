import os
from .FB import FacebookParser
from django.shortcuts import render


def index(request):
    path = os.getcwd() + '/Parser/chromedriver.exe'
    parser = FacebookParser(path)

    login_url = 'https://www.facebook.com/'

    parser.login(login_url)
    ids = parser.groups_members_id('https://www.facebook.com/groups/312401776077686')

    return render(request, 'index.html')
