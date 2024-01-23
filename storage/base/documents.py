from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import VehicleVideo, TheftMurderVideo
from accounts.models import User, Regions


@registry.register_document
class VehDocument(Document):
    # id = fields.IntegerField(),
    # title = fields.TextField(),
    # created = fields.TextField(),
    # incident = fields.TextField(),
    # plate_number = fields.TextField(),
    # diplomat_plate = fields.ObjectField(properties={
    #     #'id': fields.UUIDField(),  #fields.IntegerField(),
    #     'plate_id': fields.TextField(),
    #     'plate_name': fields.TextField(),
    # })
    # plate_region = fields.ObjectField(properties={
    #     #'id': fields.UUIDField(),
    #     'region_name': fields.TextField(),
    # })

    class Index:
        name = 'vehiclevideos'
        settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
        
    class Django:
        model = VehicleVideo
        fields= [
            'title',
            'created',
            'upload',
            'incident',
            'plate_number',
        ]


@registry.register_document
class TMDocument(Document):
    #id = fields.UUIDField()     #fields.IntegerField(),
    # title = fields.TextField(),
    # created = fields.TextField(),
    # incident = fields.TextField(),

    class Index:
        name = 'theftmurdervideos'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = TheftMurderVideo
        
        fields = [
            # 'title',
            # 'created',
            # 'upload',
            # 'incident',
        ]
