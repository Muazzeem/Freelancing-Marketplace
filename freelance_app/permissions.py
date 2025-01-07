from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Client')

    def has_object_permission(self, request, view, obj):
        return bool(request.user.role == 'Client')  # Allow access only if the user has the 'Client' role

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Admin')

    def has_object_permission(self, request, view, obj):
        return bool(request.user.role == 'Admin')

