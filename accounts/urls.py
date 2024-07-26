from django.urls import path
from .views import SignupView, LoginView, UserProfileView, UsernameChangeView, EmailChangeView, PasswordChangeView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/username_change/', UsernameChangeView.as_view(), name='username_change'),
    path('profile/change_email/', EmailChangeView.as_view(), name='change_email'),
    path('profile/change_password/', PasswordChangeView.as_view(), name='change_password'),
]
