from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义JWT令牌序列化器，添加额外的用户信息
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # 添加自定义声明
        token['username'] = user.username
        try:
            token['role'] = user.profile.role
        except UserProfile.DoesNotExist:
            token['role'] = 'student'  # 默认角色
        
        return token

    def validate(self, attrs):
        # 获取默认的验证数据
        data = super().validate(attrs)
        
        # 添加额外的响应数据
        user = self.user
        data['user_id'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        try:
            data['role'] = user.profile.role
        except UserProfile.DoesNotExist:
            data['role'] = 'student'
            
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户资料序列化器
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, required=False)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, required=False)
    
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'role', 'bio', 'avatar', 'specialization')
        read_only_fields = ('username', 'email')
    
    def update(self, instance, validated_data):
        """
        更新用户资料时同时更新User模型和UserProfile模型
        """
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        # 更新User模型字段
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        user.save()
        
        # 更新UserProfile模型字段
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器，用于用户列表展示
    """
    role = serializers.CharField(source='profile.role', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
        read_only_fields = ('id', 'role')

class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        default='student'
    )
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 
                 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "密码两次输入不匹配"})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "该邮箱已被注册"})
        
        return attrs
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        
        # 在信号中会自动创建UserProfile
        # 这里只需设置角色
        user_profile = UserProfile.objects.get(user=user)
        user_profile.role = role
        user_profile.save()
        
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    密码重置请求序列化器
    """
    email = serializers.EmailField(required=True)

class PasswordChangeSerializer(serializers.Serializer):
    """
    密码修改序列化器
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "密码两次输入不匹配"})
        return attrs 