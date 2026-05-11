from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.MeView.as_view(), name='me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Restauracje
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurants'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),

    # Zamówienia
    path('orders/', views.OrderView.as_view(), name='orders'),
    path('orders/<int:pk>/close/', views.CloseOrderView.as_view(), name='order-close'),
    path('user-orders/', views.UserOrderView.as_view(), name='user-orders'),
]