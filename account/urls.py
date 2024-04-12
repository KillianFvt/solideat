from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_account, name='login'),
    path('get-current-user/', views.get_current_user, name='get-current-user'),
]
