import os
import random
from .models import Group, Follower, FacebookCredentials

path = os.getcwd() + '/Parser/chromedriver.exe'


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

    group, created = Group.objects.get_or_create(link=group_url)

    for member_id in group_members_ids:
        follower, created = Follower.objects.update_or_create(
            group=group,
            fb_id=member_id
        )
        print(follower)
    return {'members': group_members_ids}