from rest_framework import serializers, exceptions
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from .models import Animal
from groups.models import Group
from traits.models import Trait

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer(many=False)
    traits = TraitSerializer(many=True)

    def create(self, validated_data: dict):
        group_data = validated_data.pop("group")
        trait_data = validated_data.pop("traits")

        groupObj, _ = Group.objects.get_or_create(**group_data)

        animal_data = Animal.objects.create(**validated_data, group=groupObj)

        for trait in trait_data:
            traitObj, _ = Trait.objects.get_or_create(**trait)
            animal_data.traits.add(traitObj)
        
        return animal_data

    def update(self, instance: Animal, validated_data: dict):

        for key, value in validated_data.items():
            if key == "group" or key == "traits" or key == "sex":
                raise exceptions.ValidationError({f"{key}": f"You can not update {key} property."})

            setattr(instance, key, value)

        instance.save()

        return instance