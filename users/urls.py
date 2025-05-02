from django.urls import path
from . import views
from .views import UserLoginView

app_name = "users"
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
]