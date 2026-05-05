from django.urls import path, include
from .views import UserRegistrationView, PasswordUpdateView, EmailUpdateView
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('update-password/', PasswordUpdateView.as_view(), name='update-password'),
    path('update-email/', EmailUpdateView.as_view(), name='update-email'),
	path('login/', include('rest_framework.urls')),	
]
