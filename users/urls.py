from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path('register/', views.UserCreateAPIView.as_view(), name='users-create'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='users-update'),
]
