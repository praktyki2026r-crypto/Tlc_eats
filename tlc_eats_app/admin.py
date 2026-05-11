from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Restaurant, Category, MenuItem, OptionGroup, Option, Order, UserOrder, OrderItem, OrderItemOption


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'is_staff', 'is_active']
    search_fields = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Uprawnienia', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    inlines = [CategoryInline]


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
   #sdsdsdsdsddddddd
    fields = ['name', 'price', 'ingredients']  
    verbose_name = 'Danie'
    verbose_name_plural = 'Dania'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'restaurant']
    search_fields = ['name']
    list_filter = ['restaurant']
    inlines = [MenuItemInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, MenuItem):
                instance.restaurant = form.instance.restaurant  # ← auto przypisz restaurację
                instance.save()
        formset.save_m2m()


class OptionGroupInline(admin.TabularInline):
    model = OptionGroup
    extra = 1


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'restaurant', 'category']
    search_fields = ['name']
    list_filter = ['restaurant', 'category']
    inlines = [OptionGroupInline]


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'required', 'menu_item']
    list_filter = ['type', 'required']
    inlines = [OptionInline]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'extra_price', 'capacity', 'group']
    search_fields = ['name']


class UserOrderInline(admin.TabularInline):
    model = UserOrder
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'price', 'deadline']
    search_fields = ['created_by__email']
    list_filter = ['deadline']


@admin.register(UserOrder)
class UserOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']
    list_filter = ['status']
    search_fields = ['user__email']


class OrderItemOptionInline(admin.TabularInline):
    model = OrderItemOption
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu_item', 'quantity', 'note', 'user_order']
    search_fields = ['menu_item__name']
    inlines = [OrderItemOptionInline]


@admin.register(OrderItemOption)
class OrderItemOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_item', 'option']