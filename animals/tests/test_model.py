from django.test import TestCase
from animals.models import Animal
from groups.models import Group
from traits.models import Trait
from faker import Faker

class AnimalTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.fake = Faker()

        cls.group = Group.objects.create(name="gato", scientific_name="felis catus")
        cls.trait = Trait.objects.create(name="peludo")

        cls.animal = {
           "name": cls.fake.first_name(),
           "age": cls.fake.pyint(1, 15),
           "weight": cls.fake.pyfloat(min_value=3, max_value=30, right_digits=1),
           "group": cls.group
        }

        cls.animals = [Animal.objects.create(**cls.animal) for _ in range(6)]

    def test_animal_cannot_belong_to_more_than_one_group(self):
        print("Execute test_animal_cannot_belong_to_more_than_one_group")

        group = Group.objects.create(name="cão", scientific_name="canis familiaris")

        for animal in self.animals:
            animal.group = group
            animal.save()
        
        for animal in self.animals:
            self.assertNotIn(animal, self.group.animals.all())
            self.assertIn(animal, group.animals.all())

    def test_animal_can_be_attached_to_multiple_traits(self):
        print("Execute test_animal_can_be_attached_to_multiple_traits")

        for animal in self.animals:
            self.trait.animals.add(animal)

        self.assertEquals(len(self.animals), self.trait.animals.count())

        for animal in self.animals:
            self.assertIn(self.trait, animal.traits.all())
        
    def test_animal_fields(self):
        print("Execute test_animal_fields")

        animal = {
           "name": self.fake.first_name(),
           "age": self.fake.pyint(1, 15),
           "sex": "Não informado",
           "weight": self.fake.pyfloat(min_value=3, max_value=30, right_digits=1),
           "group": self.group
        }

        animal_data = Animal.objects.create(**animal)
        
        self.assertEqual(animal_data.name, animal["name"])
        self.assertEqual(animal_data.age, animal["age"])
        self.assertEqual(animal_data.weight, animal["weight"])
        self.assertEqual(animal_data.sex, animal["sex"])
        self.assertEqual(animal_data.group, animal["group"])
