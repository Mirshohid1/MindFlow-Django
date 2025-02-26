from rest_framework.exceptions import PermissionDenied


class AdminPermissionMixin:
    def check_admin_permissions(self):
        if self.request.user.role != 'admin':
            raise PermissionDenied("You do not have the rights to perform this action.")


class UserPermissionMixin:
    def check_user_permissions(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("You do not have the rights to perform this action.")
