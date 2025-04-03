# permssions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.contenttypes.models import ContentType

class IsOwner(BasePermission):
    message = "Username and author name should be same."
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

class MethodBasedPermission(BasePermission):
    message = "Nothing for non-authenticated user. GET is for anyone authenticated. POST is for staff user. PUT and PATCH is for owner. DELETE is for admin."
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.is_staff
        if request.method in ('PUT', 'PATCH'):
            return True  
        if request.method == 'DELETE':
            print("Request user: ", request.user)
            print("Request user is superuser: ", request.user.is_superuser)
            return request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH'):
            return request.user.is_superuser or obj.author.name == request.user.username
        return True  

class StaffAndFeatured(BasePermission):
    message = """Staff person can update all books. Other normal users can only update featured books."""
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or obj.is_featured

class ContentTypePermission(BasePermission):
    message = "Only authenticated users can see all the authors."

    def has_permission(self, request, view):
        content_type = ContentType.objects.get_for_model(view.queryset.model)
        print("Content Type: ", content_type)
        if content_type.model == 'author':
            return request.user.is_authenticated
        return True