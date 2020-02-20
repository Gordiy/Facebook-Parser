import os
from .models import Group, Follower
from .FB import FacebookParser

path = os.getcwd() + '/Parser/chromedriver.exe'

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