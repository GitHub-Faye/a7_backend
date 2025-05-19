from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import (
    MyTokenObtainPairSerializer, 
    UserSerializer, 
    UserProfileSerializer, 
    RegisterSerializer, 
    PasswordResetRequestSerializer, 
    PasswordChangeSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MyTokenObtainPairView(TokenObtainPairView):
    """
    自定义令牌视图，使用自定义的序列化器
    """
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    """
    用户注册视图
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "用户注册成功",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.profile.role
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    """
    用户列表视图(管理员权限)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        """
        仅管理员可以查看用户列表
        """
        user = self.request.user
        try:
            if user.profile.role == 'admin':
                return User.objects.all()
            else:
                return User.objects.filter(id=user.id)
        except UserProfile.DoesNotExist:
            return User.objects.filter(id=user.id)

class UserDetailView(generics.RetrieveAPIView):
    """
    用户详情视图
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        """
        非管理员只能查看自己的信息
        """
        user_id = self.kwargs.get('pk')
        user = self.request.user
        
        try:
            if str(user.id) == user_id or user.profile.role == 'admin':
                return User.objects.get(id=user_id)
            else:
                return User.objects.get(id=user.id)
        except User.DoesNotExist:
            return None

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    获取和更新用户资料
    """
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        return Response({"detail": "用户资料不存在"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    修改用户密码
    """
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        # 检查旧密码是否正确
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": "原密码错误"}, status=status.HTTP_400_BAD_REQUEST)
            
        # 设置新密码
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({"message": "密码修改成功"}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """
    发送密码重置邮件
    """
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            
            # 生成重置令牌和UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # 构建重置链接
            # 实际项目中，应该是前端页面URL，例如：
            # http://frontend.example.com/reset-password?uid=MQ&token=5jj-460158dd93075981ac62
            reset_link = f"{request.scheme}://{request.get_host()}/api/users/reset-password/{uid}/{token}/"
            
            # 发送邮件
            send_mail(
                subject='重置您的密码',
                message=f'请点击以下链接重置密码: {reset_link}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            
            return Response({"message": "密码重置邮件已发送"}, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            logger.warning(f"密码重置请求：邮箱 {email} 不存在")
            # 为了安全，不告诉用户具体原因
            return Response({"message": "如果该邮箱存在，密码重置邮件已发送"}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    获取当前登录用户信息
    """
    user = request.user
    try:
        role = user.profile.role
    except UserProfile.DoesNotExist:
        role = 'student'  # 默认角色
    
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': role,
    }
    
    return Response(data, status=status.HTTP_200_OK)
