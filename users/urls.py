# from django.contrib.auth.views import LoginView, LogoutView
# from django.urls import path
from users.apps import UsersConfig
# from users.views import ProfileView

app_name = UsersConfig.name


urlpatterns = [
    # path('', LoginView.as_view(template_name='users/login.html'), name='login'),
#     path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
#     path('profile/', ProfileView.as_view(), name='profile'),
    ]