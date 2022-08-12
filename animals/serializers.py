from math import log as ln
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
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
    age_in_human_years = serializers.SerializerMethodField()
    group = GroupSerializer(many=False)
    traits = TraitSerializer(many=True)

    def get_age_in_human_years(self, obj) -> int:
        human_age = 16 * ln(obj.age) + 31

        return human_age

    def create(self, validated_data: dict) -> Animal:
        group_data = validated_data.pop("group")
        trait_data = validated_data.pop("traits")

        groupObj, _ = Group.objects.get_or_create(**group_data)

        animal_data = Animal.objects.create(**validated_data, group=groupObj)

        for trait in trait_data:
            traitObj, _ = Trait.objects.get_or_create(**trait)
            animal_data.traits.add(traitObj)
        
        return animal_data

    def update(self, instance: Animal, validated_data: dict) -> Animal:
        non_editable_keys = ("group", "traits", "sex")
        errors = {}

        for key, value in validated_data.items():
            if key in non_editable_keys:
                errors.update({f"{key}": f"You can not update {key} property."})
                continue

            setattr(instance, key, value)

        if errors:
            raise ValidationError(errors)

        instance.save()

        return instance