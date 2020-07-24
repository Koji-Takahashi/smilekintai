from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import uuid


class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル

    usernameを使わず、emailアドレスをユーザー名として使うようにしています。

    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    div = models.CharField('会社コード', max_length=150, default=uuid.uuid4)
    status = models.CharField('ステータス', max_length=150, default=0)
    name = models.CharField('名前', max_length=255, null=True, blank=True)
    slack_name = models.CharField('slack名', max_length=255, null=True, blank=True)
    slack_id = models.CharField('slackId', max_length=255, null=True, blank=True)
    status = models.CharField('ステータス', max_length=255, null=True, blank=True)
    update_time = models.DateTimeField('投稿時間', null=True, blank=True)
    department = models.CharField('部署', max_length=255, null=True, blank=True)
    flg_seat = models.CharField('座席不要フラグ', max_length=255, null=True, blank=True, default=0)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.email

class control(models.Model):
    """"会社情報"""
    name = models.CharField('会社名', max_length=225, blank=True )
    code = models.CharField('コード', max_length=225, blank=False ) #User.div リレーション
    postal_code = models.CharField('郵便番号', max_length=10, blank=True)
    address = models.CharField('住所', max_length=100, blank=True )
    url = models.CharField('URL', max_length=100, blank=True)
    tel = models.CharField('電話番号', max_length=20, blank=True)
    fax = models.CharField('FAX', max_length=100, blank=True)
    memo = models.TextField('備考', max_length=4000, blank=True)
    API_key = models.CharField('APIキー', max_length=500, null=True, blank=True)
    channelId = models.CharField('channel ID', blank=True, null=True, max_length=255 )
    div = models.CharField('自社区分', max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.name;

# Create your models here.
class Message(models.Model):
    """Message"""
    user_code = models.CharField('code', max_length=255) # User::id
    post_time =  models.CharField('postTime', max_length=255)
    message = models.TextField('message', max_length=50000, blank=True)
    slack_comment_id = models.CharField('message', max_length=255, blank=True)
    encode_time =  models.DateTimeField('postTimes', blank=True, null=True )
    div = models.CharField('自社区分', max_length=255, null=True, blank=True)
    result = models.CharField('判定結果', max_length=255, null=True, blank=True)
    post_date = models.DateField('postDate', blank=True, null=True )
    post_min = models.CharField('投稿時間', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.message

class Attendance(models.Model):
    """Seats"""
    attend_day = models.DateField('日付', max_length=255, null=True, blank=True)
    user_id = models.CharField('ユーザID', blank=True, null=True, max_length=255 )
    user_number = models.CharField('社員番号', max_length=255, null=True, blank=True)
    name = models.CharField('氏名', max_length=255, null=True, blank=True)
    work_div = models.CharField('勤務区分', max_length=255, null=True, blank=True)
    work_div_name = models.CharField('勤務区分名', max_length=255, null=True, blank=True)
    start_time = models.CharField('出勤時刻', max_length=255, null=True, blank=True)
    carry_over = models.CharField('前日_翌日', max_length=255, null=True, blank=True)
    end_time = models.CharField('退勤時刻', max_length=255, null=True, blank=True)
    carry_over_1 = models.CharField('_前日_翌日', max_length=255, null=True, blank=True)
    rest_start_1 = models.CharField('休憩1開始', max_length=255, null=True, blank=True)
    carry_over_2 = models.CharField('__前日_翌日', max_length=255, null=True, blank=True)
    rest_end_1 = models.CharField('休憩1終了', max_length=255, null=True, blank=True)
    carry_over_3 = models.CharField('___前日_翌日', max_length=255, null=True, blank=True)
    rest_start_2 = models.CharField('休憩2開始', max_length=255, null=True, blank=True)
    carry_over_4 = models.CharField('____前日_翌日', max_length=255, null=True, blank=True)
    rest_end_2 = models.CharField('休憩2終了', max_length=255, null=True, blank=True)
    carry_over_5 = models.CharField('_____前日_翌日', max_length=255, null=True, blank=True)
    memo = models.CharField('備考', max_length=255, null=True, blank=True)
    comment = models.CharField('所属長コメント', max_length=255, null=True, blank=True)
    approval = models.CharField('申請承認', max_length=255, null=True, blank=True)
    stamp_start_time = models.CharField('打刻出勤', max_length=255, null=True, blank=True)
    stamp_end_time = models.CharField('打刻退勤', max_length=255, null=True, blank=True)
    stamp_rest_start_1 = models.CharField('打刻休憩1開始', max_length=255, null=True, blank=True)
    stamp_rest_end_1 = models.CharField('打刻休憩1終了', max_length=255, null=True, blank=True)
    stamp_rest_start_2 = models.CharField('打刻休憩2開始', max_length=255, null=True, blank=True)
    stamp_rest_end_2 = models.CharField('打刻休憩2終了', max_length=255, null=True, blank=True)
    work_name = models.CharField('勤務名', max_length=255, null=True, blank=True)
    day_of_the_week = models.CharField('曜日', max_length=255, null=True, blank=True)
    special_memo = models.CharField('特殊備考', max_length=255, null=True, blank=True)
    work_type = models.CharField('出勤形態', max_length=255, null=True, blank=True)
    blank = models.CharField('ブランク', max_length=255, null=True, blank=True)
    kansei = models.CharField('管制', max_length=255, null=True, blank=True)
    div = models.CharField('自社区分', max_length=255, null=True, blank=True)
    process_month = models.CharField('処理月', max_length=6, null=True, blank=True)

    def __str__(self):
        return self.user_id

class FMLOGIN(models.Model):
    """FMLOGIN"""
    longitude = models.CharField('経度', max_length=255, blank=True, null=True)
    latitude = models.CharField('緯度', max_length=255, blank=True, null=True)
    IP_address =  models.CharField('システムIPアドレス', max_length=255, blank=True, null=True)
    NIC = models.CharField('システムNICアドレス', max_length=255, blank=True, null=True)
    NPC = models.CharField('ネットワークプロトコル', max_length=255, blank=True, null=True)
    SPH = models.CharField('システムプラットホーム', max_length=255, blank=True, null=True)
    SV = models.CharField('システムバージョン', max_length=255, blank=True, null=True)
    AV = models.CharField('アプリケーションバージョン', max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)