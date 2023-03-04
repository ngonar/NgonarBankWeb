from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='account_index'),
    path('api/list_acc', views.get_accounts, name='api_get_accounts'),
    path('api/debalacc/<str:norek>/<int:amount>', views.deduct_account_balance, name='api_deduct_balance'),
    path('api/addbalacc/<str:norek>/<int:amount>', views.topup_account_balance, name='api_topup_balance'),
]

