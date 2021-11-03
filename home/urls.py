from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', LoginView.as_view(template_name='sites/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('change_password/', PasswordChangeView.as_view(template_name='sites/change_password.html',
                                                        success_url=reverse_lazy('home')), name="change_password"),
    # path('profil/', views.profile, name='profile'),
]
