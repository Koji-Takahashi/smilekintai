from .models import User
import requests

url = "https://slack.com/api/users.list"


def create_user(div):
    c = div.objects.filter(code=div)
    token = c.API_key
    channel_id = c.channelId
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

        if User.objects.filter(slack_name=i["name"], div=div).exists():
            m = User.objects.get(slack_name=i["name"], div=div)
            m.slack_id = i["id"]
            m.name = i["profile"]["real_name"]
        else:
            m = User(slack_id=i["id"], slack_name=i["name"], name=i["profile"]["real_name"], div=div)

        m.save()

    return 'OK'