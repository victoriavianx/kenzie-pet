from rest_framework import serializers
from ..groups.serializers import GroupSerializer
from ..traits.serializers import TraitSerializer
from .models import Animal

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer(many=False)
    traits = TraitSerializer(many=True)

    def create(self, validated_data: dict):
        obj, created = Animal.objects.get_or_create(**validated_data, defaults={"group": validated_data["group"], "traits": validated_data["traits"]})

        return obj

    def update(self, instance: Animal, validated_data: dict):

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance