from celery import shared_task
from django.utils import timezone
from .models import Order
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery.schedules import crontab

channel_layer = get_channel_layer()

def send_notification(group, message):
    async_to_sync(channel_layer.group_send)(
        group,
        {
            'type': 'send_notification',
            'message': message,
        }
    )

@shared_task
def update_delivery_statuses():
    now = timezone.now()
    
    # Po deadlinie → in_progress
    orders_to_progress = Order.objects.filter(
        delivery_status='collecting',
        deadline__lte=now,
    )
    for order in orders_to_progress:
        order.delivery_status = 'in_progress'
        order.save()
        send_notification(f'user_{order.created_by.id}', f'Zamówienie #{order.id} jest w trakcie realizacji!')
        # powiadom wszystkich użytkowników zamówienia
        for user_order in order.userorder_set.all():
            send_notification(f'user_{user_order.user.id}', f'Zamówienie #{order.id} jest w trakcie realizacji!')

    # 30 min po deadlinie → in_delivery
    orders_to_delivery = Order.objects.filter(
        delivery_status='in_progress',
        deadline__lte=now - timezone.timedelta(minutes=30), #zmienione do testu
    )
    for order in orders_to_delivery:
        order.delivery_status = 'in_delivery'
        order.save()
        send_notification(f'user_{order.created_by.id}', f'Zamówienie #{order.id} jest w trakcie dostawy!')
        for user_order in order.userorder_set.all():
            send_notification(f'user_{user_order.user.id}', f'Zamówienie #{order.id} jest w trakcie dostawy!')

@shared_task
def setup_periodic_tasks(sender, **kwargs):
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )
    
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Aktualizacja statusów dostawy',
        task='tlc_eats_app.tasks.update_delivery_statuses',
    )            