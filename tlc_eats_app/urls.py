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
    path('orders/active/', views.ActiveOrderView.as_view(), name='order-active'),
    path('orders/history/', views.OrderHistoryView.as_view(), name='order-history'), 
    path('orders/<int:pk>/', views.UpdateOrderView.as_view(), name='order-update'),
    path('orders/<int:pk>/close/', views.CloseOrderView.as_view(), name='order-close'),
    path('orders/<int:pk>/summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    
    # Zamowienia uzytkownika
    path('user-orders/', views.UserOrderView.as_view(), name='user-orders'),
    path('user-orders/history/', views.UserOrderHistoryView.as_view(), name='user-order-history')
]