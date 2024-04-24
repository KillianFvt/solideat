from django.urls import path, include
from rest_framework import routers
from . import views
from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_account, name='login'),
    path('logout/', views.logout_account, name='logout'),
    path('register/', views.register_account, name='register'),
    path('get-current-user/', views.get_current_user, name='get-current-user'),
]
