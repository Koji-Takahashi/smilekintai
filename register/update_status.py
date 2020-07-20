from .models import Message, User

def update_status(div):
    users = User.objects.all()
    for i in users:
        userId = i.slack_id
        if Message.objects.filter(user_code=userId,div=div).exists():
            messages = Message.objects.filter(user_code=userId,div=div).order_by('encode_time').reverse()
            user = i
            for m in messages:
                if 'リモート退勤' in str(m):
                    user.status = '退勤'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif 'リモート' in str(m):
                    user.status = 'リモート'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '出勤' in str(m):
                    user.status = '出勤'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '出社' in str(m):
                    user.status = '出勤'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif 'in' in str(m):
                    user.status = '出勤'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '直行' in str(m):
                    user.status = '直行'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '退社' in str(m):
                    user.status = '退社'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '退勤' in str(m):
                    user.status = '退勤'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif 'out' in str(m):
                    user.status = '退勤'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '直帰' in str(m):
                    user.status = '直帰'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '外出' in str(m):
                    user.status = '外出中'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '社内' in str(m):
                    user.status = '出勤'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '昼飯' in str(m):
                    user.status = '休憩'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif 'ご飯' in str(m):
                    user.status = '休憩'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '休憩' in str(m):
                    user.status = '休憩'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif 'お休み' in str(m):
                    user.status = '休み'
                    user.update_time = m.encode_time
                    user.save()
                    break
                elif '有給' in str(m):
                    user.status = '休み'
                    user.update_time = m.encode_time
                    user.save()
                    break

    return 'Status Update!'