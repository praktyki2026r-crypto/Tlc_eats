from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Restaurant, Category, MenuItem, OptionGroup, Option, Order, UserOrder, OrderItem, OrderItemOption

# walidacja hasel, tworzy uzytkownika z zahashowanym haslem
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True) #hasło nie wroci w odpowiedzi json

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Hasła nie są identyczne')
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# sprawdza email i haslo
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Nieprawidłowy email lub hasło')
        data['user'] = user
        return data

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'name', 'extra_price', 'capacity']

class OptionGroupSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = OptionGroup
        fields = ['id', 'name', 'type', 'required', 'options']

class MenuItemSerializer(serializers.ModelSerializer):
    option_groups = OptionGroupSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'ingredients', 'option_groups']

class CategorySerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True, source='menuitem_set')

    class Meta:
        model = Category
        fields = ['id', 'name', 'menu_items']

class RestaurantSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True, source='category_set')

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'categories']

#order
class OrderSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_by', 'price', 'deadline', 'is_active']

    def get_is_active(self, obj):
        return obj.deadline > timezone.now()

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['deadline', 'price']

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.create(created_by=user, **validated_data)
        return order

class OrderItemOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemOption
        fields = ['option']

class OrderItemSerializer(serializers.ModelSerializer):
    selected_options = OrderItemOptionSerializer(many=True, required=False)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'note', 'selected_options']

    def create(self, validated_data):
        options_data = validated_data.pop('selected_options', [])
        order_item = OrderItem.objects.create(**validated_data)
        for option_data in options_data:
            OrderItemOption.objects.create(order_item=order_item, **option_data)
        return order_item

class UserOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    total = serializers.SerializerMethodField()

    class Meta:
        model = UserOrder
        fields = ['id', 'user', 'status', 'items', 'total']

    def get_total(self, obj):
        total = 0
        for item in obj.orderitem_set.all():
            total += item.menu_item.price * item.quantity
            for opt in item.selected_options.all():
                total += opt.option.extra_price * item.quantity
        return total