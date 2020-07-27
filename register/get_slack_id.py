from .models import User, control

import requests

url = "https://slack.com/api/users.list"


def get_slack_id(id, name):
    div = User.objects.filter(pk=id)[0].div
    if control.objects.filter(code=div).exists():
        c = control.objects.filter(code=div)[0]
        token = c.API_key
        channel_id = c.channelId
        if token == 'None' or token == None:
            return 'FALSE'
        elif channel_id == 'None' or channel_id == None:
            return 'FALSE'
        payload = {
            "token": token,
            "channel": channel_id
            }
        response = requests.get(url, params=payload)
        json_data = response.json()
        members = json_data["members"]
        for i in members:
            if i["is_bot"] == True:
                continue
            if i["profile"]["real_name"] == 'Slackbot':
                continue

            if User.objects.filter(pk=id).exists():
                if i["name"] == name :
                    m = User.objects.get(pk=id)
                    m.slack_id = i["id"]
                    m.save()
                    return str(i["id"])
                else:
                    m = User.objects.filter(pk=id)[0]
                    m.slack_id = ''
                    m.save()

    return 'FALSE'
