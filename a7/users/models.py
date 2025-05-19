from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# 用户扩展模型
class UserProfile(models.Model):
    # 角色选项
    ROLE_CHOICES = [
        ('teacher', '教师'),
        ('student', '学生'),
        ('admin', '管理员'),
    ]
    
    # 与Django内置User模型的一对一关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 角色字段
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # 额外的个人资料字段
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    
    # 教师/学生特定字段
    specialization = models.CharField(max_length=100, blank=True, null=True, verbose_name='专业领域')
    
    # 创建和更新时间
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

# 信号接收器：当新用户创建时自动创建关联的UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# 信号接收器：当User保存时同步保存UserProfile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
