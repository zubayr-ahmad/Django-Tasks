
class SerializerClassMixin:
    serializer_class_mapping = {}

    def get_serializer_class(self):
        version = self.request.version or 'v1'
        return self.serializer_class_mapping.get(version)