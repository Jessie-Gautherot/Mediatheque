from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='administration-home'),
    path('login/', views.login_admin, name='login-admin'),

]