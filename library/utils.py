from django.conf import settings
class SerializerClassMixin:
    serializer_class_mapping = {}

    def get_serializer_class(self):
        version = self.request.version or settings.CURRENT_API_VERSION
        return self.serializer_class_mapping.get(version)