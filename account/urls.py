from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_account, name='login'),
    path('logout/', views.logout_account, name='logout'),
    path('register/', views.register_account, name='register'),
    path('get-current-user/', views.get_current_user, name='get-current-user'),
]
