from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# 定义内联模型，使UserProfile显示在User管理界面中
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = '用户资料'
    verbose_name_plural = '用户资料'

# 扩展User管理界面
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    
    # 添加用户角色到列表显示
    def get_role(self, obj):
        try:
            return obj.profile.get_role_display()
        except UserProfile.DoesNotExist:
            return '-'
    get_role.short_description = '角色'

# 重新注册User模型
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# 单独注册UserProfile模型
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'specialization', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'specialization')
    readonly_fields = ('created_at', 'updated_at')
