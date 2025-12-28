"""
articles/permissions.py - Verify this matches your file
"""
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only access for everyone else.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for authenticated admins
        return request.user and request.user.is_authenticated and request.user.is_admin

class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own articles or admins to edit any.
    """
    def has_permission(self, request, view):
        # Read operations allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write operations require authentication
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read operations allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write operations: must be article author or admin
        return obj.author == request.user or request.user.is_admin