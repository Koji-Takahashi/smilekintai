from datetime import datetime
from .models import Message, User, control

import requests # API request

url = "https://slack.com/api/channels.history"
def get_slack(id):
    if control.objects.filter(code=id).exists():
        c = control.objects.filter(code=id)[0]
        token = c.API_key
        channel_id = c.channelId
        payload = {
            "token": token,
            "channel": channel_id
            }
        response = requests.get(url, params=payload)
        json_data = response.json()
        messages = json_data["messages"]
        for i in messages:
            if 'リモート退勤' in str(i["text"]):
                status = '退勤'
            elif 'リモート出勤' in str(i["text"]):
                status = '出勤'
            elif '出勤' in str(i["text"]):
                status = '出勤'
            elif '出社' in str(i["text"]):
                status = '出勤'
            elif 'in' in str(i["text"]):
                status = '出勤'
            elif '直行' in str(i["text"]):
                status = '出勤'
            elif '退社' in str(i["text"]):
                status = '退勤'
            elif '退勤' in str(i["text"]):
                status = '退勤'
            elif 'out' in str(i["text"]):
                status = '退勤'
            elif '直帰' in str(i["text"]):
                status = '直帰'
            elif '外出' in str(i["text"]):
                status = '外出中'
            elif '社内' in str(i["text"]):
                status = '出勤'
            elif '昼飯' in str(i["text"]):
                status = '休憩'
            elif 'ご飯' in str(i["text"]):
                status = '休憩'
            elif '休憩' in str(i["text"]):
                status = '休憩'
            elif 'お休み' in str(i["text"]):
                status = '休み'
            elif '有給' in str(i["text"]):
                status = '休み'

            if Message.objects.filter(post_time=i["ts"],div=id).exists():
                if User.objects.filter(slack_id=i["user"]).exists():
                    user_id = User.objects.filter(slack_id=i["user"])[0].id
                    m = Message.objects.get(post_time=i["ts"],div=id)
                    m.user_code = user_id
                    m.message = i["text"]
                    m.encode_time = datetime.fromtimestamp(float(i["ts"]))
                    m.result = status
                    m.post_date = datetime.fromtimestamp(float(i["ts"])).date()
                    m.post_min = datetime.fromtimestamp(float(i["ts"])).time().strftime("%H:%M")
                    m.save()
            elif i.get("user") :
                if User.objects.filter(slack_id=i["user"]).exists():
                    user_id = User.objects.filter(slack_id=i["user"])[0].id
                    m = Message(post_time=i["ts"], post_min=datetime.fromtimestamp(float(i["ts"])).time().strftime("%H:%M"), post_date=datetime.fromtimestamp(float(i["ts"])).date(), div=id, user_code=user_id, result=status, message=i["text"], encode_time=datetime.fromtimestamp(float(i["ts"])))
                    m.save()
            status = ''

        return 'OK'