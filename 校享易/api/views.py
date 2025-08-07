# api/views.py

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q # 用于复杂查询

from .models import User, Category, Item, Order
from .serializers import (
    UserSerializer, UserCreateSerializer, CategorySerializer,
    ItemSerializer, OrderSerializer, OrderCreateSerializer
)
from .permissions import IsOwnerOrReadOnly # 导入自定义的权限

# ===============================================================
# 1. 用户视图集
# ===============================================================
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    一个用于查看用户的ViewSet。
    提供了 'list' 和 'retrieve' action。
    同时增加了一个自定义的 'register' action 用于用户注册。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """处理用户注册的自定义action"""
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ===============================================================
# 2. 分类视图集
# ===============================================================
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    一个只读的分类视图集。
    提供了 'list' 和 'retrieve' action。
    任何人都可以查看分类。
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

# ===============================================================
# 3. 物品视图集
# ===============================================================
class ItemViewSet(viewsets.ModelViewSet):
    """
    一个完整的物品视图集，处理物品的增删改查。
    """
    queryset = Item.objects.filter(status='在售').order_by('-created_at')
    serializer_class = ItemSerializer
    # 设置权限：对于安全方法（GET）允许任何人，对于其他方法（POST, PUT, DELETE）需要登录且是所有者
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        在创建新物品时，自动将 'owner' 设置为当前登录用户。
        """
        serializer.save(owner=self.request.user)

# ===============================================================
# 4. 订单视图集
# ===============================================================
class OrderViewSet(viewsets.ModelViewSet):
    """
    订单视图集。
    - 创建订单
    - 查看自己的订单列表
    - 查看单个订单详情
    """
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated] # 操作订单必须登录

    def get_serializer_class(self):
        """根据action的不同，返回不同的序列化器"""
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        """
        重写查询集，确保用户只能看到与自己相关的订单
        （自己是买家 或 自己是卖家）。
        """
        user = self.request.user
        return Order.objects.filter(Q(buyer=user) | Q(item__owner=user)).distinct().order_by('-created_at')
    
    def perform_create(self, serializer):
        """
        在创建订单后，需要执行额外的业务逻辑：
        1. 保存订单，将买家设置为当前用户
        2. 将对应物品的状态更新为“已售”
        """
        order = serializer.save(buyer=self.request.user)
        # 更新物品状态
        item = order.item
        item.status = '已售'
        item.save()