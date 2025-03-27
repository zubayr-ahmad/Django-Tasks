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