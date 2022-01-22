from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'profile'

main = login_required(views.profile)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="profile/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='profile/logout.html'), name='logout'),
    path('profile/', main, name='main')
]
