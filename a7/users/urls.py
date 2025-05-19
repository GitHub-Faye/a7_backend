from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    # JWT认证相关
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # 用户注册和认证
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password-change/', views.change_password, name='password_change'),
    path('password-reset-request/', views.password_reset_request, name='password_reset_request'),
    
    # 用户管理
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<str:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    
    # 用户资料
    path('profile/', views.profile_view, name='profile'),
    path('me/', views.get_user_info, name='user_info'),
] 