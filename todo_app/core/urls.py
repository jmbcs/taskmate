from re import template

from core import views as core_views
from django.contrib.auth import views as auth_views
from django.urls import path

# Create your views here.
urlpatterns = [
    path('', core_views.front_page, name='front_page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'login/',
        core_views.login_view,
        name='login',
    ),
    path('sign_up/', core_views.sign_up, name='sign_up'),
]
