import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User, Restaurant, DailySpecial, MenuItem, Order, UserOrder, OrderItem
from .serializers import (RegisterSerializer, LoginSerializer,
                          RestaurantSerializer, MenuItemSerializer,
                          OrderSerializer, CreateOrderSerializer,
                          UpdateOrderSerializer,UserProfileSerializer,
                          UserOrderSerializer, DailySpecialSerializer, OrderItemSerializer)
from django.utils import timezone
from .permissions import IsInitiator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

def send_notification(group, message):
    async_to_sync(channel_layer.group_send)(
        group,
        {
            'type': 'send_notification',
            'message': message,
        }
    )

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

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

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'email': request.user.email,
            'id': request.user.id,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'is_initiator': request.user.is_initiator,
        }, status=status.HTTP_200_OK)

class RestaurantListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        restaurants = Restaurant.objects.all()
        search = request.query_params.get('search')
        if search:
            restaurants = restaurants.filter(name__icontains=search)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RestaurantDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restauracja nie istnieje'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

# GET /restaurants/<id>/daily-special/
class DailySpecialView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restauracja nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

        today = datetime.date.today()
        special = DailySpecial.objects.filter(
            restaurant=restaurant,
            date=today
        ).first()

        if not special:
            return Response({'message': 'Brak dania dnia'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DailySpecialSerializer(special)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInitiator()]
        return [IsAuthenticated()]

    def get(self, request):
        orders = Order.objects.filter(status='active')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActiveOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        qs = Order.objects.filter(
            status='active',
            start_time__lte=now,
            deadline__gte=now
        )

        # opcjonalne filtrowanie po restauracji
        restaurant_id = request.query_params.get('restaurant')
        if restaurant_id:
            qs = qs.filter(restaurant__id=restaurant_id)

        order = qs.first()
        if not order:
            return Response({'message': 'Brak aktywnych zamówień'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CloseOrderView(APIView):
    permission_classes = [IsInitiator]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Zamówienie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

        if order.created_by != request.user:
            return Response({'error': 'Tylko inicjator może zamknąć zamówienie'}, status=status.HTTP_403_FORBIDDEN)

        order.status = 'closed'
        order.save()
        return Response({'message': 'Zamówienie zamknięte'}, status=status.HTTP_200_OK)

class UpdateOrderView(APIView):
    permission_classes = [IsInitiator]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Zamówienie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

        if order.created_by != request.user:
            return Response({'error': 'Tylko inicjator może edytować zamówienie'}, status=status.HTTP_403_FORBIDDEN)

        if order.status == 'closed':
            return Response({'error': 'Nie można edytować zamkniętego zamówienia'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UpdateOrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        if order.status == 'closed':
            return Response({'error': 'Okno zamówień jest zamknięte'}, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.now()
        if now > order.deadline:
            return Response({'error': 'Czas na składanie zamówień minął'}, status=status.HTTP_400_BAD_REQUEST)
        
        if now < order.start_time:
            return Response({'error': 'Okno zamówień jeszcze nie jest otwarte'}, status=status.HTTP_400_BAD_REQUEST)


        # sprawdź czy restauracje są otwarte
        items_data = request.data.get('items', [])
        for item_data in items_data:
            try:
                menu_item = MenuItem.objects.get(pk=item_data.get('menu_item'))
            except MenuItem.DoesNotExist:
                return Response({'error': 'Danie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

            if not menu_item.restaurant.is_open():
                return Response({
                    'error': f'Restauracja {menu_item.restaurant.name} jest teraz zamknięta'
                }, status=status.HTTP_400_BAD_REQUEST)

        user_order, created = UserOrder.objects.get_or_create(
            user=request.user,
            order=order,             
            defaults={'status': 'active'}
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

class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(status='closed').order_by('-deadline')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserOrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_orders = UserOrder.objects.filter(
            user=request.user,
            order__status='closed'
        ).order_by('-order__deadline')
        serializer = UserOrderSerializer(user_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# GET /orders/<id>/summary/ — podsumowanie per restauracja
# GET /orders/<id>/summary/?by=user — podsumowanie per użytkownik
class OrderSummaryView(APIView):
    permission_classes = [IsInitiator]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Zamówienie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

        by = request.query_params.get('by', 'restaurant')

        if by == 'user':
            return self._summary_by_user(order)
        return self._summary_by_restaurant(order)

    def _summary_by_restaurant(self, order):
        from .models import Restaurant
        result = []
        restaurants = Restaurant.objects.filter(
            menuitem__orderitem__order=order
        ).distinct()

        for restaurant in restaurants:
            items = OrderItem.objects.filter(
                order=order,
                menu_item__restaurant=restaurant
            )
            restaurant_items = []
            restaurant_total = 0

            for item in items:
                options = [
                    f"{opt.option.group.name}: {opt.option.name}"
                    for opt in item.selected_options.all()
                ]
                item_total = item.menu_item.price * item.quantity
                for opt in item.selected_options.all():
                    item_total += opt.option.extra_price * item.quantity

                restaurant_items.append({
                    'menu_item': item.menu_item.name,
                    'quantity': item.quantity,
                    'options': options,
                    'note': item.note,
                    'price': item_total,
                })
                restaurant_total += item_total

            result.append({
                'restaurant': restaurant.name,
                'items': restaurant_items,
                'total': restaurant_total,
            })

        return Response(result, status=status.HTTP_200_OK)

    def _summary_by_user(self, order):
        user_orders = UserOrder.objects.filter(order=order)
        result = []

        for user_order in user_orders:
            user_restaurants = {}
            user_total = 0

            for item in user_order.orderitem_set.all():
                restaurant_name = item.menu_item.restaurant.name
                if restaurant_name not in user_restaurants:
                    user_restaurants[restaurant_name] = {
                        'items': [],
                        'total': 0
                    }

                options = [
                    f"{opt.option.group.name}: {opt.option.name}"
                    for opt in item.selected_options.all()
                ]
                item_total = item.menu_item.price * item.quantity
                for opt in item.selected_options.all():
                    item_total += opt.option.extra_price * item.quantity

                user_restaurants[restaurant_name]['items'].append({
                    'menu_item': item.menu_item.name,
                    'quantity': item.quantity,
                    'options': options,
                    'note': item.note,
                    'price': item_total,
                })
                user_restaurants[restaurant_name]['total'] += item_total
                user_total += item_total

            result.append({
                'user': f"{user_order.user.first_name} {user_order.user.last_name}",
                'email': user_order.user.email,
                'restaurants': user_restaurants,
                'total': user_total,
            })

        return Response(result, status=status.HTTP_200_OK)
    
# GET /profile/ — pobierz dane profilu
# PATCH /profile/ — edytuj dane profilu
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# POST /profile/change-password/
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not request.user.check_password(old_password):
            return Response({'error': 'Stare hasło jest nieprawidłowe'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({'error': 'Nowe hasło musi mieć co najmniej 8 znaków'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()
        return Response({'message': 'Hasło zmienione pomyślnie'}, status=status.HTTP_200_OK)
    
class DeleteOrderItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, item_pk):
        try:
            item = OrderItem.objects.get(
                pk=item_pk,
                user_order__user=request.user,
                user_order__pk=pk,
                order__status='active'
            )
        except OrderItem.DoesNotExist:
            return Response({'error': 'Nie znaleziono pozycji'}, status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 # dodaj do views.py

class OrderUserOrdersView(APIView):
    permission_classes = [IsInitiator]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Zamówienie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

        if order.created_by != request.user:
            return Response({'error': 'Brak dostępu'}, status=status.HTTP_403_FORBIDDEN)

        user_orders = UserOrder.objects.filter(order=order)
        serializer = UserOrderSerializer(user_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserOrderStatusView(APIView):
    permission_classes = [IsInitiator]

    def patch(self, request, pk):
        try:
            user_order = UserOrder.objects.get(pk=pk)
        except UserOrder.DoesNotExist:
            return Response({'error': 'Zlecenie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

        if user_order.order.created_by != request.user:
            return Response({'error': 'Brak dostępu'}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        valid_statuses = ['active', 'w_realizacji', 'w_dostarczeniu', 'zakonczone']
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Nieprawidłowy status. Dostępne: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_order.status = new_status
        user_order.save()
        return Response(UserOrderSerializer(user_order).data, status=status.HTTP_200_OK)   
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'Konto zostało usunięte'}, status=status.HTTP_204_NO_CONTENT)

#platnosc
class PayUserOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user_order = UserOrder.objects.get(pk=pk, user=request.user)
        except UserOrder.DoesNotExist:
            return Response({'error': 'Nie znaleziono zamówienia'}, status=404)

        if user_order.payment_status != 'unpaid':
            return Response({'error': 'Płatność już została zgłoszona'}, status=400)

        user_order.payment_status = 'pending'
        user_order.save()

        # powiadomienie dla inicjatorów
        send_notification('initiators', f'{request.user.first_name} {request.user.last_name} zgłosił płatność za zamówienie #{user_order.order.id}')
        return Response({'message': 'Płatność zgłoszona, czeka na potwierdzenie inicjatora'})


class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated, IsInitiator]

    def post(self, request, pk):
        try:
            user_order = UserOrder.objects.get(pk=pk)
        except UserOrder.DoesNotExist:
            return Response({'error': 'Nie znaleziono zamówienia'}, status=404)

        if user_order.payment_status != 'pending':
            return Response({'error': 'Brak oczekującej płatności'}, status=400)

        user_order.payment_status = 'confirmed'
        user_order.save()
        
        # powiadomienie dla pracownika
        send_notification(f'user_{user_order.user.id}', 'Twoja płatność została potwierdzona!')
        return Response({'message': 'Płatność potwierdzona'})
        

class RejectPaymentView(APIView):

    permission_classes = [IsAuthenticated, IsInitiator]

    def post(self, request, pk):
        try:
            user_order = UserOrder.objects.get(pk=pk)
        except UserOrder.DoesNotExist:
            return Response({'error': 'Nie znaleziono zamówienia'}, status=404)

        if user_order.payment_status != 'pending':
            return Response({'error': 'Brak oczekującej płatności'}, status=400)

        user_order.payment_status = 'unpaid'
        user_order.save()

        # powiadomienie dla pracownika
        send_notification(f'user_{user_order.user.id}', 'Twoja płatność została odrzucona. Spróbuj ponownie.')
        return Response({'message': 'Płatność odrzucona'})

class MarkOrderDeliveredView(APIView):
    permission_classes = [IsAuthenticated, IsInitiator]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, created_by=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Nie znaleziono zamówienia'}, status=404)

        if order.delivery_status != 'in_delivery':
            return Response({'error': 'Zamówienie nie jest w trakcie dostawy'}, status=400)

        order.delivery_status = 'delivered'
        order.save()

        # powiadom wszystkich użytkowników
        for user_order in order.userorder_set.all():
            send_notification(f'user_{user_order.user.id}', f'Zamówienie #{order.id} zostało dostarczone!')

        return Response({'message': 'Zamówienie oznaczone jako dostarczone'})