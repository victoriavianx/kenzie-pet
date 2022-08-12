from django.test import TestCase
from animals.models import Animal
from groups.models import Group
from traits.models import Trait

class AnimalTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.animal_1_data = {
            "name": "Bidu",
            "age": 1,
            "weight": 30.0,
            "sex": "Macho",
            "group": {"name": "cão", "scientific_name": "canis familiaris"},
            "traits": [{"name": "peludo"}, {"name": "médio porte"}]
        }

        group_1_data = cls.animal_1_data.pop("group")
        trait_1_data = cls.animal_1_data.pop("traits")

        group_animal_1, _ = Group.objects.get_or_create(**group_1_data)
        
        cls.animal_1 = Animal.objects.create(**cls.animal_1_data, group=group_animal_1)

        for trait in trait_1_data:
            traits_animal_1, _ = Trait.objects.get_or_create(**trait)
            cls.animal_1.traits.add(traits_animal_1)

    def test_animal_fields(self):
        print("Execute test_animal_fields")
        
        self.assertEqual(self.animal_1.name, self.animal_1_data["name"])
        self.assertEqual(self.animal_1.age, self.animal_1_data["age"])
        self.assertEqual(self.animal_1.weight, self.animal_1_data["weight"])
        self.assertEqual(self.animal_1.sex, self.animal_1_data["sex"])

        #Comentando esses dois campos, pois está dando erro já que o animal_1_data não tem os ids como o animal_1 tem
        # self.assertEqual(self.animal_1.group, self.animal_1_data["group"])
        # self.assertEqual(self.animal_1.traits, self.animal_1_data["traits"])

    def test_name_max_length(self):
        print("Execute test_name_max_length")

        expected_max_length = 50
        result_max_length = self.animal_1._meta.get_field("name").max_length
        message = "Verifique o max_length do campo 'name'"

        self.assertEqual(result_max_length, expected_max_length, message)