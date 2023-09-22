from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('login/', views.login_view, name='login'),
    path('social_login_view/', views.social_login_view, name='social_login'),
    path('signup/', views.signup_view, name='signup'),
]
