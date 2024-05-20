from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from niyo_tms.users.api.views import RegisterView

app_name = "users"
urlpatterns = [
   
    # path('register/', RegisterView.as_view(), name='user_create'),
    
]
