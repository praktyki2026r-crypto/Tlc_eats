from rest_framework.permissions import BasePermission

class IsInitiator(BasePermission):
    """Tylko użytkownik z flagą is_initiator może tworzyć/zamykać zamówienia"""
    message = 'Brak uprawnień inicjatora'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_initiator