from django.test import TestCase
from traits.models import Trait
from animals.models import Animal

class TraitTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.trait_1_data = {
            "name": "grande porte"
        }

        cls.trait_1 = Trait.objects.create(**cls.trait_1_data)

    def test_trait_fields(self):
        print("Execute test_trait_fields")
        
        self.assertEqual(self.trait_1.name, self.trait_1_data["name"])
        
