from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    # 認証
    path('', views.Top.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),

    # top_navi
    path('company/<str:id>/', views.company, name='company'),  # 会社情報
    path('company/<str:id>/<str:value>/', views.company, name='copy'),  # コピー
    path('set_slack_id/<str:name>/<int:id>', views.set_slack_id, name='set_slack_id'),  # slack id 取得

    # sidebar
    path('index/', views.index, name='index'),  # TOP
    path('status/<int:pk>/<str:status>/', views.status, name='status'),  # ステータス修正
    path('user_list/<str:id>/', views.user_list, name='user_list'),  # user一覧
    path('user/<str:id>/<int:pk>/', views.user_edit, name='user_edit'),  # 詳細
    path('user/del/<int:pk>/', views.user_del, name='user_del'),  # 削除
    path('comment/<str:id>/', views.comment_list, name='comment_list'),  # 一覧
    path('create_user/<str:id>/', views.create_slack_menber, name='create_slack_menber'),  # ユーザー作成
    path('history/<int:id>/', views.history, name='history'),  # 履歴

    # API
    path('api/employee/', views.api_employee, name='api_employee'),  # 履歴
]
