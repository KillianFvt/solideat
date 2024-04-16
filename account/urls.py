from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register('login/', views.LoginView, basename='login')

urlpatterns = [
    path('login/', views.login_account, name='login'),
    # include(router.urls),
    path('logout/', views.logout_account, name='logout'),
    path('register/', views.register_account, name='register'),
    path('get-current-user/', views.get_current_user, name='get-current-user'),
]
