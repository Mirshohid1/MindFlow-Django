from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from api.mixins import AdminPermissionMixin, UserPermissionMixin


class BaseViewSet(ModelViewSet):
    OutputSerializer = None
    InputSerializer = None

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            if not self.InputSerializer:
                raise ValidationError(
                    f"{self.__class__.__name__}: InputSerializer is not defined, but is required for {self.action}."
                )
            return self.InputSerializer
        if not self.OutputSerializer:
            raise ValidationError(
                f"{self.__class__.__name__}: OutputSerializer is not defined, but is required for {self.action}."
            )
        return self.OutputSerializer


class BaseAdminViewSet(AdminPermissionMixin, BaseViewSet):
    def perform_create(self, serializer):
        self.check_admin_permissions()
        serializer.save()

    def perform_update(self, serializer):
        self.check_admin_permissions()
        serializer.save()

    def perform_destroy(self, instance):
        self.check_admin_permissions()
        instance.delete()


class BaseUserViewSet(UserPermissionMixin, BaseViewSet):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        self.check_user_permissions(serializer.instance.user)
        serializer.save()

    def perform_destroy(self, instance):
        self.check_user_permissions(instance.user)
        instance.delete()
