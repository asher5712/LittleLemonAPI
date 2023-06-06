from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from .models import MenuItem, Category, Cart, Order, OrderItem
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    """
    Model serializer for 'Category' model
    """
    
    class Meta:
        """
        Meta class for 'CategorySerializer' specifying 'model' object and 'fields' to display
        """
        
        model = Category
        fields = ['id', 'slug', 'title']



class MenuItemSerializer(serializers.ModelSerializer):
    """
    Model serializer for 'MenuItem' model
    """
    
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        """
        Meta class for 'MenuItemSerializer' specifying 'model' object and 
        'fields' to display with validators applied on them
        """
        
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(),
                fields=['title', 'category_id']
            )
        ]
        extra_kwargs = {
            'price': {
                'min_value': 1.0
            },
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItem.objects.all()
                    )
                ],
                'max_length': 150
            }
        }



class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer for 'User' model
    """
    
    class Meta:
        """
        Meta class for 'UserSerializer' specifying 'model' object and 
        'fields' to display with applied validators
        """
        
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {
            'email': {'read_only':True}
        }



class CartSerializer(serializers.ModelSerializer):
    """
    Model serializer for 'Cart' model
    """
    
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    # calculated_unit_price = serializers.SerializerMethodField(method_name='get_price')
    # total_price = serializers.SerializerMethodField(method_name='calculate_price')
    
    class Meta:
        """
        Meta class for 'CartSerializer' specifying 'model' object and 
        'fields' to display with validatoions applied on them
        """
        
        model = Cart
        fields = ['id', 'user', 'user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields = ['menuitem_id', 'user_id']
            )
        ]
        extra_kwargs = {
            'quantity': {
                'min_value': 0,
            },
            'unit_price': {
                'min_value': 0.0
            },
            'price': {
                'min_value': 0.0
            },
        }
    
    # def calculate_price(self, product:Cart):
    #     return round(product.unit_price * Decimal(product.quantity), 2)
    
        
    # def get_price(self, product:Cart):
    #     return product.menuitem.price



class OrderItemSerializer(serializers.ModelSerializer):
    """
    Model serializer for 'OrderItem' model
    """
    
    class Meta:
        """
        Meta class for 'OrderItemSerializer' specifying 'model' object and
        'fields' to display with validations applied to them.
        Further the depth of the fields is also specified to show details upto specified level
        """
        
        model = OrderItem
        fields = ['id', 'order','menuitem', 'quantity', 'price', 'unit_price']
        depth = 1
        extra_kwargs = {
            'quantity': {
                'min_value': 0,
            },
            'unit_price': {
                'min_value': 0.0
            },
            'price': {
                'min_value': 0.0
            },
        }



class OrderSerializer(serializers.ModelSerializer):
    """
    Model serializer for 'Order' model with additional OrderItemSerializer field
    """
    
    order_items = OrderItemSerializer(read_only=True, many=True)
    
    class Meta:
        """
        Meta class for 'OrderItemSerializer' specifying 'model' object and 'fields' to display
        """
        
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']
