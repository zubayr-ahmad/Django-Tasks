from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):

    def has_permission(self, request, view):
        # This runs first, before has_object_permission. So I am checking if the user is authenticated.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Just checking if username is same as author's name
        return obj.author.name == request.user.username

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsRegularUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser

class FieldLevelPermission(BasePermission):
    restricted_fields = ['is_featured']

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return True

    def filter_serializer_fields(self, serializer):
        if not self.request.user.is_staff:
            for field in self.restricted_fields:
                if field in serializer.fields:
                    serializer.fields.pop(field)
        return serializer

class IPBasedPermission(BasePermission):
    allowed_ips = ['127.0.0.1', '192.168.1.1']

    def has_permission(self, request, view):
        client_ip = request.META.get('REMOTE_ADDR')
        print("Client IP: ", client_ip)
        return client_ip in self.allowed_ips