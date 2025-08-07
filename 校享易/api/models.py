# api/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ===============================================================
# 1. 自定义用户模型
# 继承自Django内置的AbstractUser，方便地扩展字段
# ===============================================================
class User(AbstractUser):
    school_name = models.CharField(max_length=100, verbose_name="院校名称")
    profile = models.TextField(max_length=500, blank=True, null=True, verbose_name="个人简介")

    def __str__(self):
        return self.username

# ===============================================================
# 2. 物品分类模型 (对应 CATEGORIES 表)
# ===============================================================
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="分类名称")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="分类描述")

    class Meta:
        verbose_name = "物品分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# ===============================================================
# 3. 闲置物品模型 (对应 ITEMS 表)
# ===============================================================
class Item(models.Model):
    # 定义物品状态的选项
    STATUS_CHOICES = [
        ('在售', '在售'),
        ('已售', '已售'),
    ]

    title = models.CharField(max_length=100, verbose_name="物品标题")
    description = models.TextField(verbose_name="详细描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='在售', verbose_name="物品状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    
    # 外键关联
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items', verbose_name="发布者")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='items', verbose_name="分类")

    class Meta:
        verbose_name = "闲置物品"
        verbose_name_plural = verbose_name
        ordering = ['-created_at'] # 默认按创建时间倒序排列

    def __str__(self):
        return self.title

# ===============================================================
# 4. 订单模型 (对应 ORDERS 表)
# ===============================================================
class Order(models.Model):
    # 定义订单状态的选项
    STATUS_CHOICES = [
        ('进行中', '进行中'),
        ('已完成', '已完成'),
        ('已取消', '已取消'),
    ]
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="订单创建时间")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='进行中', verbose_name="订单状态")

    # 外键和一对一关联
    item = models.OneToOneField(Item, on_delete=models.CASCADE, verbose_name="交易物品")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="购买者")
    
    class Meta:
        verbose_name = "交易订单"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"订单: {self.item.title}"