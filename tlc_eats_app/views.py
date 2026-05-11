from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Restaurant, MenuItem, Order, UserOrder, OrderItem
from .serializers import (RegisterSerializer, LoginSerializer,
                          RestaurantSerializer, MenuItemSerializer,
                          OrderSerializer, CreateOrderSerializer,
                          UserOrderSerializer, OrderItemSerializer)
from django.utils import timezone

# POST /orders/ — inicjator tworzy okno zamówień
# GET /orders/ — lista aktywnych zamówień

# Generuje token JWT dla użytkownika
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# POST /register/ tworzy usera, zwraca tokeny jwt
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Rejestracja zakończona sukcesem',
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# POST /login/ sprawdza dane, zwraca tokeny jwt
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Zalogowano pomyślnie',
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# POST /logout/ unieważnia refresh token 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Wylogowano pomyślnie'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Nieprawidłowy token'}, status=status.HTTP_400_BAD_REQUEST)

# GET /me/ zwraca dane zalogowanego uzytkownika
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'email': request.user.email,
            'id': request.user.id,
        }, status=status.HTTP_200_OK)

# GET /restaurants/
class RestaurantListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# GET /restaurants/<id>/
class RestaurantDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restauracja nie istnieje'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(deadline__gt=timezone.now())
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# POST /orders/<id>/close/ — zamknięcie zamówienia
class CloseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Zamówienie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

        if order.created_by != request.user:
            return Response({'error': 'Tylko inicjator może zamknąć zamówienie'}, status=status.HTTP_403_FORBIDDEN)

        order.deadline = timezone.now()
        order.save()
        return Response({'message': 'Zamówienie zamknięte'}, status=status.HTTP_200_OK)

# POST /user-orders/ — użytkownik składa zamówienie
class UserOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_orders = UserOrder.objects.filter(user=request.user)
        serializer = UserOrderSerializer(user_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        order_id = request.data.get('order_id')
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Zamówienie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

        if order.deadline <= timezone.now():
            return Response({'error': 'Okno zamówień jest zamknięte'}, status=status.HTTP_400_BAD_REQUEST)

        user_order, created = UserOrder.objects.get_or_create(
            user=request.user,
            status='active'
        )

        items_data = request.data.get('items', [])
        for item_data in items_data:
            item_data['user_order'] = user_order.id
            item_data['order'] = order.id
            serializer = OrderItemSerializer(data=item_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserOrderSerializer(user_order).data, status=status.HTTP_201_CREATED)