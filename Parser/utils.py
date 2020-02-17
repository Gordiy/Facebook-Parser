import re


def get_id_from_url(url):
    user_id = re.findall('id=[0-9]{15}', url)

    if len(user_id) != 0:
        user_id = user_id[0].split("=")[1]
    else:
        user_id = None

    return user_id


def remove_duplicate(list_):
    for i in range(len(list_)):
        if list_[i] == list_[i + 1]:
            list_.remove(list_[i])
