from rest_framework.permissions import BasePermission

class IsEmailVerified(BasePermission):
    message = "You must confirm your email address to gain access."

    def has_permission(self, request, view):
        return request.user.is_authenticate and request.user.is_email_verfied
