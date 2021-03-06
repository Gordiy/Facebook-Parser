import os
import random
import time
import threading
from .models import Group, Follower, FacebookCredentials
from .FB import FacebookParser


path = os.getcwd() + '/Parser/chromedriver'
result_available = threading.Event()


def get_credentials():
    login_creds = {}
    creds = FacebookCredentials.objects.all()

    if len(creds) > 1:
        cred_obj = random.randint(0, len(creds)-1)
    elif len(creds) == 0:
        return None
    else:
        cred_obj = 0

    login_creds['login'] = creds[cred_obj].login
    login_creds['password'] = creds[cred_obj].password

    return login_creds


def save_members(parser, group_url, login, pswd):
    parser.login(login, pswd)
    group_members_ids = parser.groups_members_id(group_url)

    if len(group_members_ids) == 0:
        parser.cconnect_to_group(group_url)
        return {'status': 'Subscribe on group. Try later.'}

    result_available.set()

    group, created = Group.objects.get_or_create(link=group_url)

    for member_id in group_members_ids:
        follower, created = Follower.objects.update_or_create(
            group=group,
            fb_id=member_id
        )
        print(follower)


    time.sleep(3)

    parser.close()

    return {'members': group_members_ids}


def send_msg(parser, login, password, text):
    result_available.wait()

    followers = Follower.objects.all()

    if parser.messenger_login(login, password):

        counter = random.randint(20, 30)

        timer_for_sleeping = random.randint(5000, 10000)

        i = 0
        for follower in followers:
            sleep_time = random.randint(3, 6)
            parser.send_message(follower.fb_id, text)
            time.sleep(sleep_time)

            if i == counter:
                time.sleep(timer_for_sleeping)

            i += 1

    parser.close()

def count_messages_all_accounts():
    credentials = FacebookCredentials.objects.all()

    accounts = []

    for creds in credentials:
        info = {}

        parser = FacebookParser(path)

        login = creds.login
        password = creds.password

        parser.login(login, password)
        count = parser.count_messages()

        if count:
            info['login'] = login
            info['password'] = password
            info['count_msg'] = count

            accounts.append(info)

        time.sleep(3)
        parser.close()

    return accounts
