from calendar import c
import os
from pyexpat.errors import messages

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest, Http404, JsonResponse
from django.shortcuts import redirect, resolve_url, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, EmailChangeForm
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models.functions import Concat
from django.db.models import Value as V

"""モデル・フォーム"""
from .models import Message, Attendance, control, User, FMLOGIN
from .forms import ControlForm

"""関数"""
from .get_slack_message import get_slack # slack メッセージを取得
from .get_slack_id import get_slack_id # slack idをセットする
from .create_calendar import create_calendar # カレンダー作成
from .get_slackuser_list import create_user # 一括ユーザー作成
from .update_status import update_status # ステータス更新

"""モジュール"""
import datetime # 時間
import calendar # カレンダー
from django.db.models import Q # 検索
import pyperclip # コピー
from django.contrib import messages # メッセージ

"""API response"""
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core import serializers

# ページング処理
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。::

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


User = get_user_model()


@method_decorator(login_required, name='dispatch')
class Top(generic.TemplateView):
    template_name = 'register/index.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'register/index.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('register/mail_template/create/subject.txt', context)
        message = render_to_string('register/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('register:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # まだ仮登録で、他に問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    """本人か、スーパーユーザーだけユーザーページアクセスを許可する"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    """ユーザーの詳細ページ"""
    model = User
    template_name = 'register/user_detail.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    """ユーザー情報更新ページ"""
    model = User
    form_class = UserUpdateForm
    template_name = 'register/user_form.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く

    def get_success_url(self):
        return resolve_url('register:user_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('register:password_change_done')
    template_name = 'register/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'register/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'register/mail_template/password_reset/subject.txt'
    email_template_name = 'register/mail_template/password_reset/message.txt'
    template_name = 'register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('register:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'register/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('register:password_reset_complete')
    template_name = 'register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'register/password_reset_complete.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'register/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('register/mail_template/email_change/subject.txt', context)
        message = render_to_string('register/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('register:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'register/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'register/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)


def create_slack_menber(request, div):
    """ユーザー一括登録"""
    create_user(div);
    return HttpResponse('Create User')


@login_required()
def index(request):
    """TOPメニュー"""
    return render(request,
                  'register/index.html',  # 使用するテンプレート
                    )  # テンプレートに渡すデータ


@login_required()
def set_slack_id(request, id=None, name=None):
    """slack id 取得"""
    if id:
        div = User.objects.filter(id=id)[0].div
        if control.objects.filter(code=div).exists():
            api_key = control.objects.filter(code=div)[0].API_key
            channel_id = control.objects.filter(code=div)[0].channelId
            if api_key == None or api_key == 'None':
                messages.add_message(request, messages.INFO, "API key の登録が確認出来ません。")
                return redirect('register:user_update', id)
            elif channel_id == None or channel_id == 'None':
                messages.add_message(request, messages.INFO, "channel id の登録が確認出来ません。")
                return redirect('register:user_update', id)

    if name:
        RES = get_slack_id(id, name);
        if RES == "FALSE":
            messages.add_message(request, messages.INFO, "Slack名が正しくありません。")
        else:
            messages.add_message(request, messages.INFO, "Slack id がセットされました。(" + str(RES) + ")")
    else:
        messages.add_message(request, messages.INFO, "Slack名の入力がありません。")

    return redirect('register:user_update', id)


@login_required()
def company(request, id=None, value=None):
    """会社情報入力"""
    if value: # valueがある場合会社コードをコピーする。
        pyperclip.copy(value)

    if control.objects.filter(code=id).exists():
        company = control.objects.get(code=id)
    else:
        company = control()

    # POSTの時（新規であれ編集であれ登録ボタンが押されたとき）
    if request.method == 'POST':
        # フォームを生成
        form = ControlForm(request.POST, instance=company)
        if form.is_valid():  # バリデーションがOKなら保存
            company = form.save(commit=False)
            company.code = id
            company.save()
            return redirect('register:index')
    else:  # GETの時（フォームを生成）
        form = ControlForm(instance=company)
    # 新規・編集画面を表示
    return render(request,
                  'register/company.html', {'form':company})  # テンプレートに渡すデータ


@login_required()
def status(request, pk, status):
    """ステータス手動更新ボタン"""
    if User.objects.filter(pk=pk).exists():
        time_now = datetime.datetime.now()
        today = datetime.date.today()
        messages.add_message(request, messages.INFO, "ステータスが" + status + "に変更されました。 ( " + str(time_now) + " )")
        status_msg = 'システム打刻　' + status
        status = status.replace('リモート','')
        user = User.objects.get(pk=pk)
        m = Message(user_code=user.id, message=status_msg,
                    encode_time=time_now, div=user.div, post_date=today, post_min=time_now.time().strftime("%H:%M"), result=status)
        m.save()
        update_status(user.div)

    """TOPメニュー"""
    return render(request,
                  'register/index.html', )  # テンプレートに渡すデータ


@login_required()
def comment_list(request, id=None):
    """社員一覧・メッセージ一覧"""
    if control.objects.filter(code=id).exists(): # API key が登録されているかチェックする。
        api_key = control.objects.filter(code=id)[0].API_key
        channel_id = control.objects.filter(code=id)[0].channelId
        if not api_key == 'None' and not channel_id == 'None' and not api_key == None and not channel_id == None:
            get_slack(id)  # salckメッセージ取込
    update_status(id)  # ステータス更新

    users = User.objects.filter(div=id)
    keyword = request.GET.get('query')
    if keyword:
        users = users.annotate(
            full_name=Concat('first_name', V(' '), 'last_name')
            ).filter(
                Q(full_name__contains=keyword)
                ) 
    return render(request,
                  'register/slack_index.html',  # 使用するテンプレート
                  {'slacks': users}, )  # テンプレートに渡すデータ


@login_required()
def user_list(request, id=None):
    """User List"""
    if User.objects.filter(div=id).exists():
        users = User.objects.filter(div=id)
    else:
        users = ''

    return render(request,
                  'register/user_list.html',  # 使用するテンプレート
                  {'users': users}, )  # テンプレートに渡すデータ


@login_required()
def user_edit(request, id=None, pk=None):
    """ユーザー詳細"""
    if pk:  # idがあるとき（編集の時）
        # idで検索して、結果を戻すか、404エラー
        member = get_object_or_404(User, pk=pk)
    else:  # idが無いとき（新規の時）
        # Memberを作成
        member = User()

    # POSTの時（新規であれ編集であれ登録ボタンが押されたとき）
    if request.method == 'POST':
        # フォームを生成
        form = UserUpdateForm(request.POST, instance=member)
        if form.is_valid():  # バリデーションがOKなら保存
            member = form.save(commit=False)
            member.div = id
            member.save()
            return redirect('register:user_list', id)
    else:  # GETの時（フォームを生成）
        form = UserUpdateForm(instance=member)
        messages = Message.objects.filter(user_code=pk).order_by("encode_time").reverse()

    # 新規・編集画面を表示
    return render(request, 'register/member_edit.html', dict(form=form, id=id, messages=messages, data=member))


@login_required()
def user_del(request, pk):
    """削除"""
    user_id = pk
    # return HttpResponse('削除')
    user = get_object_or_404(User, pk=user_id)
    user.delete()

    return redirect('register:user_list')


@login_required()
def history(request, id=None):
    d = datetime.date.today()
    date_start = d.replace(day=1)
    end_day = calendar.monthrange(date_start.year,date_start.month)[1]
    date_end = d.replace(day=end_day)
    create_calendar(date_start, date_end, id)
    header = str(date_start.year) + '年' + str(date_start.month) + '月'
    yearmonth = str(date_start.year) + str(date_start.month)
    data = Attendance.objects.filter(user_id=id, process_month=yearmonth)
    dict = {'data': data, 'header': header}
    return render(request,
                  'register/history.html', dict)  # テンプレートに渡すデータ


def api_employee(request):
    code = request.GET.get('code')
    if code == None or code == None:
        result = 'Error:code error!'
        return HttpResponse(result)
    if User.objects.filter(div=code,is_active=1).exists():
        users = User.objects.filter(div=code,is_active=1)
        json_data = serializers.serialize('json', users)
    else:
        result = 'Error:No Records!'
        return HttpResponse(result)
    return HttpResponse(json_data, content_type="text/json-comment-filtered")


def api_kintai(request):
    code = request.GET.get('code')
    term = request.GET.get('term')
    if code == None or code == None:
        result = 'Error:code error!'
        return HttpResponse(result)

    d = datetime.date.today()
    date_start = d.replace(day=1)
    end_day = calendar.monthrange(date_start.year,date_start.month)[1]
    date_end = d.replace(day=end_day)
    if term == None or term == 'None':
        term = str(date_start.year) + str(date_start.month)

    if User.objects.filter(div=code, is_active=1).exists():
        user = User.objects.filter(div=code, is_active=1)
    else:
        user = ''
    if user:
        for d in user:
            # 履歴データ更新
            id = d.id
            create_calendar(date_start, date_end, id)

    if Attendance.objects.filter(div=code, process_month=term).exists():
        attend = Attendance.objects.filter(div=code, process_month=term)
        # JSON形式に変換する
        json_data = serializers.serialize('json', attend)
    else:
        result = 'Error:No Records'
        return HttpResponse(result)
    return HttpResponse(json_data, content_type="text/json-comment-filtered")


def api_location(request):
    # 引数を変数に格納
    lng = request.GET.get('lng')
    lat = request.GET.get('lat')
    IP = request.GET.get('IP')
    NIC = request.GET.get('NIC')
    NPC = request.GET.get('NPC')
    SPH = request.GET.get('SPH')
    SV = request.GET.get('SV')
    AV = request.GET.get('AV')

    # レコード作成
    object = FMLOGIN()
    object.longitude = lng
    object.latitude = lat
    object.IP_address = IP
    object.NIC = NIC
    object.NPC = NPC
    object.SPH = SPH
    object.SV = SV
    object.AV = AV
    object.save()
    return HttpResponse('Success:Create Login LOG !')