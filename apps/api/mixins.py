from rest_framework.exceptions import PermissionDenied


class AdminPermissionMixin:
    is_admin_required = True

    def check_admin_permissions(self):
        if getattr(self.request.user, "role", None) != "admin" and self.is_admin_required:
            raise PermissionDenied("You do not have the rights to perform this action.")


class UserPermissionMixin:
    def check_user_permissions(self, instance_user):
        if self.request.user != instance_user:
            raise PermissionDenied("You do not have the rights to perform this action.")
