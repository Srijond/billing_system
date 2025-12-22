class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin can do anything, others can only read active packages
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_admin or request.user.is_superuser)
        )