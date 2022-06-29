from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.forms import LoginForm
from accounts.views.accounts import (StaffProfileView,
                                     StaffRegisterView,
                                     StaffListView,
                                     StaffEditView,
                                     StaffBlackListView,
                                     StaffEditPhoto,
                                     PasswordChangeView,
                                     StaffDeleteView,
                                     AddToBlackList,
                                     RemoveFromBlackList,
                                     StaffDescriptionView,
                                     StaffPassportView,
                                     StaffPassportPhotoView,
                                     GetAuthTokenTelegram,
                                     StaffPayoutDetailView,
                                     StaffOrderDetailView, Login,
                                     )
from accounts.views.payout import PayoutListView, PayoutCreateView, CashManagerCreateView

from accounts.views.accounts import StaffManagerListView

app_name = 'accounts'

urlpatterns = [
    path('login/',
         Login.as_view(),
         name='login',
         ),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', StaffRegisterView.as_view(), name='register'),
    path("password_change/", PasswordChangeView.as_view(), name="change_password"),
    path('staff/', StaffListView.as_view(), name='staff-list'),
    path('staff/<int:pk>/', StaffProfileView.as_view(), name='profile'),
    path('staff/passport/<int:pk>/', StaffPassportView.as_view(), name='staff-passport'),
    path('staff/passport/add/<int:pk>/', StaffPassportPhotoView.as_view(), name='staff-add-passport'),
    path('staff/edit/<int:pk>/', StaffEditView.as_view(), name='staff-edit'),
    path('staff/description/<int:pk>/', StaffDescriptionView.as_view(), name='staff-description'),
    path('staff/edit/photo/<int:pk>/', StaffEditPhoto.as_view(), name='staff-photo'),
    path('delete/staff/<int:pk>/', StaffDeleteView.as_view(), name='staff-delete'),
    path('black_list/', StaffBlackListView.as_view(), name='black-list'),
    path('black_list/add/<int:pk>/', AddToBlackList.as_view(), name='black-list-add'),
    path('black_list/remove/<int:pk>/', RemoveFromBlackList.as_view(), name='black-list-remove'),
    path('payout/', PayoutListView.as_view(), name='payout_list'),
    path('payout/<int:pk>/', PayoutCreateView.as_view(), name='payout_create'),
    path('staff/<int:pk>/payout/', StaffPayoutDetailView.as_view(), name='staff_payout'),
    path('staff/<int:pk>/cash/', CashManagerCreateView.as_view(), name='cash_manager_create'),
    path("staff/<int:pk>/telegram/token/", GetAuthTokenTelegram.as_view(), name="auth_tg_token"),
    path('staff/<int:pk>/order/', StaffOrderDetailView.as_view(), name='staff_orders'),
    path('staff/manager/', StaffManagerListView.as_view(), name='staff-manager-list'),
]
