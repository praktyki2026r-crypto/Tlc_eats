from django.contrib.auth.models import AbstractUser,  BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email jest wymagany')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100) 
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_initiator = models.BooleanField(default=False)  
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def is_open(self):
        from django.utils import timezone
        import datetime
        now = timezone.localtime(timezone.now())
        today = now.weekday()  # 0=poniedziałek, 6=niedziela
        try:
            hours = self.hours.get(day=today)
            if hours.is_closed:
                return False
            return hours.opening_time <= now.time() <= hours.closing_time
        except RestaurantHours.DoesNotExist:
            return True

    def __str__(self):
        return self.name

class RestaurantHours(models.Model):
    DAY_CHOICES = [
        (0, 'Poniedziałek'),
        (1, 'Wtorek'),
        (2, 'Środa'),
        (3, 'Czwartek'),
        (4, 'Piątek'),
        (5, 'Sobota'),
        (6, 'Niedziela'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='hours')
    day = models.IntegerField(choices=DAY_CHOICES)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)  

    class Meta:
        unique_together = ['restaurant', 'day']

    def __str__(self):
        return f"{self.restaurant.name} - {self.get_day_display()}"



class DailySpecial(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='daily_specials')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    source_url = models.URLField(blank=True, null=True)  # link do posta na FB

    def __str__(self):
        return f"{self.restaurant.name} - {self.name} ({self.date})"

class Category(models.Model):
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# danie ze składnikami
class MenuItem(models.Model):
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    ingredients = models.TextField(blank=True, null=True)  # skladniki
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

# grupa opcji
class OptionGroup(models.Model):
    TYPE_CHOICES = [
        ('single', 'Jeden wybór'),
        ('multi', 'Wiele wyborów'),
    ]
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='option_groups')
    name = models.CharField(max_length=100)        # "Rozmiar", "Mleko", "Smak"
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='single')
    required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"

#pojedyncza opcja
class Option(models.Model):
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)        # "Mała", "250ml", "Owsiane"
    extra_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    capacity = models.CharField(max_length=50, blank=True, null=True)  # "250ml", "500g"

    def __str__(self):
        return self.name

#okno zamowien (tworzy inicjator)
class Order(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    DELIVERY_STATUS_CHOICES = [
        ('collecting', 'Zbieranie zamówień'),
        ('in_progress', 'W trakcie realizacji'),
        ('in_delivery', 'W trakcie dostawy'),
        ('delivered', 'Dostarczone'),
    ]
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()        
    deadline = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='collecting')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

#zamowienie uzytkownika
class UserOrder(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('w_realizacji', 'W realizacji'),
        ('w_dostarczeniu', 'W dostarczeniu'),
        ('zakonczone', 'Zakończone'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    PAYMENT_STATUS = [
    ('unpaid', 'Nieopłacone'),
    ('pending', 'Oczekuje na potwierdzenie'),
    ('confirmed', 'Potwierdzone'),
    ('rejected', 'Odrzucone'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')

#pozycja w zamowieniu oraz notatka
class OrderItem(models.Model):
    user_order = models.ForeignKey(UserOrder, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)  # notatka do zamowienia
    quantity = models.IntegerField(default=1)

#wybrane opcje do pozycji
class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='selected_options')
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

class RestaurantOrder(models.Model):
    STATUS = [
        ('collecting', 'Zbieranie zamówień'),      # przed deadlinem
        ('in_progress', 'W trakcie realizacji'),    # po deadlinie
        ('in_delivery', 'W trakcie dostawy'),       # inicjator wysłał
        ('delivered', 'Dostarczone'),               # inicjator potwierdził
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='restaurant_orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='collecting')
    created_at = models.DateTimeField(auto_now_add=True)