from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users to access
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_admin or request.user.is_superuser)
        )

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to allow users to access their own data or admins to access all
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.is_admin or request.user.is_superuser:
            return True
        
        # User can only access their own data
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user