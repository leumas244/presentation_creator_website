from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', LoginView.as_view(template_name='sites/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('passwort-vergessen/', views.forgot_password, name="forgot_password"),
    path('Passwort-aendern/', views.password_change, name="change_password"),
    path('Einstellungen/', views.profile_settings, name='profile_settings'),
    path('account/<str:token>/', views.login_with_token, name='login_with_token'),
    path('first_login/', views.first_login, name='first_login'),
    path('Agenda/<int:identifier>/', views.agenda_by_identifier, name='agenda_by_identifier'),
    path('add_user/', views.add_user, name='add_user'),
    path('admin_settings/', views.admin_settings, name='admin_settings'),
    path('base/', views.base, name='base'),
]
