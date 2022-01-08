from django.urls import path 
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('', get_hierarchy),
    path('user/', get_user),
    path('upload/', upload_data),
    path('upload_users/', upload_users),
    path('doors/', get_doors),
    path('lock_door/', lock_door),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]