# api/permissions.py

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限，只允许对象的所有者进行编辑。
    """
    def has_object_permission(self, request, view, obj):
        # 读取权限允许任何请求,
        # 所以我们总是允许 GET, HEAD 或 OPTIONS 请求.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限只给物品的所有者.
        return obj.owner == request.user