from django.urls import path
from .views import HomeView, SinglePostView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug:slug>/', SinglePostView.as_view(), name='single_post'),
]
