# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'items', views.ItemViewSet, basename='item')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    # JWT Token认证路由
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # 用户通过POST用户名和密码到此URL获取Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 刷新Token
]