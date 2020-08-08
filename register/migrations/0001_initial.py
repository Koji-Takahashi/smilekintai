# Generated by Django 2.1.5 on 2020-08-08 04:57

from django.db import migrations, models
import django.utils.timezone
import register.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('div', models.CharField(default=uuid.uuid4, max_length=150, verbose_name='会社コード')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='名前')),
                ('slack_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='slack名')),
                ('slack_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='slackId')),
                ('status', models.CharField(blank=True, max_length=255, null=True, verbose_name='ステータス')),
                ('update_time', models.DateTimeField(blank=True, null=True, verbose_name='投稿時間')),
                ('department', models.CharField(blank=True, max_length=255, null=True, verbose_name='部署')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='会社名')),
                ('tel', models.CharField(blank=True, max_length=255, null=True, verbose_name='電話番号')),
                ('postalcode', models.CharField(blank=True, max_length=255, null=True, verbose_name='郵便番号')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='住所')),
                ('flg_seat', models.CharField(blank=True, default=0, max_length=255, null=True, verbose_name='座席不要フラグ')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', register.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attend_day', models.DateField(blank=True, max_length=255, null=True, verbose_name='日付')),
                ('user_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='ユーザID')),
                ('user_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='社員番号')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='氏名')),
                ('work_div', models.CharField(blank=True, max_length=255, null=True, verbose_name='勤務区分')),
                ('work_div_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='勤務区分名')),
                ('start_time', models.CharField(blank=True, max_length=255, null=True, verbose_name='出勤時刻')),
                ('carry_over', models.CharField(blank=True, max_length=255, null=True, verbose_name='前日_翌日')),
                ('end_time', models.CharField(blank=True, max_length=255, null=True, verbose_name='退勤時刻')),
                ('carry_over_1', models.CharField(blank=True, max_length=255, null=True, verbose_name='_前日_翌日')),
                ('rest_start_1', models.CharField(blank=True, max_length=255, null=True, verbose_name='休憩1開始')),
                ('carry_over_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='__前日_翌日')),
                ('rest_end_1', models.CharField(blank=True, max_length=255, null=True, verbose_name='休憩1終了')),
                ('carry_over_3', models.CharField(blank=True, max_length=255, null=True, verbose_name='___前日_翌日')),
                ('rest_start_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='休憩2開始')),
                ('carry_over_4', models.CharField(blank=True, max_length=255, null=True, verbose_name='____前日_翌日')),
                ('rest_end_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='休憩2終了')),
                ('carry_over_5', models.CharField(blank=True, max_length=255, null=True, verbose_name='_____前日_翌日')),
                ('memo', models.CharField(blank=True, max_length=255, null=True, verbose_name='備考')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='所属長コメント')),
                ('approval', models.CharField(blank=True, max_length=255, null=True, verbose_name='申請承認')),
                ('stamp_start_time', models.CharField(blank=True, max_length=255, null=True, verbose_name='打刻出勤')),
                ('stamp_end_time', models.CharField(blank=True, max_length=255, null=True, verbose_name='打刻退勤')),
                ('stamp_rest_start_1', models.CharField(blank=True, max_length=255, null=True, verbose_name='打刻休憩1開始')),
                ('stamp_rest_end_1', models.CharField(blank=True, max_length=255, null=True, verbose_name='打刻休憩1終了')),
                ('stamp_rest_start_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='打刻休憩2開始')),
                ('stamp_rest_end_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='打刻休憩2終了')),
                ('work_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='勤務名')),
                ('day_of_the_week', models.CharField(blank=True, max_length=255, null=True, verbose_name='曜日')),
                ('special_memo', models.CharField(blank=True, max_length=255, null=True, verbose_name='特殊備考')),
                ('work_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='出勤形態')),
                ('blank', models.CharField(blank=True, max_length=255, null=True, verbose_name='ブランク')),
                ('kansei', models.CharField(blank=True, max_length=255, null=True, verbose_name='管制')),
                ('div', models.CharField(blank=True, max_length=255, null=True, verbose_name='自社区分')),
                ('process_month', models.CharField(blank=True, max_length=6, null=True, verbose_name='処理月')),
            ],
        ),
        migrations.CreateModel(
            name='control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=225, verbose_name='会社名')),
                ('code', models.CharField(max_length=225, verbose_name='コード')),
                ('postal_code', models.CharField(blank=True, max_length=10, verbose_name='郵便番号')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='住所')),
                ('url', models.CharField(blank=True, max_length=100, verbose_name='URL')),
                ('tel', models.CharField(blank=True, max_length=20, verbose_name='電話番号')),
                ('fax', models.CharField(blank=True, max_length=100, verbose_name='FAX')),
                ('memo', models.TextField(blank=True, max_length=4000, verbose_name='備考')),
                ('API_key', models.CharField(blank=True, max_length=500, null=True, verbose_name='APIキー')),
                ('channelId', models.CharField(blank=True, max_length=255, null=True, verbose_name='channel ID')),
                ('div', models.CharField(blank=True, max_length=255, null=True, verbose_name='自社区分')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='FMLOGIN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.CharField(blank=True, max_length=255, null=True, verbose_name='経度')),
                ('latitude', models.CharField(blank=True, max_length=255, null=True, verbose_name='緯度')),
                ('IP_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='システムIPアドレス')),
                ('NIC', models.CharField(blank=True, max_length=255, null=True, verbose_name='システムNICアドレス')),
                ('NPC', models.CharField(blank=True, max_length=255, null=True, verbose_name='ネットワークプロトコル')),
                ('SPH', models.CharField(blank=True, max_length=255, null=True, verbose_name='システムプラットホーム')),
                ('SV', models.CharField(blank=True, max_length=255, null=True, verbose_name='システムバージョン')),
                ('AV', models.CharField(blank=True, max_length=255, null=True, verbose_name='アプリケーションバージョン')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.CharField(max_length=255, verbose_name='code')),
                ('post_time', models.CharField(max_length=255, verbose_name='postTime')),
                ('message', models.TextField(blank=True, max_length=50000, verbose_name='message')),
                ('slack_comment_id', models.CharField(blank=True, max_length=255, verbose_name='message')),
                ('encode_time', models.DateTimeField(blank=True, null=True, verbose_name='postTimes')),
                ('div', models.CharField(blank=True, max_length=255, null=True, verbose_name='自社区分')),
                ('result', models.CharField(blank=True, max_length=255, null=True, verbose_name='判定結果')),
                ('post_date', models.DateField(blank=True, null=True, verbose_name='postDate')),
                ('post_min', models.CharField(blank=True, max_length=255, null=True, verbose_name='投稿時間')),
            ],
        ),
    ]
