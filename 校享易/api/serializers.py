# api/serializers.py

from rest_framework import serializers
from .models import User, Category, Item, Order

# ===============================================================
# 用户相关的序列化器
# ===============================================================

class UserCreateSerializer(serializers.ModelSerializer):
    """用于用户注册的序列化器"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'school_name')

    def create(self, validated_data):
        # 使用模型的 create_user 方法来创建用户，这会自动处理密码哈希
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            school_name=validated_data['school_name']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """用于安全地显示用户信息的序列化器"""
    class Meta:
        model = User
        # 从不包含 password_hash 字段，确保密码安全
        fields = ('id', 'username', 'email', 'school_name', 'profile')


# ===============================================================
# 分类、物品相关的序列化器
# ===============================================================

class CategorySerializer(serializers.ModelSerializer):
    """物品分类的序列化器"""
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    """用于显示/更新物品详情的序列化器"""
    # 当读取数据时，使用 'owner' 和 'category' 的字符串表示（__str__方法）来显示，更具可读性
    owner = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    
    # 当写入数据（创建/更新）时，前端只需要提供 category 的 ID 即可
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Item
        fields = (
            'id', 'title', 'description', 'price', 'status', 
            'created_at', 'owner', 'category', 'category_id'
        )
        # 物品状态通常由后端逻辑（如创建订单时）来改变，而不应由前端直接修改
        read_only_fields = ('status',)


# ===============================================================
# 订单相关的序列化器
# ===============================================================

class OrderSerializer(serializers.ModelSerializer):
    """用于显示订单列表和详情的序列化器"""
    # 嵌套序列化器，用于在订单详情中直接显示完整的物品和买家信息
    item = ItemSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'item', 'buyer', 'status', 'created_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    """用于创建订单的序列化器"""
    # buyer 字段从请求的当前用户中获取，对前端隐藏
    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ('item', 'buyer')
    
    def validate_item(self, item):
        """
        自定义验证逻辑，检查物品是否可被购买。
        这部分逻辑直接来自于您设计的时序图！
        """
        # 检查1：物品是否处于“在售”状态
        if item.status != '在售':
            raise serializers.ValidationError("此物品非“在售”状态，无法购买。")
        
        # 检查2：购买者不能是物品的发布者自己
        if item.owner == self.context['request'].user:
            raise serializers.ValidationError("您不能购买自己发布的物品。")
        
        return item