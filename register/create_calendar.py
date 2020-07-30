from .models import Attendance, User, Message
from datetime import timedelta
import locale
locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

def create_calendar(date_start,date_end,id):
    if User.objects.filter(id=id).exists():
        yearmonth = str(date_start.year) + str(date_start.month)
        user = User.objects.filter(id=id)[0]
        date = date_start
        while date <= date_end:
            if Attendance.objects.filter(user_id=id,attend_day=date).exists():
                a = Attendance.objects.filter(user_id=id,attend_day=date)[0]
            else:
                a = Attendance(user_id=id,attend_day=date)
                a.save()
            if Message.objects.filter(user_code=id, post_date=date, result='出勤').exists():
                m = Message.objects.filter(user_code=id, post_date=date, result='出勤').order_by('encode_time')[0]
                a.start_time = m.post_min
            elif a.start_time == None:
                a.start_time = ''
            if Message.objects.filter(user_code=id, post_date=date, result='退勤').exists():
                m = Message.objects.filter(user_code=id, post_date=date, result='退勤').order_by('encode_time').reverse()[0]
                a.end_time = m.post_min
            elif a.end_time == None:
                a.end_time = ''
            a.process_month = yearmonth
            a.day_of_the_week = date.strftime('%A')
            a.div = user.div
            if Message.objects.filter(user_code=id, post_date=date, message__contains='リモート').exists():
                a.memo = '【リモート】'
            elif a.memo == None:
                a.memo = ''

            a.save()

            date = date + timedelta(days=1)

    return 'OK'
