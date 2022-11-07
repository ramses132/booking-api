from rest_framework.permissions import BasePermission, IsAuthenticated


class PermissionMixin:
    def check_permissions(self, request):
        try:
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)


class IsBusiness(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == request.user.BUSINESS


class EventPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return request.user and request.user.is_authenticated and request.user.role == request.user.BUSINESS 
         
        if view.action == "list":
            return request.user and request.user.is_authenticated
        
        return False

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == request.user.CUSTOMER