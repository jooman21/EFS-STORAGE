from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import User, Regions

User = get_user_model()


@registry.register_document
class UserDocument(Document):

    class Index:
        name = 'users'

    class Django:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'admin_name',
        ]


@registry.register_document
class RegionsDocument(Document):
    user = fields.ObjectField(properties={
        'username': fields.TextField(),
    })

    class Index:
        name = 'regions'

    class Django:
        model = Regions

        fields = [
            'name',
            'created',
        ]

    def get_queryset(self):
        return super().get_queryset().select_related('created_by')

    def prepare_user(self, instance):
        if instance.created_by:
            return {
                'username': instance.created_by.username,
                'first_name': instance.created_by.first_name,
                'last_name': instance.created_by.last_name,
                'region': instance.created_by.region,
                'admin_name': instance.created_by.admin_name,
            }
