from rest_framework import permissions

from src.apps.users.models import UserProfile
from src.apps.orders.models import Cart


class StaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_staff
        )


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_superuser
        )


class CustomerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        
        user_profile = UserProfile.objects.get(user=request.user)
        return user_profile.role == 'customer'

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_superuser
        )


class CartOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        path = request.META['PATH_INFO']
        cart_id = path.split("/")[3]
        cart = Cart.objects.get(id=cart_id)
        if request.user.is_superuser:
            return True
        return cart.user.user == request.user
    
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.cart.user.user == request.user


class OwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or request.user == obj.user
        )
        
class OwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user


class SellerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user_profile = UserProfile.objects.get(user=request.user)
        if request.user.is_superuser or user_profile.role == 'seller':
            return True

        return bool(
            request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):

        user_profile = UserProfile.objects.get(user=request.user)
        if request.user.is_superuser or user_profile.role == 'seller':
            return True

        return bool(
            request.method in permissions.SAFE_METHODS
        )

class NonCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        user_profile = UserProfile.objects.get(user=request.user)
        if request.user.is_superuser or user_profile.role == 'seller':
            return True

        return False
